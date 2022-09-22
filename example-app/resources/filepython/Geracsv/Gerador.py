import requests
import pandas as pd
import sys


#para = sys.argv[1]

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

#request = requests.get('http://localhost:8000/api/candidatos')

# response = request.json()


# dt = pd.DataFrame(response['data'])
# dt.to_csv('meu csv')


# data = request.json()
# if 'data' in data:
#      data = data['data']

# df = pd.DataFrame(data[0]['bairro2018'])
# df.to_csv('toninsasas.csv')

