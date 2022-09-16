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

df = pd.read_sql_table('bulletins', con=engine, schema="public", index_col="id")

# Keep all columns in the resulting dataframe and aggregate sum by "QT_VOTOS" and other columns in sum_columns
columns = list(df)
sum_columns = ["QT_VOTOS"]
agg_dict = {}
for column_name in columns:
    if column_name not in sum_columns:
        agg_dict[column_name] = "first"
    else:
        agg_dict[column_name] = "sum"
df2 = df.groupby(["NM_VOTAVEL", "NR_VOTAVEL", "CD_ELEICAO", "SG_UF"], as_index=False, dropna=False).agg(agg_dict)

# Drop all useless columns to keep disk and memory space
df2.drop(["ANO_ELEICAO", "DS_ELEICAO", "NR_TURNO", "CD_TIPO_ELEICAO", "HH_GERACAO", "DT_GERACAO", "SG_PARTIDO","NM_PARTIDO","NR_PARTIDO","NR_ZONA","NR_LOCAL_VOTACAO","NR_SECAO","NM_MUNICIPIO","CD_PLEITO","DS_CARGO_PERGUNTA","QT_APTOS","QT_COMPARECIMENTO","QT_ABSTENCOES","DS_TIPO_VOTAVEL"], axis=1, inplace=True)

# Read original candidates table
candidatos = pd.read_sql_table('candidates', con=engine, schema="public", index_col="id")

# Merge index columns to get each candidate their total votal count
processed_candidatos = df2.merge(candidatos, left_on=["NM_VOTAVEL", "NR_VOTAVEL", "CD_ELEICAO", "SG_UF"], right_on=["NM_URNA_CANDIDATO", "NR_CANDIDATO", "CD_ELEICAO", "SG_UF"], how='right', suffixes=('', '_df2'))

# Remove all extra columns on the new processed table and keep only QT_VOTOS
extra_columns = [item for item in list(processed_candidatos) if item not in list(candidatos)]
extra_columns.remove("QT_VOTOS")
processed_candidatos.drop(extra_columns, axis=1, inplace=True)

# Drop rows that have QT_VOTOS null
#df = df[df['QT_VOTOS'].notna()]

processed_candidatos.to_sql("candidates", con=engine, schema="public", if_exists='replace', index="id")