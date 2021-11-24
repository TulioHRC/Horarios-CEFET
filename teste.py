# Importando bibliotecas
import random
import pandas as pd
# Demonstrando utilização do pandas

df = pd.read_excel('Planilha.xlsx', 'Sheet1') # Lendo a planilha do excel, e Sheet1 é o nome da aba do excel para ler
######## Classes
"""
class Teacher:
    def __init__(self, name, subject, prefers, limits, classes):
        self.name = name
        self.subjects = [subject] # Formato = ['{subject}{year}']
        self.prefers = [prefers] # Formato = ['{subject}:{prefers}']
        self.limits = limits
        self.classes = classes # Formato = ['{turma}{ano}-{número de horários}', ...]

    def bestHour(self, turm, preDefinedHour="", alreadyChose=""): # Definição do melhor horário para o professor

        # Formato dos argumentos: class="{turma}"
        #           preDefinedHour="{day}-{horario de 0 (7:50-8:40) até 9 (16:40-17:30)}"
        #           alreadyChose={'2': '{lista com os números dos horários já escolhidos}', ... (outros dias, até o 6)}

        if preDefinedHour and not f"N{preDefinedHour[0]}" in limits and not f"N{preDefinedHour[0]}" in prefers:
            # Se o horário pré-definido poder (não for proibido pelas limits ou não for preferido)
            return preDefinedHour

        if f'{turm}-0' in self.classes: return 0 # Se não houver horários da turma

        # Pegando o melhor horário possível para o professor
        goodOptions = 0
        for prefer in self.prefers.split('-'):
            if 'S' in prefer and prefer[-1] in alread
            
############# Falta forma de se pegar os "pontos" que o Samuel falou, ou seja, avaliação de cada possibilidade com um valor dependendo das suas
# conveniencias e dificuldades

class Turm:
    def __init__(self, name):
        self.name = name
        self.schedule1 = { # Horários de cada turma
            '2': [],
            '3': [],
            '4': [],
            '5': [],
            '6': [],
        }
        self.schedule2 = self.schedule1.copy() # 2 ano
        self.schedule3 = self.schedule1.copy() # 3 ano
        # Formato dos horários = '{horário de 0 a 9}-{matéria/subject}'


class Room:
    def __init__(self, name, position, limits, preDefinedSchedule={'2': [],'3': [],'4': [],'5': [],'6': [],}):
        self.name = name
        self.position = position
        self.limits = limits
        self.schedule = preDefinedSchedule # Horários de cada sala


####### Runner
# App Imports
#from functions import loadData
#from functions import classes as c

# Dev Imports
import loadData
import classes as c

def mainFunction(): # A função principal do código, que retornará o resultado que nós esperamos

    # =================== Pegando os dados que nós fornecemos
    try:
        teachersData = loadData.getDatabase('Planilha.xlsx')
        teachersColumns = loadData.getDatabase('Planilha.xlsx', get="columns")
        roomsData = loadData.getDatabase('Planilha sala.xlsx')
    except Exception as e:
        print(f"Houve um erro ao tentar pegar os dados das planilhas.\n{e}")

    # ==================== Processando os dados para deixa-los melhor de mexer

    classes = [] # -- Turmas

    for i in range(5, len(teachersColumns)): # Pega apenas as matérias
        classes.append(teachersColumns[i])

    for index, turm in enumerate(classes): # Transforma cada turma em um objeto de uma classe
        classes[index] = c.Turm(turm)

    teachers = [] # -- Lista de objetos (professores)
    teachersNames = []

    for index, teacher  in enumerate(teachersData["Professor"]): # Transforma cada professor em um objeto de uma classe
        # Aulas por professor em cada turma
        teachersClasses = []
        for turm in classes:
            teachersClasses.append(f'{turm.name}{teachersData["Ano"][index]}-{int(teachersData[f"{turm.name}"][index])}')


        teachers.append(c.Teacher(teacher, f"{teachersData["Materia"][index]}{teachersData["Ano"][index]}", f"{teachersData["Materia"][index]}:{teachersData["Preferencias"][index]}", teachersData["Limitacoes"][index], teachersClasses))
        print(teachers[index].subjects)

    rooms = [] # -- Salas

    for index, room in enumerate(roomsData["Sala"]):
        rooms.append(c.Room(room, roomsData["Local"][index], roomsData["Limitacoes"][index]))

    # ====================== Gerando o resultado dos melhores horários

    for teacher in teachers:
        for turm in classes:

            resp = teacher.bestHour(turm.name, alreadyChose=turm.schedule) # Melhor horário para cada turma

            print(resp)

            if resp == 0: continue # Pula professor, não tem aula nessa matéria


mainFunction()


##### LoadData
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
"""