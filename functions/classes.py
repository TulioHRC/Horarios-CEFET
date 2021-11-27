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

    def bestHour(self, turm, subject, preDefinedHour="", alreadyChose=""): # Definição do melhor horário para o professor

        # Formato dos argumentos: class="{turma}"
        #           preDefinedHour="{day}-{horario de 1 (7:00-7:50) até 14 (16:40-17:30)}"
        #           alreadyChose={'2': '{lista com os números dos horários já escolhidos}', ... (outros dias, até o 6)}

        if preDefinedHour and not f"N{preDefinedHour[0]}" in limits and not f"N{preDefinedHour[0]}" in prefers:
            # Se o horário pré-definido poder (não for proibido pelas limits ou não for preferido)
            return preDefinedHour

        if f'{turm.name[0:-3]}-0' in self.classes: return 0 # Se não houver horários da turma

        # Pegando o melhor horário possível para o professor
        positionInList = self.subjects.index(f"{subject}:{turm.name.split('-')[1][0]}") # Pegar o local na lista onde está tal matéria

        # ------------ No Random mode

        # Dias possiveis e suas pontuações
        dayPos = []
        dayPoints = []

        for i in range(2, 7):
            if not f"N{i}" in str(self.limits[positionInList]):
                dayPos.append(i)
                dayPoints.append(0)

        prefers = str(self.prefers[positionInList].split(":")[1]).split('-')
        for prefer in prefers:
            point = 0
            if prefer[0] == "N":
                dayPoints[dayPos.index(int(prefer[1]))] += -1 # 3333333333333333333333 Função pegará a pontuação definida futuramente
            elif prefer[0] == "S":
                dayPoints[dayPos.index(int(prefer[1]))] += 1

        # Horários possíveis e suas pontuações
        hourPos = []
        hourPoints = [0,0,0,0,0]

        if self.types[positionInList] == 'Manha':
            hourPos = [1,2,3,5,6] # 11:30 (7) não pode começar um horário e nem (9:30/4)
        else:
            hourPos = [8,9,10,12,13] # 17:30 (14) não pode começar um horário e nem (15:30/11)

        for i in hourPos:
            if i in [1,6,8,13]: # Pontuações dependendo do horários, serão pegas depois
                hourPoints[hourPos.index(i)] += -1
            # Outras pontuações ...

        # Escolha do melhor resultado
        pos = 0
        for d in range(len(dayPos)): # Tira os dias que não são o melhor
            if not dayPoints[pos] == max(dayPoints):
                dayPos.pop(pos)
                dayPoints.pop(pos)
                pos -= 1
            pos += 1

        day = random.choice(dayPos)

        pos = 0
        for h in range(len(hourPos)): # Tira os horários que não são o melhor
            if not hourPoints[pos] == max(hourPoints):
                hourPos.pop(pos)
                hourPoints.pop(pos)
                pos -= 1
            pos += 1

        day = random.choice(dayPos)
        hour = random.choice(hourPos)

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
"""
        #return [str(day), f'{str(hour)}-{subject}'] # Lista de retorno


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
