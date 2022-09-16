# Boletins de urnas
# Boletim de urna AC 1 turno - https://cdn.tse.jus.br/eleicoes2020/buweb/bweb_1t_AC_181120201549.zip
# Boletim de urna AC 2 turno - https://cdn.tse.jus.br/eleicoes2020/buweb/bweb_2t_AC_301120201245.zip
# Cargo em 2020 é "DS_CARGO" e em 2018 é "DS_CARGO_PERGUNTA"

# Bibliotecas
import os
import dotenv
dotenv.load_dotenv()
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine
import zipfile

# cria um cliente de boto3 para baixar arquivos
from s3client import download_s3, convert_bytes

engine = create_engine("postgresql://"+os.getenv('DB_USERNAME')+":"+os.getenv('DB_PASSWORD')+"@"+os.getenv('DB_HOST')+":"+os.getenv('DB_PORT')+"/"+os.getenv('DB_DATABASE')+"")

# Get all csv files to dump to sql database
bulletins = [
    {
        "year":"2020",
        "bulletin_urls":[
            "eleicoes/2020/resultados/boletins_urna/1_turno/bweb_1t_MG_181120201549.zip",
        ]
    },
    {
        "year":"2018",
        "bulletin_urls":[
            "eleicoes/2018/resultados/boletins_urna/1_turno/BWEB_1t_MG_101020181938.zip",
        ]
    },
    {
        "year":"2016",

        "bulletin_urls":[
            "eleicoes/2016/resultados/boletins_urna/1_turno/bweb_1t_MG_04102016184853.zip",
        ]
    },
    {
        "year":"2014",
        "bulletin_urls":[
            "eleicoes/2014/resultados/boletins_urna/1_turno/bweb_1t_MG_14102014133941.zip",
        ]
    },
    {
        "year":"2012",
        "bulletin_urls":[
            "eleicoes/2012/resultados/boletins_urna/1_turno/bweb_1t_MG_10102012014547.zip",
        ]
    },
]

batch_size=25000
isFirst = True
batches_processed = 0
rows_processed = 0
cols = {}

for bulletin in bulletins:
    year = bulletin["year"]
    for bulletin_url in bulletin["bulletin_urls"]:
        # Download and unzip file
        file_path = f"/tmp/{bulletin_url.split('/')[-1]}"
        download_s3(bulletin_url, file_path)
        zf = zipfile.ZipFile(file_path, 'r')
        zipFiles = zf.namelist()
        filename = ""
        for zipFile in zipFiles:
            if zipFile.endswith(".csv"):
                filename = zipFile
            elif zipFile.endswith(".txt") and "_MG_" in zipFile:
                filename = zipFile
        if filename == "":
            print("NO VALID CSV FILE TO EXTRACT. SCRIPT CLOSED.", year, " - ", bulletin_url)
        if os.path.exists("/tmp/"+filename) != True:
            zf.extract(filename, "/tmp/")
            zf.close()
        #



        filename = "/tmp/"+filename

        chunks = pd.read_csv(filename, nrows=200000, encoding="latin1", sep=";", chunksize=batch_size, iterator=True, dtype={
            "NR_PARTIDO":str,
            "DS_AGREGADAS":str,
            "NR_JUNTA_APURADORA":str,
            "NR_TURMA_APURADORA":str,
            "CD_FLASHCARD_URNA_EFETIVADA":str,
        })

        print("STARTING TO PROCESS CHUNKS...")
        # Parse each chunk
        #HERE
        for df in chunks:
            # Get columns of read file
            cols[year] = list(df)

            # Parse each column and check if it exists, if not, remove from cols_to_rename
            cols_to_rename = {
                'DT_ELEICAO':'DT_PLEITO', # Coluna DT_ELEICAO foi mudada para DT_PLEITO em 2020
                'CD_FLASCARD_URNA_EFETIVADA':'CD_FLASHCARD_URNA_EFETIVADA', # Typo na coluna CD_FLASHCARD_URNA_EFETIVADA nos boletins de 2018
                "SG_ UF":"SG_UF" # Typo na coluna SG_UF
            }
            cols_in_cols_to_rename = [item for item in cols_to_rename if item not in cols[year]]
            for wrong_col in cols_in_cols_to_rename:
                del cols_to_rename[wrong_col]
            if len(cols_to_rename) > 0:
                df = df.rename(columns=cols_to_rename)

            # Get columns of read file after cleansing
            cols[year] = list(df)

            # Remove all "#NULO#" values from NR_PARTIDO and convert to number
            #df['NR_PARTIDO'] = df['NR_PARTIDO'].replace('#NULO#','-1', regex=True)
            #df["NR_PARTIDO"] = pd.to_numeric(df["NR_PARTIDO"])

            # Create or append to table with data
            df.to_sql("bulletins", con=engine, schema="public", if_exists="replace" if isFirst else "append", index='id')
            print("CHUNK #", batches_processed, " - Rows added: ", rows_processed, " - Year: ", year, " - Mem Usage: ", convert_bytes(df.memory_usage(deep=True).sum()), " - File: .../"+bulletin_url.split('/')[-1], "...")
            rows_processed += len(df)
            batches_processed += 1
            isFirst = False
        #     #HERE
    # delete zip file and csv
    #os.remove(filename)
    #os.remove(file_path)
