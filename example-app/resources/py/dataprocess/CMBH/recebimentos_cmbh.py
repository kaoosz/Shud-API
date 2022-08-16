import os
import requests
from bs4 import BeautifulSoup as bs
import dotenv
dotenv.load_dotenv()
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine
import json

complete_data = []
for page_index in range(1,65):
    r = requests.post("https://www.cmbh.mg.gov.br/extras/remuneracao/index.php", {
        'limpa': None,
        'pagina': page_index,
        'nome': None,
        'situacao':  None,
        'cargo':  None,
        'periodo': 202109
    })

    soup = bs(r.content,'html.parser')
    table = soup.find("table")

    for row in table.findAll("tr"):
        if len(row.findAll("td")) > 0:
            data = {}
            tds = row.findAll("td")
            name = tds[0].find("a").text
            href = tds[0].find("a").attrs['href']
            id = tds[1].text
            info = requests.get("https://www.cmbh.mg.gov.br/extras/remuneracao/"+href)
            soup2 = bs(info.content, 'html.parser')
            table2 = soup2.findAll("table")
            dados = table2[0]
            for line in dados.findAll("tr"):
                index = 0
                chave = ""
                valor = ""
                for cell in line:
                    if index == 0:
                        chave = cell.text
                        index += 1
                    else:
                        valor = cell.text
                data[chave] = valor
                #print(chave, ": ", valor)
            try:
                remuneracao = table2[2]
                remuneracao = remuneracao.findAll("table")
                for line in remuneracao[1].findAll("tr"):
                    index = 0
                    chave = ""
                    valor = ""
                    for cell in line:
                        if index == 0:
                            chave = cell.text
                            index += 1
                        else:
                            valor = cell.text
                    data[chave] = valor
                    #print(chave, ": ", valor)    
                total_liquido_chave = table2[2].findAll("tr")[-1].findAll("td")[0].text
                total_liquido_valor = table2[2].findAll("tr")[-1].findAll("td")[1].find("div").text
                data[total_liquido_chave] = total_liquido_valor
                #print(total_liquido_chave, ": ", total_liquido_valor)
                #print(data)
                complete_data.append(data)
            except:
                continue

# Create engine connection to PostgreSQL
engine = create_engine("postgresql://"+os.getenv('DB_USERNAME')+":"+os.getenv('DB_PASSWORD')+"@"+os.getenv('DB_HOST')+":"+os.getenv('DB_PORT')+"/"+os.getenv('DB_DATABASE')+"")

df = pd.DataFrame.from_dict(pd.DataFrame(complete_data))

# Create or append to table with data
df.to_sql("cmbh", con=engine, schema="public", if_exists='append')