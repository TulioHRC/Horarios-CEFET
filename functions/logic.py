# Arquivo com as funções envolvendo a lógica do nosso programa

import random
from functions import loadData

def getBetterHour(horario, board, subjectPos, typeNum):
    quadro = board.copy()
    betterH = [('', -99)] # (day-hour, pontuação), melhores horários

    teacher = horario.teacher
    turm = horario.turm
    subject = horario.subject

    for d in range(2,7): # para cada dia
        d = str(d)
        for h in range(5): # para cada horário no dia
            print('b')
            quadro[d][typeNum][h] = validation(horario, [d, h], quadro, subjectPos, typeNum)
            print("c")
            if quadro[d][typeNum][h] == 0:
                quadro[d][typeNum][h] = cost_individual(horario, [d, h], quadro, subjectPos)
                if quadro[d][typeNum][h] > betterH[0][1]:
                    betterH = [(f'{d};{h}', quadro[d][typeNum][h])]
                elif quadro[d][typeNum][h] == betterH[0][1]:
                    betterH.append((f'{d};{h}', quadro[d][typeNum][h]))

    return f"{random.choice(betterH)[0]};{turm[0]}" # Retorna f'{day};{hour};{turm}' depois nós colocaremos a room variable

def cost_individual(horario, position, board, subjectPos, sala=''):
    #points = loadData.getPoints('../data/preferencias.txt')
    #print(points)
    return 0

#def cost_board(board):



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
            if (nums[0] <= h_time) and (nums[1] >= h_time): # Se o horário entiver compreendido durante a limitação
                return INVALIDO
    """
    # Limitações da sala
    #room_invalids_h =

    # Horário já está ocupado por outro no Quadro de horários?
    if board[str(h_day)][typeNum][h_time] != 0:
        return INVALIDO

    print("d")

    return 0
