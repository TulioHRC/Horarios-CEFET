import pandas as pd
from tkinter import messagebox
from functions import convert

def saveTeacher(name, subject, type, classes, grade, subGroup, bimestral, prefers, limits):
    err = 0
    if len(name) <= 2 or len(subject) <= 2:
        messagebox.showerror('Erro', 'O nome do professor ou da matéria está muito pequeno!\nMude e tente novamente.')
        err = 1
    if not grade:
        messagebox.showerror('Erro', 'A série do professor não foi colocada.\nMude e tente novamente.')
        err = 1

    if not err:
        df = pd.read_excel('Planilha.xlsx', 'Sheet1')

        # Bimestral adaptation
        if bimestral[0] == 'S': bimestral = 1
        else: bimestral = ""


        # Prefers and limits adaptation
        prefersResult = ''

        for day in prefers["S"]:
            d = day.split(';')[0]
            hours = day.split(';')[1].split(',')
            if len(prefersResult) != 0:
                prefersResult += '-'
            prefersResult += f"S{convert.convertDayToNum(d)}:{min(hours)},{max(hours)}"
        for day in prefers["N"]:
            d = day.split(';')[0]
            hours = day.split(';')[1].split(',')
            if len(prefersResult) != 0:
                prefersResult += '-'
            prefersResult += f"S{convert.convertDayToNum(d)}:{min(hours)},{max(hours)}"
        for room in prefers["R"]:
            d = day.split(';')[0]
            hours = day.split(';')[1].split(',')
            if len(prefersResult) != 0:
                prefersResult += '-'
            prefersResult += f"S{convert.convertDayToNum(d)}:{min(hours)},{max(hours)}"

        limitsResult = ''
        for l in limits:
            o = l.split(';')[0]
            hours = l.split(';')[1].split(',')
            if len(limitsResult) != 0:
                limitsResult += '-'
            if l[0] == 'R': limitsResult += f"{o}:{min(hours)},{max(hours)}"
            else:
                limitsResult += f"N{convert.convertDayToNum(o)}:{min(hours)},{max(hours)}"

        df2 = pd.DataFrame({'Professor': [name], 'Materia': [subject], 'Tipo': [type], 'Ano': [grade], 'Bimestral': bimestral, 'Sub-Grupo': subGroup, 'Preferencias': [prefersResult], 'Limitacoes': [limitsResult]})
        print(df2)

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
