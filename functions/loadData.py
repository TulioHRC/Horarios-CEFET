import pandas as pd
import numpy as np
#from classes import Node

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

"""
def making_nodes(path):
    df = pd.read_excel(path)
    todos_os_horarios = []
    for l in range(0, df.shape[0]):
        for c in range(7, df.shape[1]):
            if not(str(df.loc[l][c]) == 'nan'):
                for h in range(0, int(df.loc[l][c])):  # Pego a quantidade de aulas que ele vai dar para essa turma nessa matéria
                    if df['Tipo'][l] == 'Manha':
                        horario = Node(
                            teacher=df['Professor'][l],   # Professor
                            subject=df['Materia'][l],     # Matéria
                            turm=df.columns[c],           # Turma
                            possible_h=[1, 2, 3, 4, 5]    # Possíveis horários que podemos colocá-lo
                        )
                        todos_os_horarios.append(horario)
                    else:
                        horario = Node(
                            teacher=df['Professor'][l],   # Professor
                            subject=df['Materia'][l],     # Matéria
                            turm=df.columns[c],           # Turma
                            possible_h=[6, 7, 8, 9, 10]   # Possíveis horários que podemos colocá-lo
                        )
                        todos_os_horarios.append(horario)

    return todos_os_horarios
"""