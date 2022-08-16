# Os arquivos de dump no banco devem ser executados em uma máquina com bastante memoria RAM e inseridos à DB remota a partir da engine correta.

# Bibliotecas
import os
import dotenv
dotenv.load_dotenv()
import pandas as pd
import sqlalchemy
import copy
import numpy as np

#engine = create_engine("postgresql://"+os.getenv('DB_USERNAME')+":"+os.getenv('REMOTE_PSQL_PASSWORD')+"@"+os.getenv('REMOTE_PSQL_IP')+":"+os.getenv('DB_PORT')+"/"+os.getenv('DB_DATABASE')+"")
engine = sqlalchemy.create_engine("postgresql://"+os.getenv('DB_USERNAME')+":"+os.getenv('DB_PASSWORD')+"@"+os.getenv('DB_HOST')+":"+os.getenv('DB_PORT')+"/"+os.getenv('DB_DATABASE')+"")

pd.set_option("display.max_columns", None)

pivot_tables = {
    'bulletins_ballots': {
        'cols' : ["CD_ELEICAO", "NR_ZONA", "NR_SECAO", "NR_LOCAL_VOTACAO", "CD_TIPO_URNA", "DS_TIPO_URNA", "NR_URNA_EFETIVADA", "CD_CARGA_1_URNA_EFETIVADA", "CD_CARGA_2_URNA_EFETIVADA", "CD_FLASHCARD_URNA_EFETIVADA", "DT_CARGA_URNA_EFETIVADA", "DS_AGREGADAS", "DT_ABERTURA", "DT_ENCERRAMENTO", "DT_BU_RECEBIDO", "DT_EMISSAO_BU", "QT_ELEITORES_BIOMETRIA_NH", "QT_VOTOS"],
        'pivot_col' : "NR_URNA_EFETIVADA",
        'keep_src_col' : ['CD_ELEICAO', "NR_ZONA", "NR_SECAO", "NR_LOCAL_VOTACAO", "QT_VOTOS"],
        'agg_col' : ["QT_VOTOS"],
        'rename_cols' : {"QT_VOTOS":"TOTAL_VOTOS"}
    },
    'bulletins_zone_votes': {
        'cols' : ["CD_ELEICAO", "CD_CARGO_PERGUNTA", "CD_MUNICIPIO", "NR_ZONA", "QT_VOTOS"],
        'pivot_col' : "NR_ZONA",
        'keep_src_col' : ["CD_ELEICAO", "CD_CARGO_PERGUNTA", "CD_MUNICIPIO", "NR_ZONA", "QT_VOTOS"],
        'agg_col' : ["QT_VOTOS"],
        'rename_cols' : {"QT_VOTOS":"TOTAL_VOTOS"}
    },
    'bulletins_section_votes': {
        'cols' : ["CD_ELEICAO", "CD_CARGO_PERGUNTA", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "QT_APTOS", "QT_COMPARECIMENTO", "QT_ABSTENCOES"],
        'pivot_col' : "NR_ZONA",
        'keep_src_col' : ["CD_ELEICAO", "CD_CARGO_PERGUNTA", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"],
    },
    'bulletins_school_votes': {
        'cols' : ["CD_ELEICAO", "CD_CARGO_PERGUNTA", "CD_MUNICIPIO", "NR_ZONA", "NR_LOCAL_VOTACAO", "QT_VOTOS"],
        'pivot_col' : "NR_ZONA",
        'keep_src_col' : ["CD_ELEICAO", "CD_CARGO_PERGUNTA", "CD_MUNICIPIO", "NR_ZONA", "NR_LOCAL_VOTACAO", "QT_VOTOS"],
        'agg_col' : ["QT_VOTOS"],
        'rename_cols' : {"QT_VOTOS":"TOTAL_VOTOS"}
    },
    'bulletins_city_votes': {
        'cols' : ["CD_ELEICAO", "CD_CARGO_PERGUNTA", "CD_MUNICIPIO", "QT_VOTOS"],
        'pivot_col' : "CD_ELEICAO",
        'keep_src_col' : ["CD_ELEICAO", "CD_CARGO_PERGUNTA", "CD_MUNICIPIO", "QT_VOTOS"],
        'agg_col' : ["QT_VOTOS"],
        'rename_cols' : {"QT_VOTOS":"TOTAL_VOTOS"}
    },
}

years = ["2020", "2018","2016","2014","2012"]

for year in years:
    df_real = pd.read_sql_table('bulletins_'+year, con=engine, schema="public", index_col="id")

    _pivot_tables = copy.deepcopy(pivot_tables)

    for pivot_table in _pivot_tables:
        unique_cols = copy.deepcopy(_pivot_tables[pivot_table]['cols'])
        wrong_cols = list(set(unique_cols)-set(list(df_real)))
        pivot_col = copy.deepcopy(_pivot_tables[pivot_table]['pivot_col'])

        for wrong_col in wrong_cols:
            df_real[wrong_col] = "#NULO#"

        if 'agg_col' in _pivot_tables[pivot_table]:
            agg_dict = {}
            for column in _pivot_tables[pivot_table]['cols']:
                if column not in _pivot_tables[pivot_table]['agg_col']:
                    agg_dict[column] = "first"
                else:
                    agg_dict[column] = "sum"
            for agg_col_item in _pivot_tables[pivot_table]['agg_col']:
                not_agg_cols = _pivot_tables[pivot_table]['cols'][:]
                not_agg_cols.remove(agg_col_item)
            df = df_real.groupby(not_agg_cols, as_index=False).agg(agg_dict)
        else:
            df = df_real.drop_duplicates(unique_cols, ignore_index=True)

        useless_columns = list(df)
        for col in unique_cols:
            if col in list(df):
                useless_columns.remove(col)
        df.drop(useless_columns, axis=1, inplace=True)

        if 'rename_cols' in _pivot_tables[pivot_table]:
            df = df.rename(columns=_pivot_tables[pivot_table]['rename_cols'])

        df = df.apply(lambda x: x.str.strip() if isinstance(x, str) else x).replace('#NULO#', np.nan)

        df.to_sql(pivot_table, con=engine, schema="public", if_exists="append", index="id")

        bulletins = df_real

        if 'keep_src_col' in _pivot_tables[pivot_table]:
            for item in _pivot_tables[pivot_table]['keep_src_col']:
                unique_cols.remove(item)
        if pivot_col in unique_cols:
            unique_cols.remove(pivot_col)
        bulletins.drop(unique_cols, axis=1, inplace=True)

        df_real = bulletins

    cols_to_drop = ["ANO_ELEICAO", "CD_TIPO_ELEICAO", "NM_TIPO_ELEICAO", "NR_TURNO", "DS_ELEICAO", "DT_PLEITO", "SG_UF", "NM_MUNICIPIO", "DS_CARGO_PERGUNTA", "NM_PARTIDO", "SG_PARTIDO", "DS_TIPO_VOTAVEL"]
    for col_to_drop in cols_to_drop:
        if col_to_drop in list(df_real):
            df_real.drop(col_to_drop, axis=1, inplace=True)

    df_real.to_sql("bulletins_"+year, con=engine, schema="public", if_exists='replace')

    ##### create school_id at bulletins table with pivot on places_schools
    #df_real = pd.read_sql_table('bulletins_'+year, con=engine, schema="public", index_col="id")
    #pivot = pd.read_sql_table('places_schools', con=engine, schema="public", columns=["id", "CD_MUNICIPIO", "NR_ZONA", "NR_LOCAL_VOTACAO"])

    #df_real = df_real.merge(pivot.add_suffix('_pivot'), how='left', left_on=["CD_MUNICIPIO", "NR_ZONA", "NR_LOCAL_VOTACAO"], right_on=["CD_MUNICIPIO_pivot", "NR_ZONA_pivot", "NR_LOCAL_VOTACAO_pivot"])
    #df_real.drop(["CD_MUNICIPIO_pivot", "NR_ZONA_pivot", "NR_LOCAL_VOTACAO_pivot"], axis=1, inplace=True)
    #df_real = df_real.rename(columns={"id_pivot":"bulletins_school_vote_id"})

    #df_real.to_sql("bulletins_"+year, con=engine, schema="public", if_exists='replace', index="id")