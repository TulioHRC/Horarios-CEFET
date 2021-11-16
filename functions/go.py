# App Imports
#from functions import loadData
#from functions import classes as c

# Dev Imports
import loadData
import classes as c

def mainFunction(): # A função principal do código, que retornará o resultado que nós esperamos

    # Pegando os dados que nós fornecemos
    try:
        teachersData = loadData.getDatabase('Planilha.xlsx')
        teachersColumns = loadData.getDatabase('Planilha.xlsx', get="columns")
        roomsData = loadData.getDatabase('Planilha sala.xlsx')
    except Exception as e:
        print(f"Houve um erro ao tentar pegar os dados das planilhas.\n{e}")

    # Processando os dados para deixa-los melhor de mexer

    classes = [] # Turmas

    for i in range(5, len(teachersColumns)): # Pega apenas as matérias
        classes.append(teachersColumns[i])

    for index, turm in enumerate(classes): # Transforma cada turma em um objeto de uma classe
        classes[index] = c.Turm(turm)

    teachers = [] # Lista de objetos (professores)

    for index, teacher  in enumerate(teachersData["Professor"]): # Transforma cada professor em um objeto de uma classe
        # Aulas por professor em cada turma
        teachersClasses = []
        for turm in classes:
            teachersClasses.append(f'{turm.name}-{int(teachersData[f"{turm.name}"][index])}')

        teachers.append(c.Teacher(teacher, teachersData["Materia"][index], teachersData["Ano"][index], teachersData["Preferencias"][index], teachersData["Limitacoes"][index], teachersClasses))

    # Gerando o resultado dos melhores horários

    for teacher in teachers:
        for turm in classes:
            teacher.bestHour(turm.name) # Melhor horário para cada turma


mainFunction()
