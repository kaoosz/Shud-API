    # Processa os votos em escolas individualmente e gera a tabela "votes_neighborhoods" agregando todos os votos de um mesmo candidato no mesmo bairro usando as colunas NR_ZONA e NR_LOCAL_VOTACAO e NM_BAIRRO.

# Bibliotecas
import os
import dotenv
dotenv.load_dotenv()
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine
import numpy as np

# Create engine connection to PostgreSQL
engine = create_engine("postgresql://"+os.getenv('DB_USERNAME')+":"+os.getenv('DB_PASSWORD')+"@"+os.getenv('DB_HOST')+":"+os.getenv('DB_PORT')+"/"+os.getenv('DB_DATABASE')+"")

coligacoes = pd.read_sql_query(f'SELECT * FROM "public"."candidates_coalitions"', con=engine)
candidatos = pd.read_sql_query(f'SELECT * FROM "public"."candidates"', con=engine)
situacoes = pd.read_sql_query(f'SELECT * FROM "public"."candidates_status_after"', con=engine)

candidatos = candidatos.merge(coligacoes, left_on="coalition_id", right_on="id", how="left")
candidatos_cols = list(candidatos)
candidatos = candidatos[candidatos["ST_CANDIDATO_INSERIDO_URNA"] == True]
del_cols = ['id_x', 'DT_GERACAO_HH_GERACAO', 'SQ_CANDIDATO', 'NM_SOCIAL_CANDIDATO', 'NR_CPF_CANDIDATO', 'NM_EMAIL', 'CD_SITUACAO_CANDIDATURA', 'CD_DETALHE_SITUACAO_CAND', 'NR_PARTIDO', 'CD_NACIONALIDADE', 'DT_NASCIMENTO', 'NR_IDADE_DATA_POSSE', 'NR_TITULO_ELEITORAL_CANDIDATO', 'CD_GENERO', 'CD_GRAU_INSTRUCAO', 'CD_ESTADO_CIVIL', 'CD_COR_RACA', 'CD_OCUPACAO', 'VR_DESPESA_MAX_CAMPANHA', 'ST_DECLARAR_BENS', 'NR_PROTOCOLO_CANDIDATURA', 'NR_PROCESSO', 'CD_SITUACAO_CANDIDATO_PLEITO', 'CD_SITUACAO_CANDIDATO_URNA', 'CD_MUNICIPIO_NASCIMENTO', 'coalition_id', 'id_y', 'CD_ELEICAO_y', 'TP_AGREMIACAO']
candidatos.drop(del_cols, axis=1, inplace=True)
candidatos["SG_UE"] = pd.to_numeric(candidatos['SG_UE'], errors='coerce').astype('Int64')

prefeitos_df = []
for ano in [2012, 2016]:
    df = pd.read_sql_query(f'SELECT * FROM "public"."bulletins_{ano}" WHERE "DS_CARGO_PERGUNTA" = \'PREFEITO\'', con=engine)
    df["NM_MUNICIPIO"] = df["NM_MUNICIPIO"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    
    df = df.groupby(["CD_ELEICAO", "NM_VOTAVEL", "NR_VOTAVEL", "SG_PARTIDO", "CD_MUNICIPIO", "NM_MUNICIPIO"], as_index=False, dropna=False).agg({"QT_VOTOS": "sum"})
    df.sort_values(by=["CD_ELEICAO", "NM_MUNICIPIO", "QT_VOTOS"], ascending=[True, True, False], inplace=True)
    
    prefeitos_eleitos = candidatos[(candidatos["CD_ELEICAO_x"].isin([47,48,426,427,221,220])) & (candidatos["CD_CARGO"] == 11) & (candidatos["CD_SIT_TOT_TURNO"].isin([1]))]
    df = df.merge(prefeitos_eleitos, left_on=["CD_ELEICAO", "NM_VOTAVEL", "NR_VOTAVEL", "CD_MUNICIPIO"], right_on=["CD_ELEICAO_x", "NM_URNA_CANDIDATO", "NR_CANDIDATO", "SG_UE"], how="left")

    df["CD_SIT_TOT_TURNO"] = df["CD_SIT_TOT_TURNO"].map(situacoes.set_index("CD_SIT_TOT_TURNO")["DS_SIT_TOT_TURNO"])
    df["ST_REELEICAO"] = df["ST_REELEICAO"].map({False: "Não", True: "Sim"})
    df = df[df["CD_SIT_TOT_TURNO"] == 'ELEITO']

    df.drop(["CD_ELEICAO","CD_CARGO","ST_CANDIDATO_INSERIDO_URNA", "CD_ELEICAO_x","SG_UE", "CD_MUNICIPIO", "NR_CANDIDATO","NM_CANDIDATO","NM_URNA_CANDIDATO","SQ_COLIGACAO"], axis=1, inplace=True)
    df.rename({
        "NM_VOTAVEL":"Candidato",
        "NR_VOTAVEL":"Número",
        "SG_PARTIDO":"Partido",
        "NM_MUNICIPIO":"Município",
        "QT_VOTOS":"Votos",
        "NM_COLIGACAO":"Coligação",
        "DS_COMPOSICAO_COLIGACAO":"Composição da Coligação",
        "ST_REELEICAO":"Reeleição",
        "CD_SIT_TOT_TURNO":"Situação",
    }, axis=1, inplace=True)

    df["Ano"] = ano

    df.to_excel(f"VOTOS_PREFEITO_{ano}.xlsx", index=False, encoding="utf-8")
    prefeitos_df.append(df)
    
prefeitos_df = pd.concat(prefeitos_df)

deputados_df = []
senadores_df = []
for ano in [2014, 2018]:
    for cargo in ["SENADOR","DEPUTADO FEDERAL","DEPUTADO ESTADUAL"]:

        df = pd.read_sql_query(f'SELECT * FROM "public"."bulletins_{ano}" WHERE "DS_CARGO_PERGUNTA" = \'{cargo}\'', con=engine)

        df["NM_MUNICIPIO"] = df["NM_MUNICIPIO"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

        df = df.groupby(["CD_ELEICAO", "NM_VOTAVEL", "NR_VOTAVEL", "SG_PARTIDO", "NM_MUNICIPIO"], as_index=False, dropna=False).agg({"QT_VOTOS": "sum"})
        
        df.sort_values(by=["NM_MUNICIPIO", "QT_VOTOS"], ascending=[True, False], inplace=True)

        votos_cidade = df.groupby(["NM_MUNICIPIO"], as_index=False, dropna=False).agg({"QT_VOTOS": "sum"})
        df["votos_cidade"] = df["NM_MUNICIPIO"].map(votos_cidade.set_index("NM_MUNICIPIO")["QT_VOTOS"])
        df['%'] = round(df["QT_VOTOS"] / df["votos_cidade"] * 100, 2)

        df = df.merge(candidatos, left_on=["CD_ELEICAO", "NM_VOTAVEL"], right_on=["CD_ELEICAO_x", "NM_URNA_CANDIDATO"], how="left")

        df["CD_SIT_TOT_TURNO"] = df["CD_SIT_TOT_TURNO"].map(situacoes.set_index("CD_SIT_TOT_TURNO")["DS_SIT_TOT_TURNO"])
        df["ST_REELEICAO"] = df["ST_REELEICAO"].map({False: "Não", True: "Sim"})

        if cargo != "SENADOR":
            df = df[df["%"] > 1]

        df.drop(["votos_cidade","ST_CANDIDATO_INSERIDO_URNA","CD_ELEICAO","SG_UE", "CD_CARGO", "CD_ELEICAO_x","NR_CANDIDATO","NM_CANDIDATO","NM_URNA_CANDIDATO","SQ_COLIGACAO"], axis=1, inplace=True)

        df.rename({
            "NM_VOTAVEL":"Candidato",
            "NR_VOTAVEL":"Número",
            "SG_PARTIDO":"Partido",
            "NM_MUNICIPIO":"Município",
            "QT_VOTOS":"Votos",
            "NM_COLIGACAO":"Coligação",
            "DS_COMPOSICAO_COLIGACAO":"Composição da Coligação",
            "ST_REELEICAO":"Reeleição",
            "CD_SIT_TOT_TURNO":"Situação",
        }, axis=1, inplace=True)

        df["Ano"] = ano
        df["Cargo"] = cargo

        df.to_excel(f"VOTOS_{cargo}_{ano}.xlsx", index=False, encoding="utf-8")

        if cargo != "SENADOR":
            deputados_df.append(df)
        else:
            senadores_df.append(df)

deputados_df = pd.concat(deputados_df)
senadores_df = pd.concat(senadores_df)

print("\PREFEITOS:")
print(prefeitos_df)
prefeitos_df.to_excel(f"VOTOS_PREFEITOS.xlsx", index=False, encoding="utf-8")

print("\SENADORES:")
print(senadores_df)
senadores_df.to_excel(f"VOTOS_SENADORES.xlsx", index=False, encoding="utf-8")

print("\DEPUTADOS:")
print(deputados_df)
deputados_df.to_excel(f"VOTOS_DEPUTADOS.xlsx", index=False, encoding="utf-8")