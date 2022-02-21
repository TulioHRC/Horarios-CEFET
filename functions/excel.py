import pandas as pd
from tkinter import messagebox
from functions import convert

def saveTeacher(name, subject, type, classes, grade, subGroup, prefers, limits):
    err = 0
    if len(name) <= 2 or len(subject) <= 2:
        messagebox.showerror('Erro', 'O nome do professor ou da matéria está muito pequeno!\nMude e tente novamente.')
        err = 1
    if not grade:
        messagebox.showerror('Erro', 'A série do professor não foi colocada.\nMude e tente novamente.')
        err = 1

    if not err:
        df = pd.read_excel('Planilha.xlsx', 'Sheet1')

        prefersResult = ''

        for day in prefers["S"]:
            if len(prefersResult) != 0:
                prefersResult += '-'
            prefersResult += f"S{convert.convertDayToNum(day)}"
        for day in prefers["N"]:
            if len(prefersResult) != 0:
                prefersResult += '-'
            prefersResult += f"N{convert.convertDayToNum(day)}"
        for room in prefers["R"]:
            if len(prefersResult) != 0:
                prefersResult += '-'
            prefersResult += f"{room}"

        limitsResult = ''
        for l in limits:
            if len(limitsResult) != 0:
                limitsResult += '-'
            if l[0] == 'R': limitsResult += f"{l}"
            else:
                limitsResult += f"N{convert.convertDayToNum(l)}"

        df2 = pd.DataFrame({'Professor': [name], 'Materia': [subject], 'Tipo': [type], 'Ano': [grade], 'Sub-Grupo': subGroup, 'Preferencias': [prefersResult], 'Limitacoes': [limitsResult]})

        for i in classes:
            df2[f"{i}"] = classes[i]

        newDf = pd.concat([df, df2], ignore_index=True,)

        newDf.to_excel('Planilha.xlsx', index=False)

def saveRoom(name, local, limits):
    err = 0
    if len(name) <= 2:
        messagebox.showerror('Erro', 'O nome da sala está muito pequeno!\nMude e tente novamente.')
        err = 1

    if not err:
        df = pd.read_excel('Planilha sala.xlsx', 'Sheet1')

        limitsResult = ''
        for l in limits:
            if len(limitsResult) != 0:
                limitsResult += '-'
            if l == 'ESPECIFICA': limitsResult += "ESPECIFICA"
            else: limitsResult += f"N{convert.convertDayToNum(l)}"

        df2 = pd.DataFrame({'Sala': [name], 'Local': [local], 'Limitacoes': [limitsResult]})

        newDf = pd.concat([df, df2], ignore_index=True,)

        newDf.to_excel('Planilha sala.xlsx', index=False)
