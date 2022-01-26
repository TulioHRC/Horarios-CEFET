from functions import loadData
from functions import classes as c
from functions import result
import random

NUMERO_DE_REPETIÇÕES = 10

def mainFunction():  # A função principal do código, que retornará o resultado que nós esperamos
    # =================== Pegando os dados que nós fornecemos
    try:
        teachersData = loadData.getDatabase('Planilha.xlsx')  # Leitura inicial da planilha excel
        teachersColumns = loadData.getDatabase('Planilha.xlsx', get="columns")
        # roomsData = loadData.getDatabase('Planilha sala.xlsx')
        pointsData = loadData.getPoints('./data/preferencias.txt')  # Leitura das pontuações para o cost
    except Exception as e:
        print(f"Houve um erro ao tentar pegar os dados das planilhas.\n{e}")

    # ==================== Processando os dados para deixa-los melhor de mexer

    classesNames = []  # -- Turmas
    classes = []  # Lista de objetos de cada turma

    for i in range(7, len(teachersColumns)):  # Pega apenas as matérias
        classesNames.append(teachersColumns[i])

    for index, turm in enumerate(classesNames):  # Transforma cada turma em um objeto de uma classe
        for i in range(1, 4):  # Turma para cada ano
            for group in ['A', 'B']:  # Adiciona os subgrupos A e B para todas as turmas
                classes.append(c.Turm(turm, str(i), group))

    teachersNames = []  # -- Professores
    teachers = []  # Lista de objetos de cada professor

    for index, teacher in enumerate(teachersData["Professor"]):  # Transforma cada professor em um objeto de uma classe
        horaries = {}  # Horários para cada turma e matéria
        for i in range(7, len(teachersColumns)):
            horaries[
                f"{teachersColumns[i]}-" + f'{teachersData["Ano"][index]}' + f'{teachersData["Sub-Grupo"][index]}'] = int(
                teachersData[f"{teachersColumns[i]}"][index])

        if not (teacher in teachersNames):
            teachers.append(c.Teacher(teacher,
                                      f'{teachersData["Materia"][index]}-{teachersData["Ano"][index]}{teachersData["Sub-Grupo"][index]}',
                                      f'{teachersData["Tipo"][index]}',
                                      str(teachersData["Preferencias"][index]).split('-'),
                                      str(teachersData["Limitacoes"][index]).split('-'), horaries))
            teachersNames.append(teacher)
        else:
            teachers[teachersNames.index(teacher)].subjects.append(
                f'{teachersData["Materia"][index]}-{teachersData["Ano"][index]}{teachersData["Sub-Grupo"][index]}')
            teachers[teachersNames.index(teacher)].types.append(f'{teachersData["Tipo"][index]}')
            teachers[teachersNames.index(teacher)].prefers.append(str(teachersData["Preferencias"][index]).split('-'))
            teachers[teachersNames.index(teacher)].limits.append(str(teachersData["Limitacoes"][index]).split('-'))
            teachers[teachersNames.index(teacher)].horaries[f'{teachersData["Materia"][index]}'] = horaries

        # print(f'{teachers[teachersNames.index(teacher)].name}, {teachers[teachersNames.index(teacher)].horaries}')

    for professor in teachers:
        horarios = professor.horaries
        for h in horarios.items():
            materia = h[0]
            for turma in h[1].items():
                turma_do_horario = turma[0]
                for time in range(0, turma[1]):
                    ho = c.Horario(professor, materia,turma) # Objeto do horário
                    professor.h_individuais.append(ho) # Uma lista com todos os objetos Horario do professor []

    # ==================== Processando os dados: Gerando a planilha final com base nos dados

    for time in range(0, NUMERO_DE_REPETIÇÕES):
        # Embaralha a lista de professores
        lista_embaralhada = teachers.copy()
        random.shuffle(lista_embaralhada)

        # Quadro de horários em branco
        quadro = {}
        for turm in classes:
            quadro[turm.name] = {
                '2': [[0,0,0,0,0], [0,0,0,0,0]], # manhã e tarde
                '3': [[0,0,0,0,0], [0,0,0,0,0]],
                '4': [[0,0,0,0,0], [0,0,0,0,0]],
                '5': [[0,0,0,0,0], [0,0,0,0,0]],
                '6': [[0,0,0,0,0], [0,0,0,0,0]]
            }

            """
            [0, 1, 0, 4, 0]
            [-, A, -, B, -] +4 +1
            """
            # Preencher horários já preenchidos com algo diferente de 0

        while len(lista_embaralhada) != 0:
            # Retiro o primeiro item da lista e o coloco na variável teacher
            teacher = lista_embaralhada[0].copy()
            lista_embaralhada = lista_embaralhada[1:]
            # lista com os objetos horários do professores
            h_professor = teacher.h_individuais.copy()

            for horario in h_professor:
                # Seleciono qual o melhor estado para aquele horário
                position = getBetterHour() # 'day-hour-turm-room'
                position_info = position.split('-')

                # Coloco o horário naquela posição
                quadro[position_info[2]][position_info[0]][position_info[1]] = horario

    """
    - Get Better (Túlio)
    - Avaliação dos Custo (Túlio)
        valido(horário) => horario -> matéria -> salas que podem ser dadas essa matéria -> horários ocupados nessa sala (Samuelsu)
            se for inválido retorna -99
            else, retorna 0

    - Salas desde o app e planilha até a parte lógica (depois)
    """

    # ====================== Criando planilhas
    for turm in classes:
        result.saveSheet(turm.name, turm.schedule, type='turm')
    for teacher in teachers:
        result.saveSheet(teacher.name, teacher.schedule, type='teacher')
