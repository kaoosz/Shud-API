# Processa a tabela de Seções e elimina as duplicadas, mantendo apenas uma entrada de escola.

# Bibliotecas
import os
import dotenv
dotenv.load_dotenv()
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine
import unicodedata
import boto3
import numpy as np

session = boto3.session.Session()
client = session.client('s3', region_name='nyc3', endpoint_url='https://nyc3.digitaloceanspaces.com', aws_access_key_id=os.getenv('DO_SPACES_KEY'), aws_secret_access_key=os.getenv('DO_SPACES_SECRET'))

# Create engine connection to PostgreSQL
engine = create_engine("postgresql://"+os.getenv('DB_USERNAME')+":"+os.getenv('DB_PASSWORD')+"@"+os.getenv('DB_HOST')+":"+os.getenv('DB_PORT')+"/"+os.getenv('DB_DATABASE')+"")

# Download file
file_src = 'eleicoes/localidades/json/municipios_ibge.json'
file_dest = '/tmp/'+file_src.split("/")[-1]

client.download_file('shud01', file_src, file_dest)

df = pd.read_json(file_dest)
for col in list(df):
    if col not in ['municipio-nome','microrregiao-nome','mesorregiao-nome','regiao-imediata-nome','regiao-intermediaria-nome', 'UF-sigla', 'UF-nome', 'regiao-nome']:
        df.drop(col, axis=1, inplace=True)

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode('utf-8')

df = df.applymap(lambda s: remove_accents(s) if type(s) == str else s)
df = df.applymap(lambda s: s.upper() if type(s) == str else s)

# COLUNAS DA ESQUERDA = IBGE e DIREITA = CITIES
ibge_to_cities = {
    "CAMACAN":"CAMACA",
    "DONA EUZEBIA":"DONA EUSEBIA",
    "OLHOS-D'AGUA":"OLHOS D'AGUA",
    "PINGO-D'AGUA":"PINGO D'AGUA",
    "SAO TOME DAS LETRAS":"SAO THOME DAS LETRAS",
    "SEM-PEIXE":"SEM PEIXE",
    "ELDORADO DO CARAJAS":"ELDORADO DOS CARAJAS",
    "SANTA IZABEL DO PARA":"SANTA ISABEL DO PARA",
    "ACU":"ASSU",
    "ARES":"AREZ",
    "JANUARIO CICCO":"BOA SAUDE",
    "ALVORADA D'OESTE":"ALVORADA DO OESTE",
    "ESPIGAO D'OESTE":"ESPIGAO DO OESTE",
    "AMPARO DO SAO FRANCISCO":"AMPARO DE SAO FRANCISCO",
    "GRACHO CARDOSO":"GRACCHO CARDOSO",
    "SAO LUIZ DO PARAITINGA":"SAO LUIS DO PARAITINGA",
}
df['municipio-nome'].replace(ibge_to_cities, inplace=True)

df['municipio-nome'] = df['municipio-nome'].str.replace(' D ', " D'")

# RENAME COLS
df_real = pd.read_sql_table("places_cities", con=engine, schema="public", index_col="id")
df = df.add_suffix('_pivot')

df = pd.merge(df_real, df, left_on=["SG_UF", "NM_MUNICIPIO"], right_on=["UF-sigla_pivot", "municipio-nome_pivot"], how='left')

df.drop(["UF-sigla_pivot", "municipio-nome_pivot"], axis=1, inplace=True)

new_cols_names = {
    "UF-nome_pivot":"NM_UF",
    "microrregiao-nome_pivot":"NM_MICRORREGIAO",
    "mesorregiao-nome_pivot":"NM_MESORREGIAO",
    "regiao-nome_pivot":"NM_REGIAO",
    "regiao-imediata-nome_pivot":"NM_REG_IMEDIATA",
    "regiao-intermediaria-nome_pivot":"NM_REG_INTERMEDIARIA",
}
df = df.rename(columns=new_cols_names)

df.reset_index(drop=True, inplace=True)

df.to_sql("places_cities", con=engine, schema="public", if_exists='replace', index="id", dtype={"CD_MUNICIPIO":sa.types.String})

# delete file
os.remove(file_dest)

# add UFs as places cities
df2 = df.drop_duplicates(["SG_UF", "NM_UF", "NM_REGIAO"], ignore_index=True)
df2 = df2.loc[df2["SG_UF"] != "ZZ"]
df2["CD_MUNICIPIO"]= df2["SG_UF"]
for col in ["NM_MUNICIPIO","NM_MICRORREGIAO","NM_MESORREGIAO","NM_REG_IMEDIATA","NM_REG_INTERMEDIARIA"]:
    df2[col] = np.nan
df2.index = np.arange(len(df), len(df)+len(df2))

df2.to_sql("places_cities", con=engine, schema="public", if_exists='append', index="id")