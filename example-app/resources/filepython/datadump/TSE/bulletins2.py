# Os arquivos de dump no banco devem ser executados em uma máquina com bastante memoria RAM e inseridos à DB remota a partir da engine correta.

# Bibliotecas
import os
import dotenv
dotenv.load_dotenv()
import pandas as pd
import sqlalchemy
import numpy as np
import boto3

session = boto3.session.Session()
client = session.client('s3', region_name='nyc3', endpoint_url='https://nyc3.digitaloceanspaces.com', aws_access_key_id=os.getenv('DO_SPACES_KEY'), aws_secret_access_key=os.getenv('DO_SPACES_SECRET'))

#engine = create_engine("postgresql://"+os.getenv('DB_USERNAME')+" : "+os.getenv('REMOTE_PSQL_PASSWORD')+"@"+os.getenv('REMOTE_PSQL_IP')+" : "+os.getenv('DB_PORT')+"/"+os.getenv('DB_DATABASE')+"")
engine = sqlalchemy.create_engine("postgresql://"+os.getenv('DB_USERNAME')+":"+os.getenv('DB_PASSWORD')+"@"+os.getenv('DB_HOST')+":"+os.getenv('DB_PORT')+"/"+os.getenv('DB_DATABASE')+"")

pd.set_option("display.max_columns", None)

# Read CSV files
files = {
    # "2020":{
    #     "files":[
    #         #"/tmp/",
    #         "/tmp/bweb_1t_MG_181120201549.csv",
    #         #"/media/abreufilho/HD - Abreu Filho/Shud/shud_spaces/eleicoes/2020/resultados/boletins_urna/1_turno/bweb_1t_MG_181120201549.csv",
    #         #"/media/abreufilho/HD - Abreu Filho/Shud/shud_spaces/eleicoes/2020/resultados/boletins_urna/2_turno/bweb_2t_MG_301120201245.csv",
    #     ]
    # },

    # "2018":{
    #     "files":[
    #         "/tmp/bweb_1t_MG_101020181954.csv",
    #         #"/media/abreufilho/HD - Abreu Filho/Shud/shud_spaces/eleicoes/2018/resultados/boletins_urna/2_turno/bweb_2t_MG_301020181749.csv"
    #     ]
    # },

    # "2016":{
    #     "col_names":["DT_GERACAO", "HH_GERACAO", "CD_PLEITO", "CD_ELEICAO", "SG_UF", "CD_CARGO_PERGUNTA", "DS_CARGO_PERGUNTA", "NR_ZONA", "NR_SECAO", "NR_LOCAL_VOTACAO", "NR_PARTIDO", "SG_PARTIDO", "CD_MUNICIPIO", "NM_MUNICIPIO", "DT_BU_RECEBIDO", "QT_APTOS", "QT_ABSTENCOES", "QT_COMPARECIMENTO", "CD_TIPO_ELEICAO", "CD_TIPO_URNA", "DS_TIPO_URNA", "NR_VOTAVEL", "NM_VOTAVEL", "QT_VOTOS", "CD_TIPO_VOTAVEL", "NR_URNA_EFETIVADA", "CD_CARGA_1_URNA_EFETIVADA", "CD_CARGA_2_URNA_EFETIVADA", "DT_CARGA_URNA_EFETIVADA", "CD_FLASHCARD_URNA_EFETIVADA", "DS_CARGO_PERGUNTA_SECAO"],
    #     "files":[
    #         "/tmp/bweb_1t_MG_04102016184853.txt",
    #         #"/media/abreufilho/HD - Abreu Filho/Shud/shud_spaces/eleicoes/2016/resultados/boletins_urna/2_turno/bweb_2t_MG_31102016133815.txt"
    #     ]
    # },

    "2014":{
        "col_names":["DT_GERACAO", "HH_GERACAO", "CD_PLEITO", "CD_ELEICAO", "SG_UF", "CD_CARGO_PERGUNTA", "DS_CARGO_PERGUNTA", "NR_ZONA", "NR_SECAO", "NR_LOCAL_VOTACAO", "NR_PARTIDO", "SG_PARTIDO", "CD_MUNICIPIO", "NM_MUNICIPIO", "DT_BU_RECEBIDO", "QT_APTOS", "QT_ABSTENCOES", "QT_COMPARECIMENTO", "CD_TIPO_ELEICAO", "CD_TIPO_URNA", "DS_TIPO_URNA", "NR_VOTAVEL", "NM_VOTAVEL", "QT_VOTOS", "CD_TIPO_VOTAVEL", "NR_URNA_EFETIVADA", "CD_CARGA_1_URNA_EFETIVADA", "CD_CARGA_2_URNA_EFETIVADA", "DT_CARGA_URNA_EFETIVADA", "CD_FLASHCARD_URNA_EFETIVADA", "DS_CARGO_PERGUNTA_SECAO"],
        "files":[
            "/tmp/bweb_1t_MG_14102014133941.txt",
            #"/media/abreufilho/HD - Abreu Filho/Shud/shud_spaces/eleicoes/2014/resultados/boletins_urna/2_turno/bweb_2t_MG_28102014122730.txt"
        ]
    },

    "2012":{
        "col_names":["DT_GERACAO", "HH_GERACAO", "CD_PLEITO", "CD_ELEICAO", "SG_UF", "CD_CARGO_PERGUNTA", "DS_CARGO_PERGUNTA", "NR_ZONA", "NR_SECAO", "NR_LOCAL_VOTACAO", "NR_PARTIDO", "SG_PARTIDO", "CD_MUNICIPIO", "NM_MUNICIPIO", "DT_BU_RECEBIDO", "QT_APTOS", "QT_ABSTENCOES", "QT_COMPARECIMENTO", "CD_TIPO_ELEICAO", "ORIGEM", "CD_TIPO_URNA", "DS_TIPO_URNA", "NR_VOTAVEL", "NM_VOTAVEL", "QT_VOTOS", "CD_TIPO_VOTAVEL", "NR_URNA_EFETIVADA", "CD_CARGA_1_URNA_EFETIVADA", "CD_CARGA_2_URNA_EFETIVADA", "DT_CARGA_URNA_EFETIVADA", "CD_FLASHCARD_URNA_EFETIVADA", "DS_CARGO_PERGUNTA_SECAO"],
        "files":[
            "/tmp/bweb_1t_MG_10102012014547.txt",
            #"/media/abreufilho/HD - Abreu Filho/Shud/shud_spaces/eleicoes/2012/resultados/boletins_urna/2_turno/bweb_2t_MG_30102012172126.txt"
        ]
    }
}


batch_size=100000
isFirst = True
batches_processed = 0
rows_processed = 0
cols = []

for year in files:
    for file_s3_path in files[year]["files"]:
        if "col_names" in files[year]:
            col_names = files[year]["col_names"]
            line_with_headers = ';'.join(f'"{w}"' for w in col_names)
            get_df_date_cols = list(pd.read_csv(file_s3_path, encoding="latin1", sep=";", nrows=2))
            if (get_df_date_cols[0] != 'DT_GERACAO'):
                os.system('sed -i 1i\''+line_with_headers+'\' '+file_s3_path.replace(" ", "\ "))
        else:
            col_names = None

        #BACK WHEN TEMPORARY IS GONE
        #file_name = "/tmp/"+file_s3_path.split("/")[-1]
        #print("Processing file", file_s3_path, file_name, "...")
        #client.download_file('shud01', file_s3_path, file_name)
        #print("Download finished", file_s3_path, file_name, "!")
        #/BACK WHEN TEMPORARY IS GONE

        #TEMPORARY
        file_name = file_s3_path
        #/TEMPORARY

        get_df_date_cols = list(pd.read_csv(file_name, encoding="latin1", sep=";", nrows=2))

        date_cols = list(set(get_df_date_cols) & set(["DT_BU_RECEBIDO", "DT_CARGA_URNA_EFETIVADA", "DT_ABERTURA", "DT_ENCERRAMENTO", "DT_EMISSAO_BU", "DT_PLEITO"]))
        date_cols.append(["DT_GERACAO", "HH_GERACAO"])

        chunks = pd.read_csv(file_name, encoding="latin1", sep=";", chunksize=batch_size, iterator=True, index_col=False,
            dtype={
                "NR_PARTIDO":str,
                "DS_AGREGADAS":str,
                "NR_JUNTA_APURADORA":str,
                "NR_TURMA_APURADORA":str,
                "CD_FLASHCARD_URNA_EFETIVADA":str,
                "DS_TIPO_URNA":str,
                "DS_CARGO_PERGUNTA":str,
                "CD_CARGA_1_URNA_EFETIVADA":str,
                "CD_CARGA_2_URNA_EFETIVADA":str,

            },
            parse_dates=date_cols,

            #nrows=1000,
        )

        print("STARTING TO PROCESS CHUNKS...\n")
        # Parse each chunk
        for df in chunks:
            # Get columns of read file
            cols = list(df)

            # Parse each column and check if it exists, if not, remove from cols_to_rename
            cols_to_rename = {
                'DT_ELEICAO':'DT_PLEITO', # Coluna DT_ELEICAO foi mudada para DT_PLEITO em 2020
                'CD_FLASCARD_URNA_EFETIVADA':'CD_FLASHCARD_URNA_EFETIVADA', # Typo na coluna CD_FLASHCARD_URNA_EFETIVADA nos boletins de 2018
                "SG_ UF":"SG_UF" # Typo na coluna SG_UF
            }
            cols_in_cols_to_rename = [item for item in cols_to_rename if item not in cols]
            for wrong_col in cols_in_cols_to_rename:
                del cols_to_rename[wrong_col]
            if len(cols_to_rename) > 0:
                df = df.rename(columns=cols_to_rename)

            # Get columns of read file after cleansing
            cols = list(df)

            for col_to_drop in ["NR_JUNTA_APURADORA", "NR_TURMA_APURADORA", "DS_CARGO_PERGUNTA_SECAO", "ORIGEM"]:
                if col_to_drop in cols:
                    df.drop([col_to_drop], axis=1, inplace=True)

            cols_to_upper = ["NM_TIPO_ELEICAO", "DS_TIPO_VOTAVEL", "DS_TIPO_URNA", "DS_ELEICAO", "DS_CARGO_PERGUNTA", "NM_PARTIDO", "NM_VOTAVEL"]
            for col_to_upper in cols_to_upper:
                if col_to_upper in cols:
                    df[col_to_upper] = df[col_to_upper].str.upper()

            df['NR_PARTIDO'] = df['NR_PARTIDO'].replace('#NULO#','-1', regex=True)
            df["NR_PARTIDO"] = pd.to_numeric(df["NR_PARTIDO"])
            df = df.apply(lambda x: x.str.strip() if isinstance(x, str) else x).replace('#NULO#', np.nan)
            df = df.apply(lambda x: x.str.strip() if isinstance(x, str) else x).replace('#NULO', np.nan)
            df = df.apply(lambda x: x.str.strip() if isinstance(x, str) else x).replace('#NE#', np.nan)

            # Create or append to table with data
            df.to_sql("bulletins_"+year, con=engine, schema="public", if_exists="append" if isFirst else "append", index='id')
            rows_processed += len(df)
            batches_processed += 1
            isFirst = False
            print("CHUNK #", batches_processed, " - Rows added to DB: ", len(df), " - Total rows until now: ", rows_processed)
        # delete file
        #BACK WHEN TEMPORARY IS GONE
        #os.remove(file_name)
        #/BACK WHEN TEMPORARY IS GONE
