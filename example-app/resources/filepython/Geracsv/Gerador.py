import requests
import pandas as pd

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer o93RCG3DXhR99VWQGdSQKtfK6YYhQjlumrI63skl'
}

params = {
    'urna':'MARCELO ARO',
    'bairro':'bairro2018',
    'ANO':'2018',
    'NR_CANDIDATO':'3133',
}
coll = [
            "NM_VOTAVEL",
            "NR_VOTAVEL",
            "ANO_ELEICAO",
            "DS_CARGO_PERGUNTA",
            "NM_MUNICIPIO",
            "NM_BAIRRO",
            "QT_VOTOS",
        ]

request = requests.get('http://127.0.0.1:8000/api/candidatos/candidatos?bairro=bairro2018&ANO=2018&urna=MARCELO ARO&NR_CANDIDATO=3133',
 params=params, headers=headers)

response = request.json()



data = request.json()
if 'data' in data:
    data = data['data']

df = pd.DataFrame(data[0]['bairro2018'])
df.to_csv('tonin.csv')

