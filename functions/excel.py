import pandas as pd
from tkinter import messagebox
from functions import convert2day as convert

def saveTeacher(name, subject, classes, grade, prefers, limits):
    if len(name) <= 2 or len(subject) <= 2:
        messagebox.showerror('Erro', 'O nome do professor ou da matéria está muito pequeno!\nMude e tente novamente.')
    if not grade:
        messagebox.showerror('Erro', 'A série do professor não foi colocada.\nMude e tente novamente.')

    df = pd.read_excel('Planilha.xlsx', 'Sheet1')

    # Falta definir preferencias e limites
    prefersResult = ''

    for day in prefers["S"]:
        if len(prefersResult) != 0:
            prefersResult += '-'
        prefersResult += f"S{convert.convertDayToNum(day)}"
    for day in prefers["N"]:
        if len(prefersResult) != 0:
            prefersResult += '-'
        prefersResult += f"N{convert.convertDayToNum(day)}"

    limitsResult = ''
    for day in limits:
        if len(limitsResult) != 0:
            limitsResult += '-'
        limitsResult += f"N{convert.convertDayToNum(day)}"

    df2 = pd.DataFrame({'Professor': [name], 'Materia': [subject], 'Ano': [grade], 'Preferencias': [prefersResult], 'Limitacoes': [limitsResult]})

    for i in classes:
        df2[f"{i}"] = classes[i]

    newDf = pd.concat([df, df2], ignore_index=True,)

    newDf.to_excel('Planilha.xlsx', index=False)

def saveRoom(number, possibilities):
    pass
