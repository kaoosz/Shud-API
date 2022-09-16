"""<Short description>
<Long description>
Author: <Name> <email>
Created: <date>
"""

import boto3
from boto3.s3.transfer import TransferConfig
import os
import dotenv
dotenv.load_dotenv()
import math
from progressbar.progressbar import ProgressBar
from progressbar import Percentage, Bar, ETA, FileTransferSpeed

def credenciais(prefix:str='DO_SPACES') -> list:
    """Gera uma lista contendo as credenciais a partir do arquivo ".env" no diretório root.

    Busca pelas variáveis de ambiente {prefix}_KEY, {prefix}_SECRET, {prefix}_ENDPOINT, {prefix}_REGION, {prefix}_BUCKET

    Args:
        prefix (str): string de prefixo antes de cada uma das variáveis a serem carregadas no .env

    Returns:
        list: [key, secret, endpoint, region, bucket]
    """
    key = os.getenv(prefix+'_KEY')
    secret = os.getenv(prefix+'_SECRET')
    endpoint = os.getenv(prefix+'_ENDPOINT')
    region = os.getenv(prefix+'_REGION')
    bucket = os.getenv(prefix+'_BUCKET')
    return [key, secret, endpoint, region, bucket]


def cliente_s3(credentials:list):
    """Cria uma instancia de cliente do S3 após abrir sessão.

    Args:
        credentials (list): lista de credenciais [key, secret, endpoint, region, bucket]

    Returns:
        client: client
    """
    session = boto3.session.Session()
    client = session.client(
        's3',
        aws_access_key_id=credentials[0],
        aws_secret_access_key=credentials[1],
        endpoint_url=credentials[2],
        region_name=credentials[3]
    )
    return client

credentials = credenciais()
client = cliente_s3(credentials=credentials)


def listar_arquivos_s3(credentials:list, s3_path:str, extension:str="", sort_by_id:bool=False) -> list:
    """Lista os arquivos disponiveis em um diretorio do S3.

    Args:
        credentials (list): lista contendo as credenciais para acesso ao S3, ex:
        [region_name, endpoint_url, aws_access_key_id, aws_secret_access_key]

        s3_path (str): string contendo caminho da pasta (excluindo o bucket), ex:
        "seedief/cubes/sentinel/"

    Returns:
        list: lista com todos os arquivos dentro do repositório em s3_path
    """

    paginator = client.get_paginator('list_objects_v2')

    pages = paginator.paginate(Bucket=credentials[4], Prefix=s3_path).build_full_result()

    files_in_folder = []
    
    for object in pages["Contents"]:
        obj_filename = object["Key"]
        if (extension != "" and obj_filename.endswith(extension)) or (extension == ""):
            files_in_folder.append(obj_filename)

    if sort_by_id:
        files_in_folder = sortear_pelo_id(files_in_folder)

    return files_in_folder


def sortear_pelo_id(file_list:list, sep:str="_", sort_index:int=1) -> list:
    """Adicionar descrição do que o método faz aqui.

    Se houver uma descrição adicional, manter um espaço entre as linhas como este exemplo.

    Args:
        nome_do_argumento (str): descrição do que deve ser inserido no argumento

    Returns:
        list: descrição do que é retornado pela função
    """
    sorted_list = file_list
    sorted_list.sort()
    sorted_list.sort(key=lambda x:int(x.split(sep)[sort_index]))
    return sorted_list

def download_s3(s3_path:str, dest_path:str, show_progress:bool=True) -> bool:
    """
        Download de um arquivo do S3 para um local específico.

        Args:
            s3_path (str): caminho do arquivo no S3
            dest_path (str): caminho do arquivo local
            show_progress (bool): mostrar o progresso do download

        Returns:
            bool: True se o arquivo foi baixado com sucesso, False se não
    """
    bucket = credentials[4]
    config = TransferConfig(multipart_threshold=1*(1024 ** 3), max_concurrency=5, num_download_attempts=5)

    if show_progress:
        # Pega os metadados do arquivo para saber o tamanho
        metadata = client.head_object(Bucket=bucket, Key=s3_path)
        total_length = int(metadata.get('ContentLength', 0))
        file_size_str = convert_size(total_length)
        # Cria um progress bar com descrição e porcentagem baseada em "total_length"
        widgets = [f'Baixando [{s3_path.split("/")[-1]}] >>> ', Percentage(), ' ', Bar(marker='#', left='[', right=']'), ' ', ETA(), ' ', FileTransferSpeed(), ' ', file_size_str]
        progress = ProgressBar(widgets=widgets, maxval=total_length).start()
        # Cria callback para atualizar o progress bar
        def download_progress(chunk):
            progress.update(progress.currval + chunk)
        # Baixa o arquivo
        client.download_file(bucket, s3_path, dest_path, Callback=download_progress, Config=config)
        # Finaliza o progress bar
        progress.finish()
    else:
        # Baixa o arquivo
        client.download_file(bucket, s3_path, dest_path, Config=config)

    return os.path.isfile(dest_path)


def upload_s3(source_path:str, s3_path:str, public_file:bool=False, content_type:str="", show_progress:bool=False) -> bool:
    """
        
    """
    # TODO: se "source_path" for um caminho e não um arquivo,
    #       listar todos arquivos dentro da pasta e enviar todos
    # TODO: se arquivo não existir, soltar um return False
    # TODO: adicionar progress bar (talvez)
    bucket = credentials[4]
    args = {'ACL':'public-read'} if public_file else {}
    # Adiciona uma chave a variavel "args" caso content_type seja diferente de ""
    if content_type != "":
        args['ContentType'] = content_type
    client.upload_file(source_path, bucket, s3_path, ExtraArgs=args)
    # checar se o arquivo foi enviado com sucesso
    return True


def check_file_in_s3(s3_path:str) -> bool:
    """
        Checa se um arquivo existe no S3 no caminho "s3_path"

        Args:
            s3_path (str): caminho do arquivo no S3

        Returns:
            bool: True se o arquivo existe no S3, False se não existe
    """
    bucket = credentials[4]
    client.head_object(Bucket=bucket, Key=s3_path)
    return True


def convert_size(size) -> str:
    """
        Converte o tamanho de um arquivo em bytes para uma string com o tamanho em MB, GB, etc.

        Args:
            size (int): tamanho do arquivo em bytes

        Returns:
            str: tamanho do arquivo em MB, GB, etc.
    """
    if (size == 0):
        return '0B'
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size,1024)))
    p = math.pow(1024,i)
    s = round(size/p,2)
    return '%.2f %s' % (s,size_name[i])


def convert_bytes(size):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0
    return size