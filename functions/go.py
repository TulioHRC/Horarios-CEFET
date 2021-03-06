from functions import loadData
from functions import classes as c
from functions import result
from functions import logic
import random
import copy

NUMERO_DE_REPETIÇÕES = 100


def restartObjects(listO):
    for t in listO:
        t.schedule = {
            '2': [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],  # manhã e tarde
            '3': [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
            '4': [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
            '5': [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
            '6': [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
        }

    return listO


def mainFunction():  # A função principal do código, que retornará o resultado que nós esperamos
    # =================== Pegando os dados que nós fornecemos
    try:
        teachersData = loadData.getDatabase('Planilha.xlsx')  # Leitura inicial da planilha
        teachersColumns = loadData.getDatabase('Planilha.xlsx', get="columns")
        roomsData = loadData.getDatabase('Planilha sala.xlsx') # Leitura inicial da planilha de salas
        pointsData = loadData.getPoints('./data/preferencias.txt')  # Leitura das pontuações para o cost
    except Exception as e:
        print(f"Houve um erro ao tentar pegar os dados das planilhas.\n{e}")

    # ==================== Processando os dados para deixa-los melhor de mexer

    classesNames = []  # -- Turmas
    classes = []  # Lista de objetos de cada turma

    for i in range(8, len(teachersColumns)):  # Pega apenas as matérias
        classesNames.append(teachersColumns[i])

    for index, turm in enumerate(classesNames):  # Transforma cada turma em um objeto de uma classe
        for i in range(1, 4):  # Turma para cada ano
            for group in ['A', 'B']:  # Adiciona os subgrupos A e B para todas as turmas
                classes.append(c.Turm(turm, str(i), group))

    teachersNames = []  # -- Professores
    teachers = []  # Lista de objetos de cada professor

    for index, teacher in enumerate(teachersData["Professor"]):  # Transforma cada professor em um objeto de uma classe
        horaries = {}  # Horários para cada turma e matéria
        for i in range(8, len(teachersColumns)):
            horaries[
                f"{teachersColumns[i]}-" + f'{teachersData["Ano"][index]}' + f'{teachersData["Sub-Grupo"][index]}'] = int(
                teachersData[f"{teachersColumns[i]}"][index])

        if not (teacher in teachersNames):
            teachers.append(c.Teacher(teacher,
                                      f'{teachersData["Materia"][index]}-{teachersData["Ano"][index]}{teachersData["Sub-Grupo"][index]}',
                                      f'{teachersData["Tipo"][index]}',
                                      str(teachersData["Preferencias"][index]).split('-'),
                                      str(teachersData["Limitacoes"][index]).split('-'),
                                      str(teachersData["Bimestral"][index]), horaries))
            teachersNames.append(teacher)
        else:
            teachers[teachersNames.index(teacher)].subjects.append(
                f'{teachersData["Materia"][index]}-{teachersData["Ano"][index]}{teachersData["Sub-Grupo"][index]}')
            teachers[teachersNames.index(teacher)].types.append(f'{teachersData["Tipo"][index]}')
            teachers[teachersNames.index(teacher)].prefers.append(str(teachersData["Preferencias"][index]).split('-'))
            teachers[teachersNames.index(teacher)].limits.append(str(teachersData["Limitacoes"][index]).split('-'))
            teachers[teachersNames.index(teacher)].bimestral.append(int(str(teachersData["Bimestral"][index])[0]))
            teachers[teachersNames.index(teacher)].horaries[
                f'{teachersData["Materia"][index]}-{teachersData["Ano"][index]}{teachersData["Sub-Grupo"][index]}'] = horaries

        # print(f'{teachers[teachersNames.index(teacher)].name}, {teachers[teachersNames.index(teacher)].horaries}')

    for professor in teachers:
        horarios = professor.horaries
        for h in horarios.items():
            materia = h[0]
            for turma in h[1].items():
                turma_do_horario = turma[0]
                for time in range(0, turma[1]):
                    ho = c.Horario(professor, materia, turma)  # Objeto do horário
                    professor.h_individuais.append(ho)  # Uma lista com todos os objetos Horario do professor []

    roomsNames = roomsData['Sala'] # -- Salas
    rooms = []

    for index, room in enumerate(roomsNames):  # Transforma cada turma em um objeto de uma classe
        rooms.append(c.Room(room, roomsData['Local'][index], roomsData['Limitacoes'][index]))

    # ==================== Processando os dados: Gerando a planilha final com base nos dados

    bestSchedule = []
    # Duplicar os objetos professores e manipular apenas umgrupo nessa parte a baixo
    for time in range(0, NUMERO_DE_REPETIÇÕES):
        teachers_copy = restartObjects(teachers)

        # Embaralha a lista de professores
        lista_embaralhada = teachers.copy()
        random.shuffle(lista_embaralhada)

        # Quadro de horários em branco
        quadro = {}
        for turm in classes:
            quadro[turm.name] = {
                '2': [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],  # manhã e tarde
                '3': [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
                '4': [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
                '5': [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
                '6': [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
            }

            # Preencher horários já preenchidos com algo diferente de 0

        while len(lista_embaralhada) != 0:
            # Retiro o primeiro item da lista e o coloco na variável teacher
            teacher = lista_embaralhada[0]
            lista_embaralhada = lista_embaralhada[1:]
            # lista com os objetos horários do professores
            h_professor = teacher.h_individuais

            for horario in h_professor:
                subjectPos = horario.teacher.subjects.index(f"{horario.subject}")  # -{horario.turm[0].split('-')[1]}")
                typeV = horario.teacher.types[subjectPos]
                typeNum = 0

                if typeV == 'Tarde': typeNum = 1
                # Seleciono qual o melhor estado para aquele horário
                position = logic.getBetterHour(horario, quadro.copy()[horario.turm[0]], subjectPos,
                                               typeNum)  # type é 0 - manha ou 1 - tarde. retorna 'day;hour;turm;room'
                position_info = position.split(';')

                # Coloco o horário naquela posição
                if teacher.bimestral[subjectPos] == 1: # Se horário for bimestral
                    if not(type(quadro[position_info[3]][position_info[0]][typeNum][int(position_info[1])]) is list): # Se no horário não for lista
                        quadro[position_info[3]][position_info[0]][typeNum][int(position_info[1])] = [0, 0, 0, 0]

                    quadro[position_info[3]][position_info[0]][typeNum][int(position_info[1])][int(position_info[2])] = horario
                else:
                    quadro[position_info[2]][position_info[0]][typeNum][int(position_info[1])] = horario

                # Professores
                if teacher.bimestral[subjectPos] == 1: # Se horário for bimestral
                    if not(type(horario.teacher.schedule[position_info[0]][typeNum][int(position_info[1])]) is list): # Se no horário não for lista
                        horario.teacher.schedule[position_info[0]][typeNum][int(position_info[1])] = [0, 0, 0, 0]

                    horario.teacher.schedule[position_info[0]][typeNum][int(position_info[1])][int(position_info[2])] = f"{horario.turm[0]}-{str(horario).split('-')[1]}"

                    teachers_copy[teachersNames.index(horario.teacher.name)].schedule[position_info[0]][typeNum][
                        int(position_info[1])] = list(horario.teacher.schedule[position_info[0]][typeNum][int(position_info[1])])
                else:
                    horario.teacher.schedule[position_info[0]][typeNum][int(position_info[1])] = f"{horario.turm[0]}-{str(horario).split('-')[1]}"

                    teachers_copy[teachersNames.index(horario.teacher.name)].schedule[position_info[0]][typeNum][
                        int(position_info[1])] = f"{horario.turm[0]}-{str(horario).split('-')[1]}"

                # Alterando objeto do professor

        #for turm in classes:
           #print(turm.name, quadro[turm.name])

        pontuacao = logic.cost_board(quadro)

        if time == 0:
            bestSchedule.append([quadro.copy(), pontuacao, copy.deepcopy(teachers_copy)]) # Deep copy to not overwrite
        elif bestSchedule[0][1] == pontuacao:
            bestSchedule.append([quadro.copy(), pontuacao, copy.deepcopy(teachers_copy)])
        elif pontuacao > bestSchedule[0][1]:
            bestSchedule = [[quadro.copy(), pontuacao, copy.deepcopy(teachers_copy)]]

        print(time, pontuacao)

    horarios = random.choice(bestSchedule)
    print(f"Melhor resultado: {horarios[1]}")

    for turm in classes:
        result.saveSheet(turm.name, horarios[0][turm.name], type='turm')
    for teacher in teachers:
        result.saveSheet(teacher.name, horarios[2][teachersNames.index(teacher.name)].schedule, type='teacher')
