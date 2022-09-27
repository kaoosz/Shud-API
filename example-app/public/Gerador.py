import requests
import pandas as pd
import sys



para2 = sys.argv[1]


para2 = para2.replace('-','&')
para2 = para2.replace('csv=csv','')


# headers = {
#     'Accept': 'application/json',
#     'Content-Type': 'application/json',
#     'Authorization': 'Bearer o93RCG3DXhR99VWQGdSQKtfK6YYhQjlumrI63skl'
# }

# params = {
#     'urna':'MARCELO ARO',
#     'bairro':'bairro2018',
#     'ANO':'2018',
#     'NR_CANDIDATO':'3133',
# }


# # request = requests.get('http://142.93.244.160/api/candidatos/candidatos',headers=headers,params=params)

# request = requests.get(para2)

# response = request.json()

print(para2)



# d2 = pd.DataFrame(response["data"][0]['bairro2018'])
# dt = pd.DataFrame(response["data"])
# d1 = dt.iloc[:,:-1]
# d1.to_csv('outpu.csv',index=False)
# d2.to_csv('outpu.csv',index=False,mode='a')


