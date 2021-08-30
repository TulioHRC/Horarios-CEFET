# Importando bibliotecas

import pandas as pd

# Demonstrando utilização do pandas

df = pd.read_excel('Planilha esperada.xlsx', 'Sheet1') # Lendo a planilha do excel, e Sheet1 é o nome da aba do excel para ler

print(df) # Printando o dataframe encontrado na planilha