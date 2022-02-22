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

    teacher = horario.teacher
    turm = horario.turm
    subject = horario.subject

    for d in range(2, 7):  # para cada dia
        d = str(d)
        for h in range(0, 5):  # para cada horário no dia
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
            if position[1] in [0, 4]:
                pontuation += points[p]
        elif p == "lastResp":
            if position[1] != 0:
                if dayBoard[position[1] - 1] != 0:
                    if dayBoard[position[1] - 1].subject == horario.subject: pontuation += points[p]
            if position[1] != 4:
                if dayBoard[position[1] + 1] != 0:
                    if dayBoard[position[1] + 1].subject == horario.subject: pontuation += points[p]
        elif p == "preferPositiva":  # negativa e positiva para diminuir código
            for prefer in horario.teacher.prefers[subjectPos]:  # para cada limitação do professor
                if f'N{position[0]}' in str(prefer) or f'S{position[0]}' in str(
                        prefer):  # Se a limitação estiver no dia do horário
                    try:
                        limite_inferior = int(prefer.split(':')[1].split(',')[0])
                        limite_superior = int(prefer.split(':')[1].split(',')[1])
                        if typeNum == 1:
                            limite_inferior -= 5
                            limite_superior -= 5
                    except:  # Considerando o caso de não ter selecionado uma variação de horários
                        limite_inferior = 1
                        limite_superior = 10

                    if (limite_inferior <= int(position[1]) + 1) and (limite_superior >= int(
                            position[1]) + 1):  # Se o horário estiver compreendido durante a limitação
                        if str(prefer)[0] == 'S':
                            pontuation += points['preferPositiva']
                        else:
                            pontuation += points['preferNegativa']
        # print(pontuation)

    return pontuation


def cost_board(board):
    points = loadData.getPoints('./data/preferencias.txt')

    result_value = 0
    for quadro in board.values():  # Para cada turma
        for day in quadro.values():  # Para cada dia nesta turma
            t = 0
            for turno in day:  # Para manhã e depois tarde
                num_of_0 = turno.count(0)
                # Pontuação para cada dia já preenchido
                result_value += (6 - num_of_0) * points['nHorariosDia']

                # Pontuação para mais de 3 horários já preenchidos no mesmo dia
                if num_of_0 < 3:
                    result_value += points['tresHorariosDia']

                # Primeiros e últimos horários do turno
                if turno[0] != 0:
                    result_value += points['horariosPoints']
                if turno[5] != 0:
                    result_value += points['horariosPoints']

                # Horários de mesma matéria agrupados
                for h in range(0, len(turno)):
                    if h != 5:
                        if turno[h] != 0 and turno[h + 1] != 0:
                            if str(type(turno[h])) == "<class 'list'>":
                                for h_bimestral in range(0, 4):
                                    if str(type(turno[h + 1])) == "<class 'list'>":
                                        if turno[h][h_bimestral].subject == turno[h + 1][h_bimestral].subject:
                                            result_value += points['lastResp']
                            elif turno[h].subject == turno[h + 1].subject:
                                result_value += points['lastResp']

                # Professor dando aula no dia que ele quer
                for h in range(0, len(turno)):
                    if turno[h] != 0:  # Horários do turno (manhã ou tarde)
                        for prefers in turno[h].teacher.prefers:
                            for p in prefers:  # para cada limitação do professor
                                if f'N{day}' in str(p) or f'S{day}' in str(
                                        p):  # Se a limitação estiver no dia do horário
                                    try:
                                        limite_inferior = int(p.split(':')[1].split(',')[0])
                                        limite_superior = int(p.split(':')[1].split(',')[1])
                                        if typeNum == 1:
                                            limite_inferior -= 5
                                            limite_superior -= 5
                                    except:  # Considerando o caso de não ter selecionado uma variação de horários
                                        limite_inferior = 1
                                        limite_superior = 10

                                    if (limite_inferior <= int(h) + 1) and (limite_superior >= int(
                                            h) + 1):  # Se o horário estiver compreendido durante a limitação
                                        if str(p)[0] == 'S':
                                            result_value += points['preferPositiva']
                                        else:
                                            result_value += points['preferNegativa']
                t += 1

    return result_value


def validation(horario, position, board, subjectPos, typeNum, all_teachers, sala=''):  # board é o quadro de horários
    # Position = [day, hour]

    INVALIDO = -99

    # h_room = sala    # Sala
    h_day = position[0]  # Dia
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
                    limite_inferior -= 5
                    limite_superior -= 5
            except:  # Considerando o caso de não ter selecionado uma variação de horários
                limite_inferior = 1
                limite_superior = 10

            if (limite_inferior <= int(h_time) + 1) and (
                    limite_superior >= int(h_time) + 1):  # Se o horário estiver compreendido durante a limitação
                return INVALIDO

    # Limitações da sala
    # room_invalids_h =

    # Horário já está ocupado por outro no Quadro de horários?
    if board[str(h_day)][typeNum][h_time] != 0:
        return INVALIDO

    # Verificar também a parte dos professores
    if horario.teacher.schedule[str(h_day)][typeNum][h_time] != 0:
        return INVALIDO

    # Não pode trabalhar mais de 8h no mesmo dia
    # O professor só vai dar mais de 8h de aula em um dia se ele der 10 horários
    for teacher in all_teachers:
        for morning, evening in teacher.schedule.values():
            day_ok = 0
            bimestral_horaries = []
            day = morning + evening
            for h in day:
                if h != 0 and (str(type(h)) != "<class 'list'>"):
                    day_ok += 1  # day_ok é a quantidade de aulas que o professor da no dia
                    break
                if str(type(h)) == "<class 'list'>":
                    bimestral_horaries.append(h)
            # ========== Agora analisamos os horários bimestrais
            max_value = 0  # É o numero máximo de horários bimestrais que ele dá de uma vez

            for c in range(0, 4):  # Para cada bimestre
                current_value = 0  # quantidade de aulas bimestrais que ele vai dar em uma semana desse bimestre
                for h in bimestral_horaries:
                    if h[c] != 0:
                        current_value += 1
                # Se a quantidade de horários dados nesse bimestre for maior que a quantidade de horários dados nos bimestres anteriores
                max_value = current_value if (current_value >= max_value) else max_value
            # Ao final somamos o maior valor à quantidade de horários normais que temos
            day_ok += max_value
            # Se a quantidade de horários da situação que tiver a maior quantidade de horários for aceitável,
            # então está tudo bem
            if day_ok >= 9:
                return INVALIDO

    # Não pode ter um intervalo entre uma aula e outra maior que 3h
    # almoço= 90min, intervalo= 20min
    for teacher in all_teachers:
        for morning, evening in teacher.schedule.values():
            tempo_ocioso = 0
            ja_passou_pelo_primeiro_h = False
            day = morning + evening
            for h in range(0, 12):
                # Adicionamos o tempo dos intervalos ao tempo ocioso
                if h == 6:  # passou o almoço
                    tempo_ocioso += 90
                if (h == 3) or (h == 9):  # passou o recreio
                    tempo_ocioso += 20

                # Adicionamos o tempo dos horários vagos ao tempo ocioso
                if day[h] == 0:
                    tempo_ocioso += 50

                # Se o professor tiver aula no horário, analisa se o tempo ocioso é maior que o permitido.
                # Se não for maior, zera o tempo ocioso.
                else:
                    if (tempo_ocioso >= 180) and ja_passou_pelo_primeiro_h:
                        return INVALIDO
                    tempo_ocioso = 0
                    ja_passou_pelo_primeiro_h = True
    # Deve ser implementado apenas quando todos os dados já estiverem cadastrados

    # Devem ser ao menos 11h entre o primeiro e o último horário de descanso

    return 0
