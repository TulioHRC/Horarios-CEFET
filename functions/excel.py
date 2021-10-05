import pandas as pd
from tkinter import messagebox

def saveTeacher(name, subject, classes, grade, prefers, limits):
    if len(name) <= 2 or len(subject) <= 2:
        messagebox.showerror('Erro', 'O nome do professor ou da matéria está muito pequeno!\nMude e tente novamente.')
    if not grade:
        messagebox.showerror('Erro', 'A série do professor não foi colocada.\nMude e tente novamente.')

    df = pd.read_excel('Planilha.xlsx', 'Sheet1')

    # Falta definir preferencias e limites

    df2 = pd.DataFrame({'Professor': [name], 'Materia': [subject], 'Ano': [grade], 'Preferencias': [''], 'Limitacoes': ['']})

    for i in classes:
        df2[f"{i}"] = classes[i]


    newDf = pd.concat([df, df2], ignore_index=True,)

    newDf.to_excel('Planilha.xlsx')

def saveRoom(number, possibilities):
    pass
