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

# Read CSV file
files = [
    "/tmp/consulta_cand_2020_MG.csv",
    #"/tmp/consulta_cand_2018_MG.csv",

    #"/tmp/consulta_cand_2016_MG.csv", # error
    #"/tmp/consulta_cand_2014_MG.csv",
    #"/tmp/consulta_cand_2012_MG.csv", # error

    # "/media/abreufilho/HD - Abreu Filho/Shud/shud_spaces/eleicoes/2020/candidatos/consulta_cand_2020/consulta_cand_2020_BRASIL.csv",
    # "/media/abreufilho/HD - Abreu Filho/Shud/shud_spaces/eleicoes/2018/candidatos/consulta_cand_2018/consulta_cand_2018_BRASIL.csv",
    # "/media/abreufilho/HD - Abreu Filho/Shud/shud_spaces/eleicoes/2016/candidatos/consulta_cand_2016/consulta_cand_2016_BRASIL.csv",
    # "/media/abreufilho/HD - Abreu Filho/Shud/shud_spaces/eleicoes/2014/candidatos/consulta_cand_2014/consulta_cand_2014_BRASIL.csv",
    # "/media/abreufilho/HD - Abreu Filho/Shud/shud_spaces/eleicoes/2012/candidatos/consulta_cand_2012/consulta_cand_2012_BRASIL.csv",

    #"eleicoes/2020/candidatos/consulta_cand_2020/consulta_cand_2020_BRASIL.csv",
    #"eleicoes/2018/candidatos/consulta_cand_2018/consulta_cand_2018_BRASIL.csv",
    #"eleicoes/2016/candidatos/consulta_cand_2016/consulta_cand_2016_BRASIL.csv",
    #"eleicoes/2014/candidatos/consulta_cand_2014/consulta_cand_2014_BRASIL.csv",
    #"eleicoes/2012/candidatos/consulta_cand_2012/consulta_cand_2012_BRASIL.csv",
]

firstRound = True

for file_s3_path in files:
    #BACK WHEN TEMPORARY IS GONE
    #file_name = "/tmp/"+file_s3_path.split("/")[-1]
    #print("Processing file", file_s3_path, file_name, "...")
    #client.download_file('shud01', file_s3_path, file_name)
    #print("Download finished", file_s3_path, file_name, "!")
    #/BACK WHEN TEMPORARY IS GONE

    #TEMPORARY
    file_name = file_s3_path
    print(file_name)
    #/TEMPORARY

    df = pd.read_csv(file_name, encoding="latin1", sep=";",
        dtype={
            "NR_CPF_CANDIDATO":str,
            "SG_UE":str,
            "NR_PROCESSO":str,
            "NM_SOCIAL_CANDIDATO":str,
        },
        parse_dates=[["DT_GERACAO", "HH_GERACAO"], "DT_NASCIMENTO", "DT_ELEICAO"],
        #nrows=1000,
    )

    cols = list(df)

    df = df.loc[df["SG_UF"].isin(["MG"])]

    cols_to_upper = ["NM_COLIGACAO", "DS_ELEICAO", "DS_SITUACAO_CANDIDATO_URNA", "DS_DETALHE_SITUACAO_CAND", "DS_SITUACAO_CANDIDATO_PLEITO"]
    for col_to_upper in cols_to_upper:
        if col_to_upper in cols:
            df[col_to_upper] = df[col_to_upper].str.upper()

    df["NR_CPF_CANDIDATO"] = df['NR_CPF_CANDIDATO'].apply(lambda x: x.zfill(11))
    df["ST_REELEICAO"] = (df["ST_REELEICAO"] == 'S').astype('bool')
    df["ST_DECLARAR_BENS"] = (df["ST_DECLARAR_BENS"] == 'S').astype('bool')
    df["ST_CANDIDATO_INSERIDO_URNA"] = (df["ST_CANDIDATO_INSERIDO_URNA"] == 'SIM').astype('bool')
    df["SG_UE"] = df["SG_UE"].str.lstrip('0')
    df = df.apply(lambda x: x.str.strip() if isinstance(x, str) else x).replace('#NULO#', np.nan)
    df = df.apply(lambda x: x.str.strip() if isinstance(x, str) else x).replace('#NULO', np.nan)
    df = df.apply(lambda x: x.str.strip() if isinstance(x, str) else x).replace('#NE#', np.nan)

    # Dicionário de colunas e descrições feitos a partir do leiame.pdf fornecido pelo TSE.
    # Dicionário dos candidatos no ano de 2020
    columns_dict = {
        "candidates" : {
            "DT_GERACAO" : "Data da extração dos dados para geração do arquivo.",
            "HH_GERACAO" : "Hora da extração dos dados para geração do arquivo com base no horário de Brasília.",
            "ANO_ELEICAO" : "Ano de referência da eleição para geração do arquivo. Observação: Para eleições suplementares o ano de referência da eleição é o da eleição ordinária correspondente. Por exemplo: Em 2016 houve eleições ordinárias. Após a data desta eleição ordinária e antes da próxima, houve eleições suplementares em 2017, 2018 e 2019. As informações destas eleições suplementares estarão divulgadas no arquivo gerado para as Eleições 2016.",
            "CD_TIPO_ELEICAO" : "Código do tipo de eleição. Pode assumir os valores: 1 - Eleição Suplementar, 2 - Eleição Ordinária e 3 - Consulta Popular.",
            "NM_TIPO_ELEICAO" : "Nome do tipo de eleição. Observação: As eleições ordinárias são previstas em Lei, possuem data certa para serem realizadas, ocorrem em anos pares e possuem a periodicidade de 04 em 04 anos. Nas eleições ordinárias nacionais são eleitos os cargos de Presidente, Governadores, Deputados (Federais e Estaduais) e Senadores. Nas eleições ordinárias municipais são eleitos os cargos de Prefeito e Vereadores. As eleições suplementares são aquelas que não têm periodicidade pré-determinada ou definida e ocorrem quando, eventualmente, se fizerem necessárias. As consultas populares ocorrem sempre que a população é convocada a opinar diretamente sobre um assunto específico e importante. Ela pode ser realizada de duas formas: plebiscito (quando o cidadão opina previamente sobre a possível criação de uma lei) e referendo (quando uma lei aprovada por um órgão legislativo é submetida à aceitação ou não dos eleitores).",
            "NR_TURNO" : "Número do turno da eleição. Observação: No Brasil, as eleições realizam-se por meio de dois sistemas: o sistema majoritário (aplicado aos cargos de Presidente, Vice- Presidente, Governador, Vice-Governador, Prefeito, Vice-Prefeito e Senador) e o sistema proporcional (aplicado aos cargos de Deputado Federal, Deputado Estadual, Deputado Distrital e Vereador). O sistema majoritário consiste em declarar eleito o candidato que tenha recebido a maioria dos votos válidos (excluídos os votos em brancos e os votos nulos). Caso o candidato ao cargo indicado no sistema majoritário, com exceção do cargo de Senador, não alcance maioria absoluta destes votos válidos no primeiro turno (mínimo de 50% + 1), haverá segundo turno em que concorrerão apenas os dois candidatos mais votados. O segundo turno das eleições no Brasil ocorre para os cargos de Presidente, Vice-Presidente da República, Governadores e Vice-Governadores dos Estados e do Distrito Federal e para Prefeitos e Vice-Prefeitos de Municípios com mais de 200 mil eleitores. Nos municípios cujo eleitorado é igual ou menor que 200 mil e para o cargo de Senador elege-se o candidato que tenha alcançado a maioria simples dos votos.",
            "CD_ELEICAO" : "Código único da eleição no âmbito da Justiça Eleitoral. Observação: Este código é único por eleição e por turno, ou seja, cada turno possui seu código de eleição.",
            "DS_ELEICAO" : "Descrição da eleição.",
            "DT_ELEICAO" : "Data em que ocorreu a eleição.",
            "TP_ABRANGENCIA" : "Abrangência da eleição. Pode assumir os valores: Municipal, Estadual e Federal. Observação: A abrangência territorial da eleição está diretamente relacionada aos cargos eletivos e suas circunscrições eleitorais. As eleições realizadas na circunscrição Municipal são as eleições para os cargos de Prefeito, Vice-Prefeito e Vereador; as realizadas na circunscrição Estadual são para os cargos de Governador, Vice-Governador, Senador, Deputado Estadual, Deputado Federal e Deputado Distrital e; as realizadas na circunscrição Federal são para os cargos de Presidente e Vice-Presidente da República.",
            "SG_UF" : "Sigla da Unidade da Federação em que ocorreu a eleição.",
            "SG_UE" : "Sigla da Unidade Eleitoral em que o candidato concorre na eleição. A Unidade Eleitoral representa a Unidade da Federação ou o Município em que o candidato concorre na eleição e é relacionada à abrangência territorial desta candidatura. Em caso de abrangência Federal (cargo de Presidente e Vice-Presidente) a sigla é BR. Em caso de abrangência Estadual (cargos de Governador, Vice-Governador, Senador, Deputado Federal, Deputado Estadual e Deputado Distrital) a sigla é a UF da candidatura. Em caso de abrangência Municipal (cargos de Prefeito, Vice-Prefeito e Vereador) é o código de identificação do município da candidatura.",
            "NM_UE" : "Nome da Unidade Eleitoral do candidato. Em caso de abrangência nacional é igual à 'Brasil'. Em caso de abrangência estadual é o nome da UF em que o candidato concorre. Em caso de abrangência municipal é o nome do município em que o candidato concorre.",
            "CD_CARGO" : "Código do cargo ao qual o candidato concorre na eleição.",
            "DS_CARGO" : "Cargo ao qual o candidato concorre na eleição.",
            "SQ_CANDIDATO" : "Número sequencial do candidato, gerado internamente pelos sistemas eleitorais para cada eleição. Observação: não é o número de campanha do candidato.",
            "NR_CANDIDATO" : "Número do candidato na urna.",
            "NM_CANDIDATO" : "Nome completo do candidato.",
            "NM_URNA_CANDIDATO" : "Nome do candidato que aparece na urna.",
            "NM_SOCIAL_CANDIDATO" : "Nome social do candidato. Observação: Nome social é o nome pelo qual pessoas travestir ou transexuais preferem ser chamadas cotidianamente, em contraste com o nome oficialmente registrado, que não reflete sua identidade de gênero. A identidade do nome social é vinculada com a identidade civil original. Em âmbito federal, o Decreto nº 8.727 de 2016, garante o direito ao uso do nome social e reconhecimento da identidade de gênero de pessoas travestis e transexuais no âmbito da administração pública federal direta, autárquica e fundacional.",
            "NR_CPF_CANDIDATO" : "Número do CPF do candidato.",
            "NM_EMAIL" : "Endereço de e-mail do candidato.",
            "CD_SITUACAO_CANDIDATURA" : "Código da situação do registro de candidatura do candidato.",
            "DS_SITUACAO_CANDIDATURA" : "Situação do registro da candidatura do candidato. Pode assumir os valores: Apto (candidato apto para ir para urna), Inapto (candidato inapto para ir para urna) e Cadastrado (registro de candidatura realizado, mas ainda não julgado). A situação inicial de uma candidatura é 'Cadastrado'. Após julgamento pela Justiça Eleitoral, a situação é alterada para 'Apto' ou 'Inapto' com relação ao encaminhamento da candidatura para a urna.",
            "CD_DETALHE_SITUACAO_CAND" : "Código do detalhe da situação do registro de candidatura do candidato.",
            "DS_DETALHE_SITUACAO_CAND" : "Detalhe da situação do registro de candidatura do candidato que especifica o motivo pelo qual a candidatura foi julgada como 'Apta' ou 'Inapta'.",
            "TP_AGREMIACAO" : "Tipo de agremiação da candidatura do candidato, ou seja, forma como o candidato concorrerá nas eleições. Pode assumir os valores: Coligação (quando o candidato concorre por coligação) e Partido Isolado (quando o candidato concorre somente pelo partido).",
            "NR_PARTIDO" : "Número do partido de origem do candidato. Mesmo que o candidato participe de uma coligação, este número é o número do seu partido de origem.",
            "SG_PARTIDO" : "Sigla do partido de origem do candidato.",
            "NM_PARTIDO" : "Nome do partido de origem do candidato.",
            "SQ_COLIGACAO" : "Sequencial da coligação da qual o candidato pertence, gerado pela Justiça Eleitoral.",
            "NM_COLIGACAO" : "Nome da coligação da qual o candidato pertence.",
            "DS_COMPOSICAO_COLIGACAO" : "Composição da coligação da qual o candidato pertence. Observação: Coligação é a união de dois ou mais partidos a fim de disputarem eleições. A informação da coligação no arquivo está composta pela concatenação das siglas dos partidos intercarladas com o símbolo /.",
            "CD_NACIONALIDADE" : "Código da nacionalidade do candidato.",
            "DS_NACIONALIDADE" : "Nacionalidade do candidato.",
            "SG_UF_NASCIMENTO" : "Sigla da Unidade da Federação de nascimento do candidato.",
            "CD_MUNICIPIO_NASCIMENTO" : "Código de identificação do município de nascimento do candidato.",
            "DT_NASCIMENTO" : "Data de nascimento do candidato.",
            "NR_IDADE_DATA_POSSE" : "Idade do candidato na data da posse. A idade é calculada com base na data da posse do referido candidato para o cargo e unidade eleitoral constantes no arquivo de vagas.",
            "NR_TITULO_ELEITORAL_CANDIDATO" : "Número do título eleitoral do candidato.",
            "CD_GENERO" : "Código do gênero do candidato.",
            "DS_GENERO" : "Gênero do candidato.",
            "CD_GRAU_INSTRUCAO" : "Código do grau de instrução do candidato.",
            "DS_GRAU_INSTRUCAO" : "Grau de instrução do candidato.",
            "CD_ESTADO_CIVIL" : "Código do estado civil do candidato.",
            "DS_ESTADO_CIVIL" : "Estado civil do candidato.",
            "CD_COR_RACA" : "Código da cor/raça do candidato. (autodeclaração)",
            "CD_OCUPACAO" : "Código da ocupação do candidato.",
            "DS_OCUPACAO" : "Ocupação do candidato.",
            "VR_DESPESA_MAX_CAMPANHA" : "Valor máximo, em reais, de despesas de campanha declarada pelo partido para aquele candidato.",
            "CD_SIT_TOT_TURNO" : "Código da situação de totalização do candidato, naquele turno da eleição, após a totalização dos votos.",
            "DS_SIT_TOT_TURNO" : "Situação de totalização do candidato, naquele turno da eleição, após a totalização dos votos.",
            "ST_REELEICAO" : "Indica se o candidato está concorrendo ou não à reeleição. Pode assumir os valores: S - Sim e N - Não. Informação autodeclarada pelo candidato. Observação: Reeleição é a renovação do mandato para o mesmo cargo eletivo, por mais um período, na mesma circunscrição eleitoral na qual o representante, no pleito imediatamente anterior, se elegeu. Pelo sistema eleitoral brasileiro, o presidente da República, os governadores de estado e os prefeitos podem ser reeleitos para um único período subsequente, o que se aplica também ao vice-presidente da República, aos vice-governadores e aos vice-prefeitos. Já os parlamentares (senadores, deputados federais e estaduais/distritais e vereadores) podem se reeleger ilimitadas vezes. A possibilidade da reeleição compreende algumas regras mais específicas detalhadas no sistema eleitoral brasileiro.",
            "ST_DECLARAR_BENS" : "Indica se o candidato tem ou não bens a declarar. Pode assumir os valores: S - Sim e N - Não. Esta informação é fornecida pelo próprio candidato no momento do pedido da candidatura.",
            "NR_PROTOCOLO_CANDIDATURA" : "Número do protocolo de registro de candidatura do candidato.",
            "NR_PROCESSO" : "Número do processo de registro de candidatura do candidato.",
            "CD_SITUACAO_CANDIDATO_PLEITO" : "Código da situação da candidatura no dia do Pleito.",
            "DS_SITUACAO_CANDIDATO_PLEITO" : "Situação da candidatura no dia do Pleito.",
            "CD_SITUACAO_CANDIDATO_URNA" : "Código da situação da candidatura na urna.",
            "DS_SITUACAO_CANDIDATO_URNA" : "Situação da candidatura na urna.",
            "ST_CANDIDATO_INSERIDO_URNA" : "Informa se o candidato foi inserido na urna eletrônica. (S/N)",
        }
    }

    df.to_sql("candidates", con=engine, schema="public", if_exists='replace' if firstRound else 'append', index=None,
        dtype={
            'ST_REELEICAO': sqlalchemy.types.Boolean,
            'ST_DECLARAR_BENS': sqlalchemy.types.Boolean,
            'ST_CANDIDATO_INSERIDO_URNA': sqlalchemy.types.Boolean,
            "NM_SOCIAL_CANDIDATO":sqlalchemy.types.String,
        }
    )
    if firstRound:
        firstRound = False

    # delete file
    #os.remove(file_name)

# adiciona coluna id com numeros incrementais
df = pd.read_sql_table("candidates", con=engine, schema="public")
df.to_sql("candidates", con=engine, schema="public", if_exists='replace', index="id")
