

# carrega um arquivo .csv com o pandas
import pandas as pd

# C:\Users\Wenyx\OneDrive\Área de Trabalho\EXCEL
# data/data.csv

df = pd.read_csv('C:\Users\Wenyx\OneDrive\Área de Trabalho\EXCEL\ALEXANDRE_AUGUSTO_20120_2016.csv')
#transforma o dataframe em um arquivo excel
df.to_excel('data/data.xlsx')
