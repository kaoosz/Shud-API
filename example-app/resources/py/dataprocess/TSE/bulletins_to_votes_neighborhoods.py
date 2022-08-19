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

df1 = pd.read_sql_table('bulletins_2016', con=engine, schema="public", index_col="id")
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
df = df.groupby(["NR_VOTAVEL", "NM_MUNICIPIO", "NM_BAIRRO"], as_index=False).agg(agg_dict) # FIX IF NEIGHBORHOOD IS NULL DO NOT GO TO DATABASE

# # Drop all useless columns to keep disk space
useless_columns = ["SG_UF_df2", "NM_MUNICIPIO_df2", "NR_ZONA", "NR_LOCAL_VOTACAO", "NR_SECAO", "NR_URNA_EFETIVADA", "CD_MUNICIPIO_df2", "DS_TIPO_VOTAVEL", "NM_LOCAL_VOTACAO", "DS_ENDERECO", "NR_CEP"]
df.drop(useless_columns, axis=1, inplace=True)

# Reorganize columns order
column_order = ["NM_VOTAVEL", "NR_VOTAVEL", "NM_BAIRRO", "QT_VOTOS"]
for column in reversed(column_order):
    df = df[ [column] + [ col for col in df.columns if col != column ] ]

# Sort rows by specific columns
df = df.sort_values(by=["NM_BAIRRO", "QT_VOTOS"], ascending=False)

# Upload dataframe to SQL server
df.to_sql("bairro2016", con=engine, schema="public", if_exists='replace', index="id")
