import pandas as pd
from functions import convert as conv

def saveSheet(name, xData, yData={"Horarios": ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']}, path="./data/", type="turm", intervals=1):
    # 1 = 7h-7h50, 2 = -8h40, 3 = -9h30, 4(5) = 9h50-10h40, 5(6) = -11h30, 6(7) = -12h20
    # 7(9) = 13h-13h50, 8(10) = -14h40, 9(11) = -15h30, 10(13) = 15h50-16h40, 11(14) = -17h30, 12(15) = -18h20
    # Horários vão até o 14 para acomodar os intervalos, 4 e 12 são intervalos, 8 é o almoço, 16 é o ultimo que não pode ser preenchido (fins de aparência)

    # xData terão o formato: {"COLLUMN 1": [valores], ...}
    # Valores de xData de turma ['2-Desenho Tecnico']; de professores ['2-Desenho Tecnico - MCT-1A']
    # yData será a primeira coluna da planilha, tendo o formato: {"Nome das linhas": [lista de nomes das linhas]}
    #print(f'{name} -> {yData, xData}')

    # Juntar horarios de manhã e tarde (2 listas que estão dentro dos horários, xData)
    for dia in xData.keys():
        xData[dia] = xData[dia][0] + xData[dia][1]

    rows = list(yData.values())[0].copy()

    for index, row in enumerate(rows):
        rows[index] = conv.convertNumToHour(row)

    df = {
        f"{name}": rows,
    }

    if intervals:
        vals = ['Intervalo', 'Almoço']
        hoursPreSelected = [4,8,12]

    for day in ['2','3','4','5','6']:
        dayConv = conv.convertNumToDay(day)
        df[dayConv] = []
        factor = 0 # Se tiver intervalos esta variavel irá aumentar para gerar as separações
        for hour in list(yData.values())[0]: # cada um dos 12 horários do yData
            if not hour == '16': # Não preenchido
                df[dayConv].append('-')
                horario = xData[day][int(hour)-1-factor]

                if intervals and (int(hour) in hoursPreSelected): # Mudar o factor se necessário
                    factor += 1
                    if hour in ['4', '12']: df[dayConv][int(hour)-1] = vals[0]  # Intervalo
                    elif hour in ['8']: df[dayConv][int(hour)-1] = vals[1] # Almoço
                elif horario: # Se não for 0
                    if type == "turm":
                        horario = str(horario)[0:-3]
                    df[dayConv][int(hour)-1] = str(horario)
            else:
                df[dayConv].append('')


    df = pd.DataFrame(data=df)
    df.to_excel(f"{path}{type}/{name}.xlsx", index=False)
