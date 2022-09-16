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

df = pd.read_sql_table('places', con=engine, schema="public", columns=['SG_UF', 'CD_MUNICIPIO', 'NM_MUNICIPIO', 'NR_ZONA', 'NR_LOCAL_VOTACAO', 'NM_LOCAL_VOTACAO', 'DS_ENDERECO', 'NM_BAIRRO', 'NR_CEP'])

columns = list(df)
agg_dict = {}
for column_name in columns:
    agg_dict[column_name] = "first"
df = df.groupby(["SG_UF", "NM_MUNICIPIO", "NR_ZONA", "NR_LOCAL_VOTACAO"], as_index=False).agg(agg_dict)

df = df.sort_values(by=["SG_UF", "NM_MUNICIPIO", "NR_ZONA", "NR_LOCAL_VOTACAO"], ascending=True)

df.reset_index(drop=True, inplace=True)

df.to_sql("places_schools", con=engine, schema="public", if_exists='replace', index="id")
