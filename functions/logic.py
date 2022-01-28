# Arquivo com as funções envolvendo a lógica do nosso programa

import random
from functions import loadData

"""
Regras Básicas:
- não mudar o board dentro das funções
"""

def getBetterHour(horario, board, subjectPos, typeNum):
    quadro = board.copy()
    betterH = [('', -99)] # (day-hour, pontuação), melhores horários

    teacher = horario.teacher
    turm = horario.turm
    subject = horario.subject

    for d in range(2,7): # para cada dia
        d = str(d)
        for h in range(5): # para cada horário no dia
            pontuation = validation(horario, [d, h], quadro, subjectPos, typeNum)
            if pontuation == 0:
                pontuation = cost_individual(horario, [d, h], quadro, subjectPos, typeNum)
                if pontuation > betterH[0][1]:
                    betterH = [(f'{d};{h}', pontuation)]
                elif pontuation == betterH[0][1]:
                    betterH.append((f'{d};{h}', pontuation))

    return f"{random.choice(betterH)[0]};{turm[0]}" # Retorna f'{day};{hour};{turm}' depois nós colocaremos a room variable


def cost_individual(horario, position, board, subjectPos, typeNum, sala=''):
    points = loadData.getPoints('./data/preferencias.txt')
    pointsKeys = points.keys()

    pontuation = 0
    dayBoard = board[position[0]][typeNum]

    for p in pointsKeys:
        if p == "nHorariosDia": # Para a quantidade de horários já preenchidos no dia
            for h in dayBoard:
                if h != 0:
                    pontuation += points[p]

    return pontuation


def cost_board(board, path):
    points = getPoints(path)

    result_value = 0
    for quadro in board.values():
        for day in quadro.values():
            t = 0
            for turno in day:
                t += 1
                num_of_0 = turno.count(0)
                # Pontuação para cada dia já preenchido
                result_value += (5 - num_of_0) * points['nHorariosDia']

                # Pontuação para mais de 3 horários já preenchidos no mesmo dia
                if num_of_0 < 3:
                    result_value += points['tresHorariosDia'] * 5

                # Primeiros e últimos horários do turno
                if turno[0] != 0:
                    result_value += points['horariosPoints']
                if turno[4] != 0:
                    result_value += points['horariosPoints']

                # Horários de mesma matéria agrupados
                for h in range(0, len(turno)):
                    if (h != 0) and (turno[h].subject == turno[h + 1].subject):
                            result_value += points['lastResp']

                # Professor dando aula no dia que ele quer
                for h in range(0, len(turno)):
                    for prefer in turno[h].teacher.prefers:

                        limite_inferior = prefer.split(':')[1].split('-')[0]
                        limite_superior = prefer.split(':')[1].split('-')[1]
                        if t > 1:
                            limite_inferior -= 5
                            limite_superior -= 5

                        if (f'S{day}' in prefer) and (h >= limite_inferior) and (h <= limite_superior):
                            result_value += points['preferPositiva']
                        elif (f'N{day}' in prefer) and (h >= limite_inferior) and (h <= limite_superior):
                            result_value += points['preferNegativa']
    return result_value


def validation(horario, position, board, subjectPos, typeNum, sala=''): # board é o quadro de horários
    # Position = [day, hour]

    INVALIDO = -99

    #h_room = sala    # Sala
    h_day = position[0]  # Dia
    h_time = position[1] # Horário

    # Limitações do professor
    limitation = horario.teacher.limits[subjectPos]
    t_limitations = [] # N3:1-4
    """
    for l in limitation: # para cada limitação do professor
        if f'N{h_day}' in l: # Se a limitação estiver no dia do horário
            nums = l.split(':')[1].split('-')
            if (nums[0] <= h_time) and (nums[1] >= h_time): # Se o horário estiver compreendido durante a limitação
                return INVALIDO
    """
    # Limitações da sala
    #room_invalids_h =

    # Horário já está ocupado por outro no Quadro de horários?
    if board[str(h_day)][typeNum][h_time] != 0:
        return INVALIDO

    print("d")

    return 0
