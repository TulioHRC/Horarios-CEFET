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

    for i in range(6, len(teachersColumns)): # Pega apenas as matérias
        classes.append(teachersColumns[i])

    for index, turm in enumerate(classes): # Transforma cada turma em um objeto de uma classe
        for i in range(1, 4): # Turma para cada ano
            classes[index] = c.Turm(turm, str(i))

    teachers = [] # -- Lista de objetos (professores)
    teachersNames = []

    for index, teacher  in enumerate(teachersData["Professor"]): # Transforma cada professor em um objeto de uma classe
        # Aulas por professor em cada turma
        teachersClasses = []
        for turm in classes:
            teachersClasses.append(f'{turm.name}-{int(teachersData[f"{turm.name[0:-3]}"][index])}')

        if not teacher in teachersNames:
            teachers.append(c.Teacher(teacher, f'{teachersData["Materia"][index]}:{teachersData["Ano"][index]}', f'{teachersData["Tipo"][index]}', f'{teachersData["Materia"][index]}:{teachersData["Preferencias"][index]}', teachersData["Limitacoes"][index], teachersClasses))
            teachersNames.append(teacher)
        else:
            teachers[teachersNames.index(teacher)].subjects.append(f'{teachersData["Materia"][index]}:{teachersData["Ano"][index]}')
            teachers[teachersNames.index(teacher)].types.append(f'{teachersData["Tipo"][index]}')
            teachers[teachersNames.index(teacher)].prefers.append(f'{teachersData["Materia"][index]}:{teachersData["Preferencias"][index]}')
            teachers[teachersNames.index(teacher)].limits  = teachersData["Limitacoes"][index] # Substitui pela mais recente
            teachers[teachersNames.index(teacher)].classes.append(teachersClasses)

        # Print de teste - print(f'{teachers[teachersNames.index(teacher)].name}, {teachers[teachersNames.index(teacher)].types}\n{teachers[teachersNames.index(teacher)].classes}')

    rooms = [] # -- Salas

    for index, room in enumerate(roomsData["Sala"]):
        rooms.append(c.Room(room, roomsData["Local"][index], roomsData["Limitacoes"][index]))

    # ====================== Gerando o resultado dos melhores horários

    for teacher in teachers:
        for subject in teacher.subjects: # Por matéria do professor
            for turm in classes:
                resp = teacher.bestHour(turm, subject, alreadyChose=turm.schedule) # Melhor horário para cada turma
                #print(resp)
                if resp == 0: continue # Pula professor, não tem aula nessa matéria

mainFunction()
