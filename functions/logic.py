# Arquivo com as funções envolvendo a lógica do nosso programa

import random
from functions import loadData

"""
Regras Básicas:
- não mudar o board dentro das funções
"""


def getBetterHour(horario, board, subjectPos, typeNum):
    quadro = board.copy()
    betterH = [['', -99]]  # (day;hour, pontuação), melhores horários
    # Se for horário bimestral será (day;hour;bimestre, pontuação)

    teacher = horario.teacher
    turm = horario.turm
    subject = horario.subject

    for d in range(2, 7):  # para cada dia
        d = str(d)
        for h in range(0, 6):  # para cada horário no dia
            pontuation = validation(horario, [d, h], quadro, subjectPos, typeNum)  # -------------- Verificado
            if pontuation == 0:
                pontuation = cost_individual(horario, [d, h], quadro, subjectPos, typeNum)
                if pontuation > betterH[0][1]:
                    betterH = [[f'{d};{h}', pontuation]]
                elif pontuation == betterH[0][1]:
                    betterH.append([f'{d};{h}', pontuation])
            # else:
            # print(d, h, pontuation, teacher.name, turm)

    return f"{random.choice(betterH)[0]};{turm[0]}"  # Retorna f'{day};{hour};{turm}' depois nós colocaremos a room variable


def cost_individual(horario, position, board, subjectPos, typeNum, sala=''):
    points = loadData.getPoints('./data/preferencias.txt')
    pointsKeys = points.keys()

    pontuation = 0
    dayBoard = board[position[0]][typeNum]
    teacherDayBoard = horario.teacher.schedule[position[0]][typeNum]

    horariosPreenchidos = 0  # Horarios já preenchidos no dia
    horariosP = 0  # Horarios já preenchidos no dia para os professores

    for p in pointsKeys:
        if p == "nHorariosDia":  # Para a quantidade de horários já preenchidos no dia
            for h in dayBoard:
                if h != 0:
                    horariosPreenchidos += 1
                    pontuation += points[p]
            for h in teacherDayBoard:
                if h != 0:
                    horariosP += 1
                    pontuation += points[p]
        elif p == "tresHorariosDia":
            if horariosPreenchidos >= 3: pontuation += points[p]  # Da turma
            if horariosP >= 3: pontuation += points[p]  # Do professor
        elif p == "horariosPoints":
            if position[1] in [0, 5]:
                pontuation += points[p]
        elif p == "lastResp": # Se o horário for ao lado de outro da mesma matéria
            if position[1] != 0:
                if dayBoard[position[1] - 1] != 0:
                    if dayBoard[position[1] - 1].subject == horario.subject: pontuation += points[p]
            if position[1] != 5:
                if dayBoard[position[1] + 1] != 0:
                    if dayBoard[position[1] + 1].subject == horario.subject: pontuation += points[p]
        elif p == "preferPositiva":  # negativa e positiva para diminuir código
            for prefer in horario.teacher.prefers[subjectPos]:  # para cada limitação do professor
                if f'N{position[0]}' in str(prefer) or f'S{position[0]}' in str(prefer):  # Se a limitação estiver no dia do horário
                    try:
                        limite_inferior = int(prefer.split(':')[1].split(',')[0])
                        limite_superior = int(prefer.split(':')[1].split(',')[1])
                        if typeNum == 1: # tarde, diminui em 6 para a avaliação dentro apenas do turno
                            limite_inferior -= 6
                            limite_superior -= 6
                    except:  # Considerando o caso de não ter selecionado uma variação de horários
                        limite_inferior = 1
                        limite_superior = 12

                    if (limite_inferior <= int(position[1]) + 1) and (limite_superior >= int(
                            position[1]) + 1):  # Se o horário estiver compreendido durante a limitação
                        if str(prefer)[0] == 'S':
                            pontuation += points['preferPositiva']
                        else:
                            pontuation += points['preferNegativa']
        # print(pontuation)

    return pontuation


def cost_board(board):
    # Vamos calcular uma vez para cada bimestre como se fosse um quadr a parte
    points = loadData.getPoints('./data/preferencias.txt')

    media = 0
    for b in range(0, 4):
        result_value = 0
        for quadro in board.values():  # Para cada turma
            for day in quadro.values():  # Para cada dia nesta turma
                typeNum = 0 # qual turno (0 manhã, 1 tarde)
                for turno in day:  # Para manhã e depois tarde
                    num_of_0 = 0

                    for h in turno:
                        if type(h) is list:
                            if h[b] == 0:
                                num_of_0 += 1
                        elif h == 0:
                            num_of_0 += 1
                    # Pontuação para cada dia já preenchido
                    result_value += (6 - num_of_0) * points['nHorariosDia']

                    # Pontuação para mais de 3 horários já preenchidos no mesmo dia
                    if num_of_0 < 3:
                        result_value += points['tresHorariosDia']

                    # Primeiros e últimos horários do turno
                    if type(turno[0]) is list:
                        if turno[0][b] != 0:
                            result_value += points['horariosPoints']
                    elif turno[0] != 0:
                        result_value += points['horariosPoints']

                    if type(turno[5]) is list:
                        if turno[5][b] != 0:
                            result_value += points['horariosPoints']
                    elif turno[5] != 0:
                        result_value += points['horariosPoints']

                    # Horários de mesma matéria agrupados
                    for h in range(0, len(turno)):
                        if (h != 5):
                            if turno[h] != 0 and turno[h+1] != 0:
                                actual = turno[h] if not(type(turno[h]) is list) else turno[h][b]
                                prox = turno[h+1] if not(type(turno[h]) is list) else turno[h][b]
                                if actual != 0 and prox != 0:
                                    if actual.subject == prox.subject:
                                        result_value += points['lastResp']
                    """for h in range(0, len(turno)):
                        if h != 5:
                            if turno[h] != 0 and turno[h + 1] != 0:
                                if str(type(turno[h])) == "<class 'list'>":
                                    for h_bimestral in range(0, 4):
                                        if str(type(turno[h + 1])) == "<class 'list'>":
                                            if turno[h][h_bimestral].subject == turno[h + 1][h_bimestral].subject:
                                                result_value += points['lastResp']
                                elif turno[h].subject == turno[h + 1].subject:
                                    result_value += points['lastResp']
                    """
                    # Professor dando aula no dia que ele quer
                    for h in range(0, len(turno)):
                        hor = turno[h] if not(type(turno[h]) is list) else turno[h][b]
                        if hor != 0:  # Horários do turno (manhã ou tarde)
                            for prefers in hor.teacher.prefers:
                                for p in prefers:  # para cada limitação do professor
                                    if f'N{day}' in str(p) or f'S{day}' in str(p):  # Se a limitação estiver no dia do horário
                                        try:
                                            limite_inferior = int(p.split(':')[1].split(',')[0])
                                            limite_superior = int(p.split(':')[1].split(',')[1])
                                            if typeNum == 1:
                                                limite_inferior -= 6
                                                limite_superior -= 6
                                        except:  # Considerando o caso de não ter selecionado uma variação de horários
                                            limite_inferior = 1
                                            limite_superior = 12

                                        if (limite_inferior <= int(h) + 1) and (limite_superior >= int(h) + 1):  # Se o horário estiver compreendido durante a limitação
                                            if str(p)[0] == 'S':
                                                result_value += points['preferPositiva']
                                            else:
                                                result_value += points['preferNegativa']
                    typeNum += 1
        media += result_value
    return (media/4)



def validation(horario, position, board, subjectPos, typeNum, sala=''):  # board é o quadro de horários
    # Position = [day, hour]

    INVALIDO = -99

    # h_room = sala    # Sala
    h_day = position[0]   # Dia
    h_time = position[1]  # Horário

    # Limitações do professor
    limitation = horario.teacher.limits[subjectPos]
    t_limitations = []  # N3:1,4

    for l in limitation:  # para cada limitação do professor
        if f'N{h_day}' in str(l):  # Se a limitação estiver no dia do horário
            try:
                limite_inferior = int(l.split(':')[1].split(',')[0])
                limite_superior = int(l.split(':')[1].split(',')[1])
                if typeNum == 1:
                    limite_inferior -= 6
                    limite_superior -= 6
            except:  # Considerando o caso de não ter selecionado uma variação de horários
                limite_inferior = 1
                limite_superior = 12

            if (limite_inferior <= int(h_time) + 1) and (limite_superior >= int(h_time) + 1):  # Se o horário estiver compreendido durante a limitação
                return INVALIDO

    # Limitações da sala
    # room_invalids_h =

    # Horário já está ocupado por outro no Quadro de horários?
    if board[str(h_day)][typeNum][h_time] != 0: # Se horário preenchido 
        if board[str(h_day)][typeNum][h_time] is list and horario.teacher.bimestral[subjectPos] == 1: # Se horário preenchido for lista e o 
            # horário for bimestral

            if len(board[str(h_day)][typeNum][h_time]) != 4: # Se horário lista estiver completamente preenchido
                return INVALIDO

        else: return INVALIDO

    # Verificar também a parte dos professores
    if horario.teacher.schedule[str(h_day)][typeNum][h_time] != 0: # Se horário preenchido 
        if horario.teacher.schedule[str(h_day)][typeNum][h_time] is list and horario.teacher.bimestral[subjectPos] == 1: # Se horário preenchido for lista e o 
            # horário for bimestral

            if len(horario.teacher.schedule[str(h_day)][typeNum][h_time]) != 4: # Se horário lista estiver completamente preenchido
                return INVALIDO

        else: return INVALIDO

    # Não pode trabalhar mais de 8h no mesmo dia
    horaries_in_day = horario.teacher.schedule[position[0]]
    bimestral_h = [] # horários bimestrais
    num_h = 0 # numero de horários
    for h in horaries_in_day:
        if type(h) is list:
            bimestral_h.append(h)
        elif h != 0:
            num_h += 1
    max_value = 0
    for c in range(0, 4):
        num_h_bimestral = 0
        for h in bimestral_h:
            if h[c] != 0:
                num_h_bimestral += 1
        max_value = num_h_bimestral if num_h_bimestral >= max_value else max_value
    num_h = num_h + max_value
    if num_h >= 10:
        return INVALIDO

    # Não pode ter um intervalo entre uma aula e outra maior que 3h
    """
    h_teacher = horario.teacher.schedule
    h_in_day = h_teacher[0] + h_teacher[1]
    free_time = 0 # In minutes
    for c in range(0, 12):
        if c == 3 or c == 9:
            free_time += 20
        elif c == 6:
            free_time += 40
        # Tempo livre que provem de horários vagos
        if h_in_day[c] == 0:
            free_time += 50
            if free_time >= 180:
                return INVALIDO

        elif str(type(h_in_day[c])) == "<class 'list'>":
            bimestral_free_time = 0
            for i in range(0, 4):
                current = h_in_day[c]
                a = c
                while str(type(current)) == "<class 'list'>":
                    bimestral_free_time = bimestral_free_time + 50 if current[i] == 0 else 0
                    a += 1
                    current = h_in_day[a]
                    if bimestral_free_time + free_time >= 180:
                        return INVALIDO

            for i in range(0, 4):
                if h_in_day[c][i] == 0:
                    zero_in_sequence += 1
                    if h_in_day[c + 1][i] == 0:
                        zero_in_sequence += 1
                        if h_in_day[c + 2][i] == 0:
                            zero_in_sequence += 1
                    else:
                        zero_in_sequence = 0

            for thing in range(0, 4):
                if h_in_day[c][thing] == 0:
                    zero_in_sequence += 1
                    if zero_in_sequence >= 3:
                        return INVALIDO
                    if h_in_day[c][thing + 1] == 0 or (h_in_day[c + 1] == 0):
                        zero_in_sequence += 1
                        c += 1
                        if zero_in_sequence >= 3:
                            return INVALIDO"""


    # Devem ser ao menos 11h entre o primeiro e o último horário de descanso
    # Status: aguardando reunião, atualmente seria impossível o estado acima citado não ser válido
    return 0
