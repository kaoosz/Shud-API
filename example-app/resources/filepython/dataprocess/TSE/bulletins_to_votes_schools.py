# Processa os boletins de urnas individualmente e gera a tabela "votes_schools" agregando todos os votos de um mesmo candidato na mesma escola usando as colunas NR_ZONA e NR_LOCAL_VOTACAO.

# Bibliotecas
import os
import dotenv
dotenv.load_dotenv()
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine

# Create engine connection to PostgreSQL
engine = create_engine("postgresql://"+os.getenv('DB_USERNAME')+":"+os.getenv('DB_PASSWORD')+"@"+os.getenv('DB_HOST')+":"+os.getenv('DB_PORT')+"/"+os.getenv('DB_DATABASE')+"")

df = pd.read_sql_table('bulletins_2012', con=engine, schema="public", index_col="id")

# Keep all columns in the resulting dataframe and aggregate sum by "QT_VOTOS" and other columns in sum_columns
columns = list(df)
sum_columns = ["QT_VOTOS","QT_APTOS","QT_COMPARECIMENTO","QT_ABSTENCOES"] # fix adicionar no school votes as abstencoes e %
agg_dict = {}
for column_name in columns:
    if column_name not in sum_columns:
        agg_dict[column_name] = "first"
    else:
        agg_dict[column_name] = "sum"
df = df.groupby(['NR_ZONA', 'NR_LOCAL_VOTACAO', "NR_VOTAVEL"], as_index=False, dropna=False).agg(agg_dict) # CHECK IF THIS IS WORKING
#df["QT_VOTOS"] = 0 DROP TABLE

# Drop all useless columns to keep disk space
#df.drop(['DT_GERACAO', "HH_GERACAO", "CD_TIPO_ELEICAO", "NM_TIPO_ELEICAO", "DT_PLEITO", "DS_ELEICAO", "CD_MUNICIPIO", "CD_CARGO_PERGUNTA", "CD_TIPO_URNA", "DT_BU_RECEBIDO", "DS_TIPO_URNA", "CD_TIPO_VOTAVEL", "NR_URNA_EFETIVADA", "CD_CARGA_1_URNA_EFETIVADA", "CD_CARGA_2_URNA_EFETIVADA", "CD_FLASHCARD_URNA_EFETIVADA", "DT_CARGA_URNA_EFETIVADA", "DS_CARGO_PERGUNTA_SECAO", "DS_AGREGADAS", "DT_ABERTURA", "DT_ENCERRAMENTO", "QT_ELEITORES_BIOMETRIA_NH", "DT_EMISSAO_BU", "NR_JUNTA_APURADORA", "NR_TURMA_APURADORA"], axis=1, inplace=True)

# Reorganize columns order
# 2016 NM_PARTIDO não existe
#column_order = ["NM_VOTAVEL", "NR_VOTAVEL", "SG_PARTIDO", "NR_PARTIDO", "QT_VOTOS", "NR_ZONA", "NR_LOCAL_VOTACAO", "NR_SECAO", "NM_MUNICIPIO", "SG_UF"]
column_order = ["NM_VOTAVEL", "NR_VOTAVEL", "SG_PARTIDO", "NR_PARTIDO", "QT_VOTOS", "NR_ZONA", "NR_SECAO", "NM_MUNICIPIO", "SG_UF"]
for column in reversed(column_order):
    df = df[ [column] + [ col for col in df.columns if col != column ] ]

# Sort rows by specific columns
df = df.sort_values(by=['QT_VOTOS', "NM_VOTAVEL"], ascending=False)

# Drop column that doesnt matter anymore
df.drop(['NR_SECAO'], axis=1, inplace=True)

# Upload dataframe to SQL server
df.to_sql("votes_schools_2012_test", con=engine, schema="public", if_exists='replace', index="id")
