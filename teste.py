# Importando bibliotecas

import pandas as pd

# Demonstrando utilização do pandas

df = pd.read_excel('./Planilha.xlsx') # Lendo a planilha do excel, e Sheet1 é o nome da aba do excel para ler

print(df) # Printando o dataframe encontrado na planilha
