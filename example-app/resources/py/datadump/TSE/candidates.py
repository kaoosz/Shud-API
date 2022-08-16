# Arquivo de extração ao BD dos dados de candidatos por ano da eleição
# Candidatos - https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_vagas/consulta_vagas_2020.zip
# Bens de candidatos - https://cdn.tse.jus.br/estatistica/sead/odsele/bem_candidato/bem_candidato_2020.zip
# Coligações - https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_coligacao/consulta_coligacao_2020.zip
# Vagas - https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_vagas/consulta_vagas_2020.zip
# Fotos de candidatos - https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2020/fotos/foto_cand2020_{UF}_div.zip

# Baixar fotos dos candidatos, transformar todos ".jpg" em ".jpeg"
# Adicionar fotos de candidatos por eleicao por estado no Spaces
# Acessar foto do candidato por "/foto_cand2020_{UF}_div/F{UF}{SQ_CANDIDATO}_div.jpeg"

# Bibliotecas
import os
import dotenv
dotenv.load_dotenv()
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import inspect, create_engine
import zipfile

# cria um cliente de boto3 para baixar arquivos
from s3client import download_s3, convert_bytes

engine = create_engine("postgresql://"+os.getenv('DB_USERNAME')+":"+os.getenv('DB_PASSWORD')+"@"+os.getenv('DB_HOST')+":"+os.getenv('DB_PORT')+"/"+os.getenv('DB_DATABASE')+"")


# Get all csv files to dump to sql database
candidates = [
    {
        "year":"2020",
        "candidate_urls":[
            "https://shud01.nyc3.digitaloceanspaces.com/eleicoes/2020/candidatos/consulta_cand_2020.zip",
        ]
    },
    {
        "year":"2018",
        "candidate_urls":[
            "https://shud.nyc3.digitaloceanspaces.com/eleicoes/2018/candidatos/consulta_cand_2018.zip",
        ]
    },
    {
        "year":"2016",
        "candidate_urls":[
            "https://shud.nyc3.digitaloceanspaces.com/eleicoes/2016/candidatos/consulta_cand_2016.zip",
        ]
    },
    {
        "year":"2014",
        "candidate_urls":[
            "https://shud.nyc3.digitaloceanspaces.com/eleicoes/2014/candidatos/consulta_cand_2014.zip",
        ]
    },
    {
        "year":"2012",
        "candidate_urls":[
            "https://shud.nyc3.digitaloceanspaces.com/eleicoes/2012/candidatos/consulta_cand_2012.zip",
        ]
    },
]

uf = "MG"
batch_size=100000
isFirst = True
batches_processed = 0
rows_processed = 0
cols = {}

for bulletin in candidates:
    year = bulletin["year"]
    for bulletin_url in bulletin["candidate_urls"]:
        # Download and unzip file
        file_path = f"/tmp/{bulletin_url.split('/')[-1]}"
        download_s3(bulletin_url, file_path)
        zf = zipfile.ZipFile(file_path, 'r')
        zipFiles = zf.namelist()
        filename = ""
        for zipFile in zipFiles:
            if zipFile.endswith(".csv"):
                filename = zipFile
        if filename == "":
            print("NO VALID CSV FILE TO EXTRACT. SCRIPT CLOSED.", year, " - ", bulletin_url)
        if os.path.exists("/tmp/"+filename) != True:
            zf.extract(filename, "/tmp/")
            zf.close()
        filename = "/tmp/"+filename

        chunks = pd.read_csv(filename, encoding="latin1", sep=";", chunksize=batch_size, iterator=True, dtype={
            "NR_CPF_CANDIDATO":str,
            "SG_UE":str
        })

        print("STARTING TO PROCESS CHUNKS...")
        # Parse each chunk
        for df in chunks:
            # Get columns of read file
            cols[year] = list(df)

            # Filter localidades by NM_UE (2020)
            if year == "2020":
                df = df.loc[df['NM_UE'] == "BELO HORIZONTE"]
                df["PHOTO_URL"] = "https://shud01.nyc3.digitaloceanspaces.com/eleicoes/"+df["ANO_ELEICAO"].astype(str)+"/candidatos/fotos/foto_cand"+df["ANO_ELEICAO"].astype(str)+"_"+uf+"_div/F"+uf+df["SQ_CANDIDATO"].astype(str)+"_div.jpg"
            elif year == "2018":
                df = df.loc[df['NM_UE'] == "MINAS GERAIS"]
                df["PHOTO_URL"] = "https://shud01.nyc3.digitaloceanspaces.com/eleicoes/media/avatar_placeholder.jpg"
                if "QT_VOTOS" in list(df):
                    df["QT_VOTOS"] = 0
            # Drop all useless columns that are not mutually existent to keep disk space
            useless_columns = ["NM_TIPO_ELEICAO"]
            for col in useless_columns:
                if col not in list(df):
                    useless_columns.remove(col)
            df.drop(useless_columns, axis=1, inplace=True)

            # Create or append to table with data
            df.to_sql("candidates", con=engine, schema="public", if_exists="replace" if isFirst else "append", index='id')
            print("CHUNK #", batches_processed, " - Rows added to DB: ", rows_processed, " - Year: ", year, " - Memory Usage (After): ", convert_bytes(df.memory_usage(deep=True).sum()), " - File: .../"+bulletin_url.split('/')[-1], "...")
            rows_processed += len(df)
            batches_processed += 1
            isFirst = False
        # delete zip file and csv
        os.remove(filename)
        os.remove(file_path)
