from functions import loadData
from functions import classes as c
from functions import result

def mainFunction(): # A função principal do código, que retornará o resultado que nós esperamos

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
        # Aulas por professor em cada turma
        teachersClasses = []
        for turm in classes:
            teachersClasses.append(f'{turm.name}-{int(teachersData[f"{turm.name[0:-3]}"][index])}')

        if not teacher in teachersNames:
            teachers.append(c.Teacher(teacher, f'{teachersData["Materia"][index]}-{teachersData["Ano"][index]}{teachersData["Sub-Grupo"][index]}', f'{teachersData["Tipo"][index]}', str(teachersData["Preferencias"][index]).split('-'), str(teachersData["Limitacoes"][index]).split('-')))
            teachersNames.append(teacher)
        else:
            teachers[teachersNames.index(teacher)].subjects.append(f'{teachersData["Materia"][index]}-{teachersData["Ano"][index]}{teachersData["Sub-Grupo"][index]}')
            teachers[teachersNames.index(teacher)].types.append(f'{teachersData["Tipo"][index]}')
            teachers[teachersNames.index(teacher)].prefers.append(str(teachersData["Preferencias"][index]).split('-'))
            teachers[teachersNames.index(teacher)].limits.append(str(teachersData["Limitacoes"][index]).split('-'))

        # print(f'{teachers[teachersNames.index(teacher)].name}, {teachers[teachersNames.index(teacher)].prefers}\n{teachers[teachersNames.index(teacher)].subjects}')



# ====================== Gerando o resultado dos melhores horários



# ====================== Criando planilhas
    for turm in classes:
        result.saveSheet(turm.name, turm.schedule, type='turm')
    for teacher in teachers:
        result.saveSheet(teacher.name, teacher.schedule, type='teacher')
