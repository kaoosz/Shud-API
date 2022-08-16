# Os arquivos de dump no banco devem ser executados em uma máquina com bastante memoria RAM e inseridos à DB remota a partir da engine correta.

# Bibliotecas
import os
import dotenv
dotenv.load_dotenv()
import pandas as pd
import sqlalchemy

engine = sqlalchemy.create_engine("postgresql://"+os.getenv('DB_USERNAME')+":"+os.getenv('REMOTE_PSQL_PASSWORD')+"@"+os.getenv('REMOTE_PSQL_IP')+":"+os.getenv('DB_PORT')+"/"+os.getenv('DB_DATABASE')+"")
#engine = sqlalchemy.create_engine("postgresql://"+os.getenv('DB_USERNAME')+":"+os.getenv('DB_PASSWORD')+"@"+os.getenv('DB_HOST')+":"+os.getenv('DB_PORT')+"/"+os.getenv('DB_DATABASE')+"")

file_name = "/media/abreufilho/HD - Abreu Filho/Shud/shud_spaces/crie2022/csv/inepescolas.csv"

df = pd.read_csv(file_name, sep=";")

df.to_sql("crie_escolas", con=engine, schema="public", if_exists="replace", index='id')