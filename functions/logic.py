# Arquivo com as funções envolvendo a lógica do nosso programa

import random

def getBetterHour(horario, board):
    quadro = board.copy()
    betterH = [('', -99)] # (day-hour, pontuação), melhores horários

    teacher = horario.teacher
    turm = horario.turm
    subject = horario.subject

    for d in range(5): # para cada dia
        for h in range(5): # para cada horário no dia
            quadro[d][h] = validation(horario, [d, h], quadro)
            if quadro[d][h] == 0:
                quadro[d][h] = cost_individual(quadro[d][h])
                if quadro[d][h] > betterH[0][1]:
                    betterH = [(f'{d}-{h}', quadro[d][h])]
                elif quadro[d][h] == betterH[0][1]:
                    betterH.append((f'{d}-{h}', quadro[d][h]))

    return random.choice(betterH)[0] # Retorna f'{day}-{hour}'

def cost_individual(horario, position, board, sala=''):
    #

def cost_board(board):



def validation(horario, position, board, sala=''): # board é o quadro de horários
    # Position = (sala, (dia, horario))
    INVALIDO = -99

    h_room = sala    # Sala
    h_day = position[0]  # Dia
    h_time = position[1] # Horário

    # Limitações do professor
    limitation = horario.teacher.limits
    t_limitations = [] # N3:1-4
    for l in limitation: # para cada limitação do professor
        if f'N{h_day}' in l: # Se a limitação estiver no dia do horário
            nums = l.split(':')[1].split('-')
            if (nums[0] <= h_time) and (nums[1] >= h_time): # Se o horário entiver compreendido durante a limitação
                return INVALIDO

    # Limitações da sala
    #room_invalids_h =

    # Horário já está ocupado por outro no Quadro de horários?
    if type(board[horario.turm.name][h_day][h_time]) != type(0):
        return INVALIDO

    return 0
