# Arquivo com as funções envolvendo a lógica do nosso programa

def getBetterHour():

def cost():

def validation(horario, position, board):
    INVALIDO = -99

    h_room = position[0]
    h_day = position[1][0]
    h_time = position[1][1]

    # Limitações do professor
    limitation = horario.teacher.limits
    t_limitations = []
    for l in limitation: # para cada limitação do professor
        if f'N{h_day}' in l: # Se a limitação estiver no dia do horário
            nums = (l.split(':')[1].split('-'))
            if (nums[0] <= h_time) and (nums[1] >= h_time): # Se o horário entiver compreendido durante a limitação
                return INVALIDO

    # Limitações da sala
    room_invalids_h =

    # Horário já está ocupado por outro no Quadro de horários?
    if type(board[horario.turm][h_day][h_time]) != type(0):
        return INVALIDO

    return 0


