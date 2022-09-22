# Bibliotecas
import os
import dotenv
dotenv.load_dotenv()
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import inspect, create_engine
import requests
import zipfile
import boto3

session = boto3.session.Session()
client = session.client('s3', region_name='nyc3', endpoint_url='https://nyc3.digitaloceanspaces.com', aws_access_key_id=os.getenv('DO_SPACES_KEY'), aws_secret_access_key=os.getenv('DO_SPACES_SECRET'))


engine = create_engine("postgresql://"+os.getenv('DB_USERNAME')+":"+os.getenv('DB_PASSWORD')+"@"+os.getenv('DB_HOST')+":"+os.getenv('DB_PORT')+"/"+os.getenv('DB_DATABASE')+"")


def download_file(url, dest_path="/tmp/"):
    local_filename = url.split('/')[-1]
    final_file = dest_path+local_filename # igual nome /tmp/consulta_cand_2020.zip9
    if os.path.exists(final_file) != True:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(final_file, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return final_file
    else:
        return final_file

def convert_bytes(size):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0
    return size


# Get all csv files to dump to sql database



sections = [
    #{
        #"year":"2020",
        #"section_urls":[
       #     "https://shud01.nyc3.digitaloceanspaces.com/eleicoes/localidades/csv/BR_Zona_Secao_2020.csv",
      #      #"https://shud.nyc3.digitaloceanspaces.com/eleicoes/localidades/BR_Zona_Secao_2020.csv",
     #   ]
    #},
    #"/tmp/bweb_1t_MG_14102014133941.txt",
    # {
    #     "year":"2020",
    #     "section_urls":[
    #         #"https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2020.zip",
    #         "/tmp/consulta_cand_2020_MG.csv",
    #     ]
    # },
    {
        "year":"2018",
        "section_urls":[
            #"https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2018.zip",
            "/tmp/consulta_cand_2018_MG.csv",
        ]
    },
    #     {
    #     "year":"2016",
    #     "section_urls":[
    #         "https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2016.zip",
    #         "/tmp/consulta_cand_2016_MG.csv",
    #     ]
    # },
    #     {
    #     "year":"2014",
    #     "section_urls":[
    #         "https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2014.zip",
    #         "/tmp/consulta_cand_2014_MG.csv",
    #     ]
    # },
    #     {
    #     "year":"2012",
    #     "section_urls":[
    #         #"https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2012.zip",
    #         "/tmp/consulta_cand_2012_MG.csv",
    #     ]
    # },
]

uf = "MG"
batch_size=25000
isFirst = False if inspect(engine).has_table("sections", "public") else True
batches_processed = 0
rows_processed = 0
cols = {}

for candidate in sections:
    year = candidate["year"]
    for section_url in candidate["section_urls"]:
        # Download and unzip file
        downloaded = download_file(section_url)

        if section_url.endswith(".zip"):
            zf = zipfile.ZipFile(downloaded, 'r')
            zipFiles = zf.namelist()
            filename = ""
            for zipFile in zipFiles:
                if zipFile.endswith("MG.csv"):
                    filename = zipFile
        else:
            filename = downloaded
        if filename == "":
            print("NO VALID CSV FILE TO EXTRACT. SCRIPT CLOSED.", year, " - ", section_url)
        if os.path.exists("/tmp/"+filename) != True and filename.endswith(".zip"):
            zf.extract(filename, "/tmp/")
            zf.close()
            filename = "/tmp/"+filename

        # Read unzipped file

        chunks = pd.read_csv(filename, encoding="utf-8", sep=";", chunksize=batch_size, iterator=True)

        print("STARTING TO PROCESS CHUNKS...")


        # Parse each chunk
        for df in chunks:
            # Get columns of read file
            cols[year] = list(df)

            # Filter localidades by SG_UF
            df = df.loc[df['SG_UF'] == uf]

            # Create or append to table with data
            df.to_sql("sections", con=engine, schema="public", if_exists="replace" if isFirst else "append", index='id')

            print("CHUNK #", batches_processed, " - Rows added to DB: ", rows_processed, " - Year: ", year, " - Memory Usage (After): ", convert_bytes(df.memory_usage(deep=True).sum()), " - File: .../"+section_url.split('/')[-1], "...")
            rows_processed += len(df)
            batches_processed += 1
            isFirst = False
        # delete zip file and csv

        #TIREI O DELETE DO FILE

        # os.remove(filename)
        # if filename.endswith(".csv"):
        #     os.remove(downloaded)
