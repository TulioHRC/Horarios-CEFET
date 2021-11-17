# Importando bibliotecas
import random
import pandas as pd
# Demonstrando utilização do pandas

df = pd.read_excel('Planilha.xlsx', 'Sheet1') # Lendo a planilha do excel, e Sheet1 é o nome da aba do excel para ler

lista = list(c for c in range(0, 5))
for a in range(len(lista), 0, -1):
    print(a)

print(lista)