# Bibliotecas
import os
import dotenv
dotenv.load_dotenv()
import pandas as pd
from sqlalchemy import create_engine
import boto3

session = boto3.session.Session()
client = session.client('s3', region_name='nyc3', endpoint_url='https://nyc3.digitaloceanspaces.com', aws_access_key_id=os.getenv('DO_SPACES_KEY'), aws_secret_access_key=os.getenv('DO_SPACES_SECRET'))

#engine = create_engine("postgresql://"+os.getenv('DB_USERNAME')+" : "+os.getenv('REMOTE_PSQL_PASSWORD')+"@"+os.getenv('REMOTE_PSQL_IP')+" : "+os.getenv('DB_PORT')+"/"+os.getenv('DB_DATABASE')+"")
engine = create_engine("postgresql://"+os.getenv('DB_USERNAME')+":"+os.getenv('DB_PASSWORD')+"@"+os.getenv('DB_HOST')+":"+os.getenv('DB_PORT')+"/"+os.getenv('DB_DATABASE')+"")


# Download file
file_src = 'eleicoes/localidades/csv/BR_Zona_Secao_2018.csv'
file_dest = '/tmp/BR_Zona_Secao_2018.csv'

client.download_file('shud01', file_src, file_dest)

#Read unzipped file
# df = pd.read_csv(file_dest, encoding="utf-8", sep=";")

# df["NM_MUNICIPIO"] = df["NM_MUNICIPIO"].str.upper()
# df["NM_MUNICIPIO"] = df["NM_MUNICIPIO"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8') # To sort with accents

# df = df.sort_values(by=["SG_UF", "NR_ZONA", "NR_SECAO", "NM_MUNICIPIO"], ascending=True)

# df.reset_index(drop=True, inplace=True)

# # Create or append to table with data
# df.to_sql("places", con=engine, schema="public", if_exists="replace", index='id')

# # delete file
# #os.remove(file_dest)
