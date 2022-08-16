# Processa a tabela de Seções e elimina as duplicadas, mantendo apenas uma entrada de escola.

# Bibliotecas
import os
import dotenv
dotenv.load_dotenv()
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine

# Create engine connection to PostgreSQL
engine = create_engine("postgresql://"+os.getenv('DB_USERNAME')+":"+os.getenv('DB_PASSWORD')+"@"+os.getenv('DB_HOST')+":"+os.getenv('DB_PORT')+"/"+os.getenv('DB_DATABASE')+"")

df = pd.read_sql_table('sections', con=engine, schema="public", index_col="id")

# Keep all columns in the resulting dataframe and aggregate sum by "QT_VOTOS"
columns = list(df)
agg_dict = {}
for column_name in columns:
    agg_dict[column_name] = "first"
df = df.groupby(["NR_ZONA", "NR_LOCAL_VOTACAO"], as_index=False).agg(agg_dict)

# Sort rows by specific columns
df["NM_MUNICIPIO_TEMP"] = df["NM_MUNICIPIO"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8') # To sort with accents
df = df.sort_values(by=["NM_MUNICIPIO_TEMP", "NR_ZONA", "NR_LOCAL_VOTACAO"], ascending=True)

# Drop column that doesnt matter anymore
df.drop(['NR_SECAO', "NM_MUNICIPIO_TEMP"], axis=1, inplace=True)

# Upload dataframe to SQL server
df.to_sql("schools", con=engine, schema="public", if_exists='replace', index="id")
