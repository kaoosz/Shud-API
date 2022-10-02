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


headers = {
     'Accept': 'application/json',
     'Content-Type': 'application/json',
#     'Authorization': 'Bearer o93RCG3DXhR99VWQGdSQKtfK6YYhQjlumrI63skl'
}



# # request = requests.get('http://142.93.244.160/api/candidatos/candidatos',headers=headers,params=params)

request = requests.get(s,headers=headers)

response = request.json()

q = ['cities2020','cities2018','cities2016','cities2014','cities2012',
    'bairro2020','bairro2018','bairro2016','bairro2014','bairro2012',
    'schools2020','schools2018','schools2016','schools2014','schools2012']

d1 = pd.DataFrame(response['data'])
f = None


for i in q:
    if i in d1.columns:
        d1 = d1.iloc[:,:-1]
        df = pd.DataFrame(response['data'])
        df = df[i][0]
        f = pd.DataFrame(df)
        d1.to_csv('output.csv',index=False)
        f.to_csv('output.csv',index=False,mode='a')






