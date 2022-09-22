# Processa os votos em escolas individualmente e gera a tabela "votes_neighborhoods" agregando todos os votos de um mesmo candidato no mesmo bairro usando as colunas NR_ZONA e NR_LOCAL_VOTACAO e NM_BAIRRO.

# Bibliotecas
import os
import dotenv
dotenv.load_dotenv()
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine

# Create engine connection to PostgreSQL
engine = create_engine("postgresql://"+os.getenv('DB_USERNAME')+":"+os.getenv('DB_PASSWORD')+"@"+os.getenv('DB_HOST')+":"+os.getenv('DB_PORT')+"/"+os.getenv('DB_DATABASE')+"")

df1 = pd.read_sql_table('bulletins_2012', con=engine, schema="public", index_col="id")
df2 = pd.read_sql_table('schools', con=engine, schema="public", index_col="id")

df = df1.merge(df2, on=['NR_ZONA', 'NR_LOCAL_VOTACAO'], how='outer', suffixes=('', '_df2'))

# Keep all columns in the resulting dataframe and aggregate sum by "QT_VOTOS" and other columns in sum_columns
columns = list(df)
sum_columns = ["QT_VOTOS","QT_APTOS","QT_COMPARECIMENTO","QT_ABSTENCOES"] # fix adicionar no school votes as abstencoes e %
agg_dict = {}
for column_name in columns:
    if column_name not in sum_columns:
        agg_dict[column_name] = "first"
    else:
        agg_dict[column_name] = "sum"
df = df.groupby(["NR_VOTAVEL", "NM_MUNICIPIO"], as_index=False).agg(agg_dict) # FIX IF NEIGHBORHOOD IS NULL DO NOT GO TO DATABASE

# Drop all useless columns to keep disk space
#useless_columns = ["SG_UF_df2", "NM_MUNICIPIO_df2", "CD_MUNICIPIO_df2", "HH_GERACAO", "DT_ABERTURA", "DT_ENCERRAMENTO", "QT_ELEITORES_BIOMETRIA_NH", "CD_TIPO_ELEICAO", "NM_TIPO_ELEICAO", "DT_BU_RECEBIDO", "DT_EMISSAO_BU", "NR_JUNTA_APURADORA", "NR_TURMA_APURADORA", "DS_AGREGADAS", "CD_FLASHCARD_URNA_EFETIVADA", "DT_CARGA_URNA_EFETIVADA", "CD_CARGA_2_URNA_EFETIVADA", "CD_CARGA_1_URNA_EFETIVADA", "DS_TIPO_URNA", "CD_TIPO_URNA", "NM_BAIRRO", "NR_ZONA", "NR_LOCAL_VOTACAO", "NR_SECAO", "NR_URNA_EFETIVADA", "DS_CARGO_PERGUNTA_SECAO", "DS_TIPO_VOTAVEL", "NM_LOCAL_VOTACAO", "DS_ENDERECO", "NR_CEP"]
useless_columns = ["SG_UF_df2", "NM_MUNICIPIO_df2", "CD_MUNICIPIO_df2", "CD_TIPO_ELEICAO", "DT_BU_RECEBIDO", "CD_FLASHCARD_URNA_EFETIVADA", "DT_CARGA_URNA_EFETIVADA", "CD_CARGA_2_URNA_EFETIVADA", "CD_CARGA_1_URNA_EFETIVADA", "DS_TIPO_URNA", "CD_TIPO_URNA", "NM_BAIRRO", "NR_ZONA", "NR_LOCAL_VOTACAO", "NR_SECAO", "NR_URNA_EFETIVADA", "NM_LOCAL_VOTACAO", "DS_ENDERECO", "NR_CEP"]
#useless_columns = ["SG_UF_df2", "NM_MUNICIPIO_df2", "CD_MUNICIPIO_df2", "CD_FLASHCARD_URNA_EFETIVADA", "DT_CARGA_URNA_EFETIVADA", "CD_CARGA_2_URNA_EFETIVADA", "CD_CARGA_1_URNA_EFETIVADA", "DS_TIPO_URNA", "CD_TIPO_URNA", "NM_BAIRRO", "NR_ZONA", "NR_LOCAL_VOTACAO", "NR_SECAO", "NR_URNA_EFETIVADA", "DS_ENDERECO", "NR_CEP"]
df.drop(useless_columns, axis=1, inplace=True)

# Reorganize columns order
column_order = ["NM_VOTAVEL", "NR_VOTAVEL", "QT_VOTOS"]
for column in reversed(column_order):
    df = df[ [column] + [ col for col in df.columns if col != column ] ]

# Sort rows by specific columns
df = df.sort_values(by=["NM_MUNICIPIO", "QT_VOTOS"], ascending=False)

# Upload dataframe to SQL server
df.to_sql("votes_cities_2012", con=engine, schema="public", if_exists='replace', index="id")
