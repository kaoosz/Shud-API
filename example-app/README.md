ADICIONEI CPF menor que 11 digitos o 0 na frente..
########
TODOS OS CANDIDATOS ###############
################
http://localhost:8000/api/candidatos

PESSOA ESPECIFICA com todas ELEICOES

http://localhost:8000/api/candidatos/candidatos?urna=MARCELO%20ARO


APENAS ANO E NUMERO DO CANDIDATO E NOME
http://localhost:8000/api/candidatos/candidatos?urna=MARCELO%20ARO&NR_CANDIDATO=3133&ANO=2014

#############
VOTOS POR CIDADE
#######
http://localhost:8000/api/candidatos/candidatos?cidade=cities2014&urna=MARCELO%20ARO&NR_CANDIDATO=3133&ANO=2014
#######
VOTOS CIDADE POR UF ###
#######
http://localhost:8000/api/candidatos/candidatos?UF=BELO HORIZONTE&cidade=cities2014&urna=MARCELO%20ARO&NR_CANDIDATO=3133&ANO=2014

######
VOTOS ESCOLA ##
######
http://localhost:8000/api/candidatos/candidatos?escola=schools2014&urna=MARCELO%20ARO&NR_CANDIDATO=3133&ANO=2014
######
VOTOS ESCOLA UF ##
######
http://localhost:8000/api/candidatos/candidatos?UF=BELO HORIZONTE&escola=schools2014&urna=MARCELO%20ARO&NR_CANDIDATO=3133&ANO=2014

######
VOTOS BAIRRO ##
######
http://localhost:8000/api/candidatos/candidatos?bairro=bairro2014&urna=MARCELO%20ARO&NR_CANDIDATO=3133&ANO=2014
######
VOTOS BAIRRO UF ##
######
http://localhost:8000/api/candidatos/candidatos?UF=BELO HORIZONTE&bairro=bairro2014&urna=MARCELO%20ARO&NR_CANDIDATO=3133&ANO=2014

######
Paginação Exemplo &page=3
paginação para não ter uma resposta de 30 mil linhas
serão exibidos 10 resuldatos por pagina....
######
http://localhost:8000/api/candidatos/candidatos?bairro=bairro2014&NR_CANDIDATO=3133&ANO=2014&urna=MARCELO ARO&page=3
######

######
MAIS VOTADOS POR BAIRRO TOP 10 Candidatos DE UM BAIRRO
######

mais votados por Bairro pega todos municipios e bairro sem restrições
Ex: top_bairro=bairro e amount=5 é quantidade de candidatos retornada
######
http://localhost:8000/api/candidatosMaisVotadosBairro/10?top_bairro=bairro2018&amount=5
######

######

bairro com Municipio  traz todos candidatos com este municipio
ex: municipio=UBERLÂNDIA e amount=5 é quantidade desejada
######
http://localhost:8000/api/candidatosMaisVotadosBairro/10?top_bairro=bairro2018&municipio=UBERLÂNDIA&amount=5
######

bairro com outro bairro definido e quantidade desejada
ex: bairro=CENTRO e amount=5 quantidade igual 5
######
http://localhost:8000/api/candidatosMaisVotadosBairro/10?top_bairro=bairro2018&bairro=CENTRO&amount=5
######


bairro e apenas Cargo e quantidade desejada traz apenas candidatos com este cargo especifico
ex: cargo=SENA e amount=5
######
http://localhost:8000/api/candidatosMaisVotadosBairro/10?top_bairro=bairro2018&cargo=SENADOR&amount=5
######


bairro com Municipio definido e Bairro definido retorna aquele municipio e bairro especifico apenas
ex: municipio=UBERLÂNDIA e bairro=CENTRO e amount=5
######
http://localhost:8000/api/candidatosMaisVotadosBairro/10?top_bairro=bairro2018&municipio=UBERLÂNDIA&bairro=CENTRO&amount=5
######

bairro com Municipio,Bairro,Cargo defenidos vão retornar apenas candidatos com essas caracteristicas
ex: municipio=UBERLÂNDIA e bairro=CENTRO e cargo=SENADOR e amount=5
######
http://localhost:8000/api/candidatosMaisVotadosBairro/10?top_bairro=bairro2018&municipio=UBERLÂNDIA&bairro=CENTRO&cargo=SENADOR&amount=5
######

######
MAIS VOTADOS POR ESCOLA TOP 10 Candidatos DE UMA ESCOLA
######


candidatos por escola vai de trazer os candidatos por escola com mais votos
ex: top_escola=escola2012 ou escola2020 amount=5

######
http://localhost:8000/api/candidatosMaisVotadosEscola/?top_escola=escola2012&amount=5
######

candidatos por escola vai trazer os candidatos por escola e um determinado Municipio amount é quantidade
ex: MUNICIPIO=UBERLÂNDIA e amount=5
######
http://localhost:8000/api/candidatosMaisVotadosEscola/?municipio=UBERLÂNDIA&top_escola=escola2012&amount=5
######

candidatos por escola vai trazer os candidatos por escola e um determinado Cargo e amount é quantidade desejada
ex: CARGO=PREFEITO e amount=5
######
http://localhost:8000/api/candidatosMaisVotadosEscola/?top_escola=escola2012&cargo=PREFEITO&amount=5
######

candidatos por escola vai trazer os candidatos por escola e um determinado Cargo e Municipio e quantidade é amount=5
ex: CARGO=PREFEITO e MUNICIPIO=UBERLÂNDIA e amount=5
######
http://localhost:8000/api/candidatosMaisVotadosEscola/?municipio=UBERLÂNDIA&top_escola=escola2012&cargo=PREFEITO&amount=5
######
######

Top Votos por Cidade
######
votos por Cidade você passa o ano e quantidade ele trara quantidate especifica de Candidatos
ex:top_cidade=cidade2014 e amount=10 quantidade
######
http://localhost:8000/api/candidatosMaisVotadosCidade/?top_cidade=cidade2014&amount=10
######

votos por Cidade com Cargo e quantidade. trara apenas de uma cidade e cargo especifico
ex: cargo=SENADOR ou cargo=DEPUTADO FEDERAL
######
http://localhost:8000/api/candidatosMaisVotadosCidade/?top_cidade=cidade2014&amount=10&cargo=SENADOR
######

votos por Cidade especifica retorna apenas Candidatos de uma cidade especifica apenas
ex: municipio=UBERLÂNDIA e top_cidade=cidade2014 e amount=10
######
http://localhost:8000/api/candidatosMaisVotadosCidade/?municipio=UBERLÂNDIA&top_cidade=cidade2014&amount=10
######

votos por Cidade,Cargo especificos isso retorna apenas Candidatos com Cidade e Cargo especificos
ex: municipio=UBERLÂNDIA e cargo=SENADOR e amount=10
######
http://localhost:8000/api/candidatosMaisVotadosCidade/?municipio=UBERLÂNDIA&top_cidade=cidade2014&amount=10&cargo=SENADOR
######
######
######
######


#OBS SE VOCÊ COLOCAR ANO = 2018 e bairro2014
#ele irá trazer os dados de 2014

#TODAS FUNÇÔES DE PESQUISA APENAS MUDAR O ANO QUE IRA FUNCIONAR CORRETAMENTE

urna=MARCELO%20ARO ou urna=MARCELO ARO  ## ira funcionar normalmente.. é nome do candidato


bairro=bairro2014 ou bairro=bairro2018

escola=schools2014 ou escola=schools2018

cidade=cities2014 ou cidade=cities2018


NR_CANDIDATO=3133   ## numero da urna do candidato

ANO=2014 ou ANO=2018  ## ano da eleição alvo da pesquisa

UF=BELO HORIZONTE ou UF=PARAOPEBA  ## cidade alvo é o MUNICIPIO

page=3 ## Paginação para não ter 30 mil linhas de jsoon de registros

