import pandas as pd
from functions import convert as conv

def saveSheet(name, xData, yData={"Horarios": ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']}, path="./data/", type="turm", intervals=1):
    # xData terão o formato: {"COLLUMN 1": [valores], ...}
    # Valores de xData de turma ['2-Desenho Tecnico']; de professores ['2-Desenho Tecnico - MCT-1A']
    # yData será a primeira coluna da planilha, tendo o formato: {"Nome das linhas": [lista de nomes das linhas]}
    #print(f'{name} -> {yData, xData}')

    rows = list(yData.values())[0].copy()

    for index, row in enumerate(rows):
        rows[index] = conv.convertNumToHour(row)

    df = {
        f"{name}": rows,
    }

    if intervals:
        vals = ['Intervalo', 'Almoço']

    if type == "turm":
        for day in ['2','3','4','5','6']:
            dayConv = conv.convertNumToDay(day)
            df[dayConv] = []
            for hour in list(yData.values())[0]:
                df[dayConv].append('-')
                if not str(xData[day]).find(f"\'{hour}-") == -1:
                    df[dayConv][int(hour)-1] = str(xData[day])[str(xData[day]).find(f"-", str(xData[day]).find(f"\'{hour}-")) + 1:str(xData[day]).find(f"'", str(xData[day]).find(f"\'{hour}-")+1)]
                elif vals:
                    if hour in ['4', '11']: df[dayConv][int(hour)-1] = vals[0]  # Intervalo
                    elif hour in ['7']: df[dayConv][int(hour)-1] = vals[1] # Almoço
    elif type == "teacher":
        for day in ['2','3','4','5','6']:
            dayConv = conv.convertNumToDay(day)
            df[dayConv] = []
            for hour in list(yData.values())[0]:
                df[dayConv].append('-')
                if not str(xData[day]).find(f"\'{hour}-") == -1:
                    df[dayConv][int(hour)-1] = str(xData[day])[str(xData[day]).find(f"-", str(xData[day]).find(f"\'{hour}-")) + 1:str(xData[day]).find(f"'", str(xData[day]).find(f"\'{hour}-")+1)]
                elif vals:
                    if hour in ['4', '11']: df[dayConv][int(hour)-1] = vals[0]  # Intervalo
                    elif hour in ['7']: df[dayConv][int(hour)-1] = vals[1] # Almoço

    df = pd.DataFrame(data=df)
    df.to_excel(f"{path}{type}/{name}.xlsx", index=False)
