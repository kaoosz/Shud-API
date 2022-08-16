# Os arquivos de dump no banco devem ser executados em uma máquina com bastante memoria RAM e inseridos à DB remota a partir da engine correta.

# Bibliotecas
import os
import dotenv
dotenv.load_dotenv()
import pandas as pd
import sqlalchemy

#engine = create_engine("postgresql://"+os.getenv('DB_USERNAME')+":"+os.getenv('REMOTE_PSQL_PASSWORD')+"@"+os.getenv('REMOTE_PSQL_IP')+":"+os.getenv('DB_PORT')+"/"+os.getenv('DB_DATABASE')+"")
engine = sqlalchemy.create_engine("postgresql://"+os.getenv('DB_USERNAME')+":"+os.getenv('DB_PASSWORD')+"@"+os.getenv('DB_HOST')+":"+os.getenv('DB_PORT')+"/"+os.getenv('DB_DATABASE')+"")

pd.set_option("display.max_columns", None)

pivot_tables = {
    'candidates_elections': {
        'cols' : ["ANO_ELEICAO", "CD_TIPO_ELEICAO", "NM_TIPO_ELEICAO", "NR_TURNO", "CD_ELEICAO", "DS_ELEICAO", "DT_ELEICAO", "TP_ABRANGENCIA"],
        'pivot_col' : 'CD_ELEICAO',
    },
    'candidates_situations': {
        'cols' : ["CD_SITUACAO_CANDIDATO_PLEITO", "DS_SITUACAO_CANDIDATO_PLEITO"],
        'pivot_col' : 'CD_SITUACAO_CANDIDATO_PLEITO'
    },
    'candidates_genders': {
        'cols' : ["CD_GENERO", "DS_GENERO"],
        'pivot_col' : 'CD_GENERO'
    },
    'candidates_status': {
        'cols' : ["CD_SITUACAO_CANDIDATURA", "DS_SITUACAO_CANDIDATURA"],
        'pivot_col' : 'CD_SITUACAO_CANDIDATURA'
    },
    'candidates_status_after': {
        'cols' : ["CD_SIT_TOT_TURNO", "DS_SIT_TOT_TURNO"],
        'pivot_col' : 'CD_SIT_TOT_TURNO'
    },
    'candidates_scholarities': {
        'cols' : ["CD_GRAU_INSTRUCAO", "DS_GRAU_INSTRUCAO"],
        'pivot_col' : 'CD_GRAU_INSTRUCAO'
    },
    'candidates_races': {
        'cols' : ["CD_COR_RACA", "DS_COR_RACA"],
        'pivot_col' : 'CD_COR_RACA'
    },
    'candidates_places': {
        'cols' : ["SG_UF", "SG_UE", "NM_UE"],
        'pivot_col' : 'SG_UE'
    },
    'candidates_parties': {
        'cols' : ["NR_PARTIDO", "SG_PARTIDO", "NM_PARTIDO"],
        'pivot_col' : 'NR_PARTIDO'
    },
    'candidates_offices': {
        'cols' : ["CD_CARGO", "DS_CARGO"],
        'pivot_col' : 'CD_CARGO'
    },
    'candidates_occupations': {
        'cols' : ["CD_OCUPACAO", "DS_OCUPACAO"],
        'pivot_col' : 'CD_OCUPACAO'
    },
    'candidates_marital_status': {
        'cols' : ["CD_ESTADO_CIVIL", "DS_ESTADO_CIVIL"],
        'pivot_col' : 'CD_ESTADO_CIVIL'
    },
    'candidates_genders': {
        'cols' : ["CD_GENERO", "DS_GENERO"],
        'pivot_col' : 'CD_GENERO'
    },
    'candidates_coalitions': {
        'cols' : ["CD_ELEICAO", "TP_AGREMIACAO", "SQ_COLIGACAO", "NM_COLIGACAO", "DS_COMPOSICAO_COLIGACAO"],
        'pivot_col' : 'SQ_COLIGACAO',
        'keep_src_col' : 'CD_ELEICAO'
    },
    'candidates_nationalities': {
        'cols' : ["CD_NACIONALIDADE", "DS_NACIONALIDADE"],
        'pivot_col' : 'CD_NACIONALIDADE'
    },
}

df_real = pd.read_sql_table('candidates', con=engine, schema="public", index_col="id")

for pivot_table in pivot_tables:
    unique_cols = pivot_tables[pivot_table]['cols']
    pivot_col = pivot_tables[pivot_table]['pivot_col']

    df = df_real.drop_duplicates(unique_cols, ignore_index=True)

    useless_columns = list(df)
    for col in unique_cols:
        if col in list(df):
            useless_columns.remove(col)
    df.drop(useless_columns, axis=1, inplace=True)

    df.to_sql(pivot_table, con=engine, schema="public", if_exists='replace', index="id")

    candidates = df_real

    if 'keep_src_col' in pivot_tables[pivot_table]:
        unique_cols.remove(pivot_tables[pivot_table]['keep_src_col'])
    unique_cols.remove(pivot_col)
    candidates.drop(unique_cols, axis=1, inplace=True)

    df_real = candidates

# CRIA PIVOT TABLE DE MUNICIPIOS DE NASCIMENTO A PARTIR DA UF/MUNICIPIO DE NASCIMENTO DO CANDIDATO PQ A COLUNA "CD_MUNICIPIO_NASCIMENTO" VEM -3 POR PADRÃO
pivot = pd.read_sql_table("places_cities", con=engine, schema="public", columns=["SG_UF", "CD_MUNICIPIO","NM_MUNICIPIO"])

pivot = pivot.add_suffix('_pivot')

df_real["NM_MUNICIPIO_NASCIMENTO"] = df_real["NM_MUNICIPIO_NASCIMENTO"].str.upper()
df_real["NM_MUNICIPIO_NASCIMENTO"] = df_real["NM_MUNICIPIO_NASCIMENTO"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8') # To sort with accents
df_real['NM_MUNICIPIO_NASCIMENTO'] = df_real['NM_MUNICIPIO_NASCIMENTO'].str.replace(' D ', " D'")

df = pd.merge(df_real, pivot, left_on=["SG_UF_NASCIMENTO","NM_MUNICIPIO_NASCIMENTO"], right_on=["SG_UF_pivot", "NM_MUNICIPIO_pivot"], how='left')

df.drop(["SG_UF_pivot", "NM_MUNICIPIO_pivot", "CD_MUNICIPIO_NASCIMENTO", "NM_MUNICIPIO_NASCIMENTO", "SG_UF_NASCIMENTO", "DS_DETALHE_SITUACAO_CAND", "DS_SITUACAO_CANDIDATO_URNA"], axis=1, inplace=True)

df = df.rename(columns={"CD_MUNICIPIO_pivot":"CD_MUNICIPIO_NASCIMENTO"})

df.to_sql("candidates", con=engine, schema="public", if_exists='replace', index="id")

# gera situacoes das colunas CD_SITUACAO_CANDIDATO_PLEITO e DS_SITUACAO_CANDIDATO_PLEITO a partir da tabela candidates situations
situations = pd.read_sql_table("candidates_situations", con=engine, schema="public", index_col="id")
situations = situations.drop_duplicates(["CD_SITUACAO_CANDIDATO_PLEITO"], ignore_index=True)
situations = situations.rename(columns={"CD_SITUACAO_CANDIDATO_PLEITO":"CD_SITUACAO", "DS_SITUACAO_CANDIDATO_PLEITO":"DS_SITUACAO"})
situations = situations.sort_values(by=["CD_SITUACAO"], ascending=True)
situations.reset_index(drop=True, inplace=True)
situations.to_sql("candidates_situations", con=engine, schema="public", if_exists='replace', index="id")
del situations

# gera coluna de coalition_id na tabela candidates a partir da tabela candidates_coalitions
pivot = pd.read_sql_table('candidates_coalitions', con=engine, schema="public", columns=["id", "CD_ELEICAO", "SQ_COLIGACAO"])
df = df.merge(pivot.add_suffix('_pivot'), how='left', left_on=["CD_ELEICAO", "SQ_COLIGACAO"], right_on=["CD_ELEICAO_pivot", "SQ_COLIGACAO_pivot"])
df.drop(["CD_ELEICAO_pivot", "SQ_COLIGACAO_pivot","SQ_COLIGACAO"], axis=1, inplace=True)
df = df.rename(columns={"id_pivot":"coalition_id"})
df.to_sql("candidates", con=engine, schema="public", if_exists='replace', index="id")