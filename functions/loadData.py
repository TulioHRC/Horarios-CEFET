import pandas as pd
import numpy as np

def getDatabase(path, get="dict"): # Retorna um dicionário com os itens, como as colunas da planilha. E os valores como as linhas
    result = {}

    df = pd.read_excel(path) # Lê planilha
    df_columns = list(df.columns.values)
    df = df.fillna(0) # Preenche as celulas da planilha vazias, com 0.

    if get == "columns": # Lista das colunas
        return df_columns

    for col in df_columns:
        result[f"{col}"] = list(df[f"{col}"].values)

    return result

def getPoints(path, desc=False): # Retorna um dicionário com as pontuações
    with open(path) as file:
        text = file.readlines() # Lista das linhas do arquivo .txt

    points = {}
    for line in text: # Salvando no dicionário
        if not desc:
            points[f"{line.split('=')[0]}"] = float(line.split(';')[0].split('=')[1])
        else:
            points[f"{line.split('=')[0]}"] = str(line.split('//')[1]) # Descrição de cada

    return points
