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
    'bulletins_ballot_votes': {
        'cols' : ["CD_ELEICAO", "NR_ZONA", "NR_SECAO", "NR_LOCAL_VOTACAO", "CD_TIPO_URNA", "DS_TIPO_URNA", "NR_URNA_EFETIVADA", "CD_CARGA_1_URNA_EFETIVADA", "CD_CARGA_2_URNA_EFETIVADA", "CD_FLASHCARD_URNA_EFETIVADA", "DT_CARGA_URNA_EFETIVADA", "DS_AGREGADAS", "DT_ABERTURA", "DT_ENCERRAMENTO", "DT_BU_RECEBIDO", "DT_EMISSAO_BU", "QT_ELEITORES_BIOMETRIA_NH", "QT_VOTOS"],
        'pivot_col' : "NR_URNA_EFETIVADA",
        'keep_src_col' : ['CD_ELEICAO', "NR_ZONA", "NR_SECAO", "NR_LOCAL_VOTACAO", "QT_VOTOS"],
        'agg_col' : ["QT_VOTOS"],
        'rename_cols' : {"QT_VOTOS":"TOTAL_VOTOS"}
    },
}


# Agrega todos os votos de uma mesma seção/urna (NR_SECAO), numa mesma eleição (CD_ELEICAO), para o mesmo cargo (CD_CARGO_PERGUNTA)
isFirst = True
for year in ["2020", "2018", "2016", "2014", "2012"]:
    columns = ["CD_ELEICAO", "NR_ZONA", "NR_SECAO", "NR_LOCAL_VOTACAO", "CD_CARGO_PERGUNTA", "QT_APTOS", "QT_COMPARECIMENTO", "QT_ABSTENCOES"]
    df_real = pd.read_sql_table('bulletins_'+year, con=engine, schema="public", index_col="id", columns=columns)
    agg_dict = {}
    for column in columns:
        agg_dict[column] = "first"
    df = df_real.groupby(columns, as_index=False).agg(agg_dict)
    df = df.rename(columns={"QT_VOTOS":"TOTAL_VOTOS"})
    df.to_sql("bulletins_section_votes", con=engine, schema="public", if_exists="replace" if isFirst else "append", index=None)
    isFirst = False

# Agrega todos os votos de uma mesma escola (NR_ZONA + NR_LOCAL_VOTACAO), numa mesma eleição (CD_ELEICAO), para o mesmo cargo (CD_CARGO_PERGUNTA)
isFirst = True
for year in ["2020", "2018", "2016", "2014", "2012"]:
    columns = ["CD_ELEICAO", "NR_ZONA", "NR_LOCAL_VOTACAO", "CD_CARGO_PERGUNTA", "QT_APTOS", "QT_COMPARECIMENTO", "QT_ABSTENCOES", "QT_VOTOS"]
    df_real = pd.read_sql_table('bulletins_'+year, con=engine, schema="public", index_col="id", columns=columns)
    agg_dict = {}
    for column in columns:
        agg_dict[column] = "first"
    agg_dict["QT_VOTOS"] = "sum"
    not_agg_cols = copy.deepcopy(columns)
    not_agg_cols.remove("QT_VOTOS")
    df = df_real.groupby(not_agg_cols, as_index=False).agg(agg_dict)
    df = df.rename(columns={"QT_VOTOS":"TOTAL_VOTOS"})
    df.to_sql("bulletins_school_votes", con=engine, schema="public", if_exists="replace" if isFirst else "append", index=None)
    isFirst = False