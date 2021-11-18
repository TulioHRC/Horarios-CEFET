import pandas as pd

def saveSheet(name, yData, xData, path="./data/", type="turm"):
    # xData terão o formato: {"COLLUMN 1": [valores], ...}
    # Formato dos valores -> ['2-Desenho Técnico:1', '3-Desenho Técnico', '5-EAP', '7-Circuitos Elétricos 2:2', '9-Circuitos Elétricos 2:2', '10-EAP:3', '11-EAP:2', '12-Circuitos Elétricos 2:2']
    # yData será a primeira coluna da planilha, tendo o formato: {"Nome das linhas": [lista de nomes das linhas]}
    #print(f'{name} -> {yData, xData}')

    df = {
        f"{name}": list(yData.values())[0],
    }

    if type == "turm":
        for day in ['2','3','4','5','6']:
            df[day] = []
            for hour in list(yData.values())[0]:
                df[day].append('-')
                if not str(xData[day]).find(f"\'{hour}-") == -1:
                    df[day][int(hour)-1] = str(xData[day])[str(xData[day]).find(f"-", str(xData[day]).find(f"\'{hour}-")) + 1:str(xData[day]).find(f"'", str(xData[day]).find(f"\'{hour}-")+1)]

    #elif type == "teacher":


    df = pd.DataFrame(data=df)
    print(df)
    df.to_excel(f"{path}{type}/{name}.xlsx", index=False)
