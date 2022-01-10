from functions import loadData
from functions import classes as c
from functions import result
import random

NUMERO_DE_REPETIÇÕES = 10

def mainFunction():  # A função principal do código, que retornará o resultado que nós esperamos
    # =================== Pegando os dados que nós fornecemos
    try:
        teachersData = loadData.getDatabase('Planilha.xlsx') # Leitura inicial da planilha excel
        teachersColumns = loadData.getDatabase('Planilha.xlsx', get="columns")
        #roomsData = loadData.getDatabase('Planilha sala.xlsx')
        pointsData = loadData.getPoints('./data/preferencias.txt') # Leitura das pontuações para o cost
    except Exception as e:
        print(f"Houve um erro ao tentar pegar os dados das planilhas.\n{e}")


    # ==================== Processando os dados para deixa-los melhor de mexer

    classesNames = [] # -- Turmas
    classes = [] # Lista de objetos de cada turma

    for i in range(7, len(teachersColumns)): # Pega apenas as matérias
        classesNames.append(teachersColumns[i])

    for index, turm in enumerate(classesNames): # Transforma cada turma em um objeto de uma classe
        for i in range(1, 4): # Turma para cada ano
            for group in ['A', 'B']: # Adiciona os subgrupos A e B para todas as turmas
                classes.append(c.Turm(turm, str(i), group))

    teachersNames = [] # -- Professores
    teachers = [] # Lista de objetos de cada professor

    for index, teacher  in enumerate(teachersData["Professor"]): # Transforma cada professor em um objeto de uma classe
        horaries = {} # Horários para cada turma e matéria
        for i in range(7, len(teachersColumns)):
            horaries[f"{teachersColumns[i]}-" + f'{teachersData["Ano"][index]}' + f'{teachersData["Sub-Grupo"][index]}'] = int(teachersData[f"{teachersColumns[i]}"][index])

        if not teacher in teachersNames:
            teachers.append(c.Teacher(teacher, f'{teachersData["Materia"][index]}-{teachersData["Ano"][index]}{teachersData["Sub-Grupo"][index]}', f'{teachersData["Tipo"][index]}', str(teachersData["Preferencias"][index]).split('-'), str(teachersData["Limitacoes"][index]).split('-'), horaries))
            teachersNames.append(teacher)
        else:
            teachers[teachersNames.index(teacher)].subjects.append(f'{teachersData["Materia"][index]}-{teachersData["Ano"][index]}{teachersData["Sub-Grupo"][index]}')
            teachers[teachersNames.index(teacher)].types.append(f'{teachersData["Tipo"][index]}')
            teachers[teachersNames.index(teacher)].prefers.append(str(teachersData["Preferencias"][index]).split('-'))
            teachers[teachersNames.index(teacher)].limits.append(str(teachersData["Limitacoes"][index]).split('-'))
            teachers[teachersNames.index(teacher)].horaries[f'{teachersData["Materia"][index]}'] = horaries


        # print(f'{teachers[teachersNames.index(teacher)].name}, {teachers[teachersNames.index(teacher)].horaries}')

    # ==================== Processando os dados: Gerando a planilha final com base nos dados

    for c in range(0, NUMERO_DE_REPETIÇÕES):


        random.shuffle(teachers)

        for professor in teachers:
            horarios = professor.horaries
            for h in horarios.items():
                materia = h[0]
                for turma in h[1].items():
                    turma_do_horario = turma[0]
                    for c in range(0, turma[1]):
                        professor.h_individuais.append(f'{professor}-{turma}-{materia}')
            print(professor.h_individuais)

        while len(lista_embaralhada) != 0:
            # Retiro o primeiro item da lista e o coloco na variável node
            horario = lista_embaralhada[0]
            lista_embaralhada = lista_embaralhada[1:]
            # Seleciono qual o melhor estado para aquele node e o coloco nele
    # ====================== Criando planilhas
    for turm in classes:
        result.saveSheet(turm.name, turm.schedule, type='turm')
    for teacher in teachers:
        result.saveSheet(teacher.name, teacher.schedule, type='teacher')
