import random
import re


class Teacher:
    def __init__(self, name, subject, type, prefers, limits, classes):
        self.name = name
        self.subjects = [subject] # Formato = ['{subject}:{year}', ...]
        self.types = [type] # Formato = ['Manha', ...] manhã ou tarde
        self.prefers = [prefers] # Formato = ['{subject}:{prefers}', ...]
        self.limits = [limits] # Formato ['{limits}', ...]
        self.classes = [classes] # Formato = [['{turma}-{ano}A-{número de horários}', ...]] Uma lista pra cada matéria
        self.schedule = {'2': [],'3': [],'4': [],'5': [],'6': []}

    def getClassesNum(self, className, subject): # Retorna o número de aulas dadas para tal turma em tal matéria
        pos = self.subjects.index(subject)
        start = str(self.classes[pos]).find(f"{className}-")
        end = str(self.classes[pos]).find(f"-", start+4) # Segundo '-'
        return int(str(self.classes[pos])[end+1])

    def bestHour(self, turm, subject, preDefinedHour="", alreadyChose="", classNumber="", points="", lastResp="a"): # Definição do melhor horário para o professor
    # Formato dos argumentos: class="{turma}"
        #           preDefinedHour="{day}-{horario de 1 (7:00-7:50) até 14 (16:40-17:30)}"
        #           alreadyChose={'2': '{lista com os números dos horários já escolhidos}', ... (outros dias, até o 6)}

    # Pre código verificações
        if preDefinedHour and not f"N{preDefinedHour[0]}" in limits and not f"N{preDefinedHour[0]}" in prefers:
            # Se o horário pré-definido poder (não for proibido pelas limits ou não for preferido)
            return preDefinedHour

        if f'{turm.name[0:-3]}-0' in self.classes: return 0 # Se não houver horários da turma

        # Pegando o melhor horário possível para o professor
        positionInList = self.subjects.index(f"{subject}:{turm.name.split('-')[1][0]}") # Pegar o local na lista onde está tal matéria

    # ------------ No Random mode

        days = { # 'day': [dayNote, [hoursNotes]]
            '2': [0, [0,0,0,0,0]],
            '3': [0, [0,0,0,0,0]],
            '4': [0, [0,0,0,0,0]],
            '5': [0, [0,0,0,0,0]],
            '6': [0, [0,0,0,0,0]],
        }

        if self.types[positionInList] == "Manha": # Tipo de matéria
            minHour = 0
            maxHour = 7
            hourPos = [1,2,3,5,6] # 11:30 (7) não pode começar um horário e nem (9:30/4)
        else:
            minHour = 8
            maxHour = 14
            hourPos = [8,9,10,12,13] # 17:30 (14) não pode começar um horário e nem (15:30/11)

        # Day Pontuations
        for day in range(2, 7):
            if f"N{day}" in str(self.limits[positionInList]): del days[f"{day}"] # Se dia for uma limitação remove ele
            else:
                # Compromissos da sala durante o dia
                pontuation = 0
                hourFilled = 0 # Quantidade de horários preenchidos

                for h in alreadyChose[str(day)]: # Contagem de horários já preenchidos
                    if int(h.split('-')[0]) > minHour and int(h.split('-')[0]) < maxHour: hourFilled += 1

                # Mais de 1 horário preenchido e não é outro horário de uma matéria do mesmo dia
                if hourFilled > 0: pontuation += points['nHorariosDia']*hourFilled # Pontuação para cada dia já preenchido no dia
                if hourFilled >= 3: pontuation += points['tresHorariosDia'] # Pontuação para mais de 3 dias já preenchidos (pontuação a mais da acima)
                if hourFilled >= 5:
                    del days[f"{day}"] # Não pode no dia na turma já preenchido
                    break

                # Compromissos do professor durante o dia
                hourFilled = 0

                for h in self.schedule[str(day)]: # Contagem de horários preenchidos do professor
                    if int(h.split('-')[0]) > minHour and int(h.split('-')[0]) < maxHour: hourFilled += 1

                if hourFilled > 0: pontuation += points['nHorariosDia']*hourFilled
                if hourFilled >= 3: pontuation += points['tresHorariosDia']
                if hourFilled >= 5:
                    del days[f"{day}"] # Não pode no dia na turma já preenchido
                    break

                # Outras Pontuações

                if lastResp[0] == str(day): pontuation += points['lastResp'] # Acontecer no mesmo dia da outra aula da mesma matéria
                if f"N{day}" in str(self.prefers[positionInList].split(":")[1]): pontuation += points['preferNegativa']
                if f"S{day}" in str(self.prefers[positionInList].split(":")[1]): pontuation += points['preferPositiva']

                days[f"{day}"][0] = pontuation # Definição da ontuação do dia

                # Hour Pontuations
                h = 0
                while h < len(days[f"{day}"][1]):
                    if hourPos[h] in [1,6,8,13]: # Pontuações dependendo do horários, serão pegas depois
                        days[f"{day}"][1][h] += points['horariosPoints']
                    h += 1

        # Hour Already Chosen
        for day in list(days.keys()):
            if len(alreadyChose[str(day)]):
                for hour in alreadyChose[str(day)]: # Para a turma ( formato = hour-materia)
                    if int(hour.split('-')[0]) in hourPos: # Se horário está nas possibilidades
                        days[day][1][hourPos.index(int(hour.split('-')[0]))] = -9999 # Se o horário não pode
                for hourT in self.schedule[str(day)]: # Para o porfessor ( formato = hour-materia - turma )
                    if int(hourT.split('-')[0]) in hourPos:
                        days[day][1][hourPos.index(int(hourT.split('-')[0]))] = -9999 # Se o horário não pode

        # Escolha do melhor resultado
        daysChoosed = []
        daysNotes = []
        for day in list(days.keys()): # Escolha do dia
            daysNotes.append(days[day][0]) # Nota
        for n in range(len(daysNotes)):
            if daysNotes[n] == max(daysNotes): # Se a nota é a maior
                daysChoosed.append(list(days.keys())[n])

        day = random.choice(daysChoosed)

        hoursChoosed = []
        hoursNotes = days[day][1]
        for hour in range(len(hoursNotes)): # Escolha do horário
            if hoursNotes[hour] == max(hoursNotes): # Se a nota é a maior
                hoursChoosed.append(hourPos[hour]) # Adiciona na lista, o número do horário na lista

        hour = random.choice(hoursChoosed)

        return [str(day), f'{str(hour)}-{subject}'] # Lista de retorno

        # ------------ Random mode
"""
        day = random.randint(2, 6)
        if self.types[positionInList] == 'Manha':
            hour = random.choice([1,2,3,5,6]) # 11:30 (7) não pode começar um horário e nem (9:30/4)
        else:
            hour = random.randint([8,9,10,12,13]) # 17:30 (14) não pode começar um horário e nem (15:30/11)

        try: # Se alreadyChose não existir dará um erro
            while re.findall(f"\'{hour}-", str(alreadyChose[f"{day}"])): # Tenta encontrar "'{hour}-" na lista de horários já escolhidos:
                day = random.randint(2, 6)
                if self.types[positionInList] == 'Manha':
                    hour = random.choice([1,2,3,5,6])
                else:
                    hour = random.randint([8,9,10,12,13])
        except:
            print('alreadyChose não existe ainda, o código continuará normalmente!')

        return [str(day), f'{str(hour)}-{subject}'] # Lista de retorno
"""

class Turm:
    def __init__(self, name, year, preDefinedSchedule=''):
        self.name = f'{name}-{year}A'
        if preDefinedSchedule:
            self.schedule = preDefinedSchedule # Horários de cada turma
        else:
            self.schedule = {'2': [],'3': [],'4': [],'5': [],'6': []}
        # Formato dos horários = '{horário de 1 a 12}-{matéria/subject}'

class Room:
    def __init__(self, name, position, limits, preDefinedSchedule=''):
        self.name = name
        self.position = position
        self.limits = limits
        if preDefinedSchedule:
            self.schedule = preDefinedSchedule # Horários de cada sala
        else:
            self.schedule = {'2': [],'3': [],'4': [],'5': [],'6': []}

class Horario:
    def __init__(self, teacher, subject, turm, possible_h=0):
        self.teacher = teacher
        self.subject = subject
        self.turm = turm
        self.possible_h = possible_h
        #self.position = None

    def __repr__(self):
        return f'{self.teacher}-{self.subject}'