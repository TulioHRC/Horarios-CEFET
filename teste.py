import pandas as pd

df = pd.read_excel('Planilha.xlsx', sheet_name='Sheet1')
print(df.loc[1][5])
if str(df.loc[1][5]) == 'nan':
    print('É igual')