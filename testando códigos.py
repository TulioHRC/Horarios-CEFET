import pandas as pd
df = pd.read_excel('Planilha esperada.xlsx', 'Sheet1')
lista = [0, 1, 2, 3, 4, 5]
lista = lista[1:]
print(lista)