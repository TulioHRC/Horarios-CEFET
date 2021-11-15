import pandas as pd
import numpy as np

def getDatabase(path, get="dict"): # Retorna um dicionário com os itens, como as colunas da planilha. E os valores como as linhas
    result = {}

    df = pd.read_excel(path) # Lê planilha
    df_columns = list(df.columns.values)
    df = df.fillna(0) # Preenche as celulas da planilha vazias, com 0.

    if get == "columns":
        return df_columns

    for col in df_columns:
        result[f"{col}"] = list(df[f"{col}"].values)

    return result
