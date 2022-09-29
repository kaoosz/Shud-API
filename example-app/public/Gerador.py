import requests
import pandas as pd
import sys
import base64



para2 = sys.argv[1]

ba = base64.b64decode(para2)


# para2 = para2.replace('-','&')
# para2 = para2.replace('csv=csv','')
s = ba.decode('UTF-8')
s = s.replace('csv=csv','')

#ba = ba.replace('csv=csv','')

headers = {
     'Accept': 'application/json',
     'Content-Type': 'application/json',
#     'Authorization': 'Bearer o93RCG3DXhR99VWQGdSQKtfK6YYhQjlumrI63skl'
}



# # request = requests.get('http://142.93.244.160/api/candidatos/candidatos',headers=headers,params=params)

request = requests.get(url=s,headers=headers)

response = request.json()
print(response)


d1 = pd.DataFrame(response["data"])
if 'bairro2018' in d1.columns:
    d1 = d1.iloc[:,:-1]
    df = pd.DataFrame(response['data'][0])
    df = df['bairro2018']['data']
    f = pd.DataFrame(df)
    d1.to_csv('outpu.csv',index=False)
    f.to_csv('outpu.csv',index=False,mode='a')


if 'cities2018' in d1.columns:
    d1 = d1.iloc[:,:-1]
    df = pd.DataFrame(response['data'][0])
    df = df['cities2018']['data']
    f = pd.DataFrame(df)
    d1.to_csv('outpu.csv',index=False)
    f.to_csv('outpu.csv',index=False,mode='a')



