# Arquivo com as funções envolvendo a lógica do nosso programa

import random
from functions import loadData

"""
Regras Básicas:
- não mudar o board dentro das funções
"""

def getBetterHour(horario, board, subjectPos, typeNum):
    quadro = board.copy()
    betterH = [['', -99]] # (day;hour, pontuação), melhores horários

    teacher = horario.teacher
    turm = horario.turm
    subject = horario.subject

    for d in range(2,7): # para cada dia
        d = str(d)
        for h in range(0, 5): # para cada horário no dia
            pontuation = validation(horario, [d, h], quadro, subjectPos, typeNum) # -------------- Verificado
            if pontuation == 0:
                pontuation = cost_individual(horario, [d, h], quadro, subjectPos, typeNum)
                if pontuation > betterH[0][1]:
                    betterH = [[f'{d};{h}', pontuation]]
                elif pontuation == betterH[0][1]:
                    betterH.append([f'{d};{h}', pontuation])
            #else:
                #print(d, h, pontuation, teacher.name, turm)

    return f"{random.choice(betterH)[0]};{turm[0]}" # Retorna f'{day};{hour};{turm}' depois nós colocaremos a room variable


def cost_individual(horario, position, board, subjectPos, typeNum, sala=''):
    points = loadData.getPoints('./data/preferencias.txt')
    pointsKeys = points.keys()

    pontuation = 0
    dayBoard = board[position[0]][typeNum]

    horariosPreenchidos = 0 # Horarios já preenchidos no dia

    for p in pointsKeys:
        if p == "nHorariosDia": # Para a quantidade de horários já preenchidos no dia
            for h in dayBoard:
                if h != 0:
                    horariosPreenchidos += 1
                    pontuation += points[p]
        elif p == "tresHorariosDia":
            if horariosPreenchidos >= 3: pontuation += points[p]
        elif p == "horariosPoints":
            if position[1] in [0, 4]:
                pontuation += points[p]
        elif p == "lastResp":
            if position[1] != 0:
                if dayBoard[position[1]-1] != 0:
                    if dayBoard[position[1]-1].subject == horario.subject: pontuation += points[p]
            if position[1] != 4:
                if dayBoard[position[1]+1] != 0:
                    if dayBoard[position[1]+1].subject == horario.subject: pontuation += points[p]
        elif p == "preferPositiva": # negativa e positiva para diminuir código
            for prefer in horario.teacher.prefers[subjectPos]: # para cada limitação do professor
                if f'N{position[0]}' in str(prefer) or f'S{position[0]}' in str(prefer): # Se a limitação estiver no dia do horário
                    try:
                        limite_inferior = int(prefer.split(':')[1].split(',')[0])
                        limite_superior = int(prefer.split(':')[1].split(',')[1])
                        if typeNum == 1:
                            limite_inferior -= 5
                            limite_superior -= 5
                    except: # Considerando o caso de não ter selecionado uma variação de horários
                        limite_inferior = 1
                        limite_superior = 10

                    if (limite_inferior <= int(position[1])+1) and (limite_superior >= int(position[1])+1): # Se o horário estiver compreendido durante a limitação
                        if str(prefer)[0] == 'S': pontuation += points['preferPositiva']
                        else: pontuation += points['preferNegativa']

        #print(pontuation)

    return pontuation


def cost_board(board):
    points = loadData.getPoints('./data/preferencias.txt')

    result_value = 0
    for quadro in board.values(): # Para cada turma
        for day in quadro.values(): # Para cada dia nesta turma
            t = 0
            for turno in day: # Para manhã e depois tarde
                num_of_0 = turno.count(0)
                # Pontuação para cada dia já preenchido
                result_value += (5 - num_of_0) * points['nHorariosDia']

                # Pontuação para mais de 3 horários já preenchidos no mesmo dia
                if num_of_0 < 3:
                    result_value += points['tresHorariosDia'] # * 5 # ???????? Não precisaria multiplicar por 5

                # Primeiros e últimos horários do turno
                if turno[0] != 0:
                    result_value += points['horariosPoints']
                if turno[4] != 0:
                    result_value += points['horariosPoints']

                # Horários de mesma matéria agrupados
                for h in range(0, len(turno)):
                    """ Acho que não seria assim
                    if (h != 0) and (turno[h].subject == turno[h + 1].subject):
                            result_value += points['lastResp']
                    """
                    if (h != 4):
                        if turno[h] != 0 and turno[h+1] != 0: # ?????? Evitar erros na lógica seguinte
                            if turno[h].subject == turno[h + 1].subject:
                                result_value += points['lastResp']

                # Professor dando aula no dia que ele quer
                for h in range(0, len(turno)):
                    if turno[h] != 0: # Horários do turno (manhã ou tarde)
                        for prefers in turno[h].teacher.prefers:
                            for p in prefers: # para cada limitação do professor
                                if f'N{day}' in str(p) or f'S{day}' in str(p): # Se a limitação estiver no dia do horário
                                    try:
                                        limite_inferior = int(p.split(':')[1].split(',')[0])
                                        limite_superior = int(p.split(':')[1].split(',')[1])
                                        if typeNum == 1:
                                            limite_inferior -= 5
                                            limite_superior -= 5
                                    except: # Considerando o caso de não ter selecionado uma variação de horários
                                        limite_inferior = 1
                                        limite_superior = 10

                                    if (limite_inferior <= int(h)+1) and (limite_superior >= int(h)+1): # Se o horário estiver compreendido durante a limitação
                                        if str(p)[0] == 'S': result_value += points['preferPositiva']
                                        else: result_value += points['preferNegativa']
                t += 1

    return result_value


def validation(horario, position, board, subjectPos, typeNum, sala=''): # board é o quadro de horários
    # Position = [day, hour]

    INVALIDO = -99

    #h_room = sala    # Sala
    h_day = position[0]  # Dia
    h_time = position[1] # Horário

    # Limitações do professor
    limitation = horario.teacher.limits[subjectPos]
    t_limitations = [] # N3:1,4

    for l in limitation: # para cada limitação do professor
        if f'N{h_day}' in str(l): # Se a limitação estiver no dia do horário
            try:
                limite_inferior = int(l.split(':')[1].split(',')[0])
                limite_superior = int(l.split(':')[1].split(',')[1])
                if typeNum == 1:
                    limite_inferior -= 5
                    limite_superior -= 5
            except: # Considerando o caso de não ter selecionado uma variação de horários
                limite_inferior = 1
                limite_superior = 10

            if (limite_inferior <= int(h_time)+1) and (limite_superior >= int(h_time)+1): # Se o horário estiver compreendido durante a limitação
                return INVALIDO

    # Limitações da sala
    #room_invalids_h =

    # Horário já está ocupado por outro no Quadro de horários?
    if board[str(h_day)][typeNum][h_time] != 0:
        return INVALIDO

    # Verificar também a parte dos professores
    if horario.teacher.schedule[str(h_day)][typeNum][h_time] != 0:
        return INVALIDO

    return 0
