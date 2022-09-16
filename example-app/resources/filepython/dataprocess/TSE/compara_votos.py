import pandas as pd

prefeitos = pd.read_excel("VOTOS_PREFEITOS.xlsx")
prefeitos2012 = prefeitos[prefeitos["Ano"] == 2012]
prefeitos2016 = prefeitos[prefeitos["Ano"] == 2016]

senadores = pd.read_excel("VOTOS_SENADORES.xlsx")
senadores2014 = senadores[senadores["Ano"] == 2014]
senadores2018 = senadores[senadores["Ano"] == 2018]

# Filtrar apenas os senadores eleitos
senadores2014 = senadores2014[senadores2014["Situação"] == "ELEITO"]
senadores2018 = senadores2018[senadores2018["Situação"] == "ELEITO"]

# Comparar partidos dos senadores eleitos com a composição da coligação de prefeitos
comparacao1 = prefeitos2012.merge(senadores2014, left_on=["Município"], right_on=["Município"], how="left")
# Comparar partidos dos senadores eleitos com a composição da coligação de prefeitos
comparacao2 = prefeitos2016.merge(senadores2018, left_on=["Município"], right_on=["Município"], how="left")


# Conta quantos prefeitos são do mesmo partido que o senador eleito
comparacao1["Prefeitos do mesmo partido"] = comparacao1["Partido_x"] == comparacao1["Partido_y"]
# Conta quantos prefeitos eleitos são do mesmo partido que o senador eleito
print("Comparação 1:")
print(comparacao1["Prefeitos do mesmo partido"].value_counts())

# Conta quantos prefeitos são do mesmo partido que o senador eleito
comparacao2["Prefeitos do mesmo partido"] = comparacao2["Partido_x"] == comparacao2["Partido_y"]
# Conta quantos prefeitos eleitos são do mesmo partido que o senador eleito
print("Comparação 2:")
print(comparacao2["Prefeitos do mesmo partido"].value_counts())

# Checa se a string do partido do senador eleito está contida na string do partido do prefeito
# OU SEJA: Coligação do senador possui partido do prefeito
comparacao1["teste"] = comparacao1.apply(lambda x: x["Partido_x"] in x["Composição da Coligação_y"], axis=1)
print(comparacao1["teste"].value_counts())

# Checa se a string do partido do senador eleito está contida na string do partido do prefeito
# OU SEJA: Coligação do senador possui partido do prefeito
comparacao2["teste"] = comparacao2.apply(lambda x: x["Partido_x"] in x["Composição da Coligação_y"], axis=1)
print(comparacao2["teste"].value_counts())

