import os
from urllib import request
import json

unzip_files = True

ufs = ['AC','AL','AP','AM','BA','CE','ES','GO','MA','MS','MT','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']
#ufs = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MS','MT','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']

files = {
    "eleicoes/2020/candidatos/":[
        "https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2020.zip", #Candidatos (formato ZIP)
        "https://cdn.tse.jus.br/estatistica/sead/odsele/bem_candidato/bem_candidato_2020.zip", #Bens de candidatos (formato ZIP)
        "https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_coligacao/consulta_coligacao_2020.zip", #Coligações (formato ZIP)
        "https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_vagas/consulta_vagas_2020.zip", #Vagas (formato ZIP)
        "https://cdn.tse.jus.br/estatistica/sead/odsele/motivo_cassacao/motivo_cassacao_2020.zip", #Motivo da cassação (formato ZIP)
        "https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/rede_social_candidato_2020.zip", #Redes sociais de candidatos (formato ZIP)
    ],
    "eleicoes/2020/candidatos/fotos/":[
        "https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2020/fotos/foto_cand2020_{UF}_div.zip", #Fotos de candidatos
    ],
    "eleicoes/2020/candidatos/proposta_gov/":[
        "https://cdn.tse.jus.br/estatistica/sead/odsele/proposta_governo/proposta_governo_2020_{UF}.zip", #Proposta de governo
    ],
    "eleicoes/2020/comparecimento_abstencao/":[
        "https://cdn.tse.jus.br/estatistica/sead/odsele/perfil_comparecimento_abstencao/perfil_comparecimento_abstencao_2020.zip", #Comparecimento e Abstenção
        "https://cdn.tse.jus.br/estatistica/sead/odsele/perfil_comparecimento_abstencao_eleitor_deficiente/perfil_comparecimento_abstencao_eleitor_deficiente_2020.zip", #Pessoas com deficiência
        "https://cdn.tse.jus.br/estatistica/sead/odsele/perfil_comparecimento_abstencao_eleitor_tte/perfil_comparecimento_abstencao_eleitor_tte_2020.zip", #Transferência temporária de eleitor
    ],
    "eleicoes/2020/eleitorado/":[
        "https://cdn.tse.jus.br/estatistica/sead/odsele/perfil_eleitorado/perfil_eleitorado_2020.zip", #Eleitorado 2020 (formato ZIP)
        "https://cdn.tse.jus.br/estatistica/sead/odsele/perfil_eleitor_deficiente/perfil_eleitor_deficiencia_2020.zip", #Perfil do Eleitorado com deficiência 2020 (formato ZIP)
        "https://cdn.tse.jus.br/estatistica/sead/odsele/eleitorado_locais_votacao/eleitorado_local_votacao_2020.zip", #Eleitorado por local de votação
    ],
    "eleicoes/2020/eleitorado/perfil_secao/":[
        "https://cdn.tse.jus.br/estatistica/sead/odsele/perfil_eleitor_secao/perfil_eleitor_secao_2020_{UF}.zip", #Perfil do eleitorado por seção eleitoral
    ],
    "eleicoes/2020/partidos/":[
        "https://cdn.tse.jus.br/estatistica/sead/odsele/delegado_partidario/delegado_partidario.zip", #Delegados Partidários
        "https://cdn.tse.jus.br/estatistica/sead/odsele/orgao_partidario/orgao_partidario.zip", #Órgãos Partidários
        "https://cdn.tse.jus.br/estatistica/sead/odsele/filiacao_partidaria/perfil_filiacao_partidaria.zip", #Perfil Filiação Partidária
    ],
    "eleicoes/2020/mesarios/":[
        "https://cdn.tse.jus.br/estatistica/sead/odsele/convocacao_mesarios/convocacao_mesarios_2020.zip",
    ],
    "eleicoes/2020/pesquisas/":[
        "https://cdn.tse.jus.br/estatistica/sead/odsele/pesquisa_eleitoral/pesquisa_eleitoral_2020.zip", #Pesquisas eleitorais (formato ZIP)
        "https://cdn.tse.jus.br/estatistica/sead/odsele/pesquisa_eleitoral/nota_fiscal_2020.zip", #Notas fiscais (formato ZIP)
        "https://cdn.tse.jus.br/estatistica/sead/odsele/pesquisa_eleitoral/questionario_pesquisa_2020.zip", #Questionários de pesquisa (formato ZIP)
        "https://cdn.tse.jus.br/estatistica/sead/odsele/pesquisa_eleitoral/bairro_municipio_2020.zip", #Detalhamento de bairro/município (formato ZIP)
    ],
    "eleicoes/2020/prestacao_candidatos/":[
        "https://cdn.tse.jus.br/estatistica/sead/odsele/prestacao_contas/prestacao_de_contas_eleitorais_orgaos_partidarios_2020.zip", #Órgãos partidários (formato zip)
        "https://cdn.tse.jus.br/estatistica/sead/odsele/prestacao_contas/prestacao_de_contas_eleitorais_candidatos_2020.zip", #Candidatos (formato zip)
        "https://cdn.tse.jus.br/estatistica/sead/odsele/prestacao_contas/CNPJ_campanha_2020.zip", #CNPJ de campanha (formato zip)
    ],
    "eleicoes/2020/processual/":[
        "https://cdn.tse.jus.br/estatistica/sead/odsele/processual/processo_eleitoral_2020.zip", #Processo Eleitoral
        "https://cdn.tse.jus.br/estatistica/sead/odsele/processual/processos_eleitorais_assuntos_2020.zip", #Assuntos
        "https://cdn.tse.jus.br/estatistica/sead/odsele/processual/processos_eleitorais_decisoes_2020.zip", #Decisões
        "https://cdn.tse.jus.br/estatistica/sead/odsele/processual/recursos_eleitorais_2020.zip", #Recursos
    ],
    "eleicoes/2020/resultados/":[
        "https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_candidato_munzona/votacao_candidato_munzona_2020.zip", #Votação nominal por município e zona (formato ZIP)
        "https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_partido_munzona/votacao_partido_munzona_2020.zip", #Votação em partido por município e zona (formato ZIP)
        "https://cdn.tse.jus.br/estatistica/sead/odsele/detalhe_votacao_munzona/detalhe_votacao_munzona_2020.zip", #Detalhe da apuração por município e zona (formato ZIP)
        "https://cdn.tse.jus.br/estatistica/sead/odsele/detalhe_votacao_secao/detalhe_votacao_secao_2020.zip", #Detalhe da apuração por seção eleitoral (formato ZIP)
    ],
    "eleicoes/2020/resultados/boletins_urna/1_turno/":[
        "https://cdn.tse.jus.br/eleicoes2020/buweb/bweb_1t_{UF}_181120201549.zip", #Boletim de urna — Primeiro turno
    ],
    "eleicoes/2020/resultados/boletins_urna/2_turno/":[
        "https://cdn.tse.jus.br/eleicoes2020/buweb/bweb_2t_{UF}_301120201245.zip", #Boletim de urna — Segundo turno
    ],
    "eleicoes/2020/resultados/votacao_secao/":[
        "https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2020_{UF}.zip", #Votação por seção eleitoral
    ],
}

files = {
    "eleicoes/2020/candidatos/fotos/":[
        "https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2020/fotos/foto_cand2020_{UF}_div.zip", #Fotos de candidatos
    ],
    "eleicoes/2020/candidatos/proposta_gov/":[
        "https://cdn.tse.jus.br/estatistica/sead/odsele/proposta_governo/proposta_governo_2020_{UF}.zip", #Proposta de governo
    ]
}

for folder in files:
    for file in files[folder]:
        if "{UF}" in file:
            string_to_replace = file
            del files[folder][0]
            for uf in ufs:
                files[folder].append(file.replace("{UF}", uf))

def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist
    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)
    r = request.urlretrieve(url, file_path)
    return file_path

for folder in files:
    for file in files[folder]:
        print("\n################\n\nDownloading URL ["+file+"] to folder ["+folder+"]...")
        final_file = download(file, dest_folder=folder)
        if final_file.endswith(".zip"):
            if unzip_files:
                final_file_folder = final_file.replace(".zip", "")
                print("Unzipping file ["+final_file+"]...")
                os.system("unzip -d "+final_file_folder+" "+final_file) # Unzip files
                print("Uploading folder ["+final_file_folder+"] to Spaces...")
                os.system("s3cmd --recursive put "+final_file_folder+" s3://shud/"+final_file_folder.rsplit("/", 1)[0]+"/") # Upload to Spaces
                print("Deleting folder ["+final_file_folder+"] from droplet...")
                os.system("rm -rf "+final_file_folder.split("/")[0]) # Delete files from droplet
            else:
                print("Uploading file ["+final_file+"] to Spaces...")
                os.system("s3cmd --recursive put "+final_file+" s3://shud/"+final_file.rsplit("/", 1)[0]+"/") # Upload to Spaces
                print("Deleting folder ["+final_file+"] from droplet...")
                os.system("rm -rf "+final_file.split("/")[0]) # Delete files from droplet

            print("URL ["+file+"] done!")
