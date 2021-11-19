class Teacher:
    def __init__(self, name, subject, type, prefers, limits, classes):
        self.name = name
        self.subjects = [subject] # Formato = ['{subject}:{year}']
        self.types = [type] # Formato = ['Manha', ...] manhã ou tarde
        self.prefers = [prefers] # Formato = ['{subject}:{prefers}']
        self.limits = limits
        self.classes = [classes] # Formato = [['{turma}-{ano}A-{número de horários}', ...]] Uma lista pra cada matéria
        self.schedule = {'2': [],'3': [],'4': [],'5': [],'6': []}

    def getClassesNum(self, className, subject): # Retorna o número de aulas dadas para tal turma em tal matéria
        pos = self.subjects.index(subject)
        start = str(self.classes[pos]).find(f"{className}-")
        end = str(self.classes[pos]).find(f"-", start+4) # Segundo '-'
        return int(str(self.classes[pos])[end+1])

    def bestHour(self, turm, subject, preDefinedHour="", alreadyChose=""): # Definição do melhor horário para o professor

        # Formato dos argumentos: class="{turma}"
        #           preDefinedHour="{day}-{horario de 0 (7:50-8:40) até 9 (16:40-17:30)}"
        #           alreadyChose={'2': '{lista com os números dos horários já escolhidos}', ... (outros dias, até o 6)}

        if preDefinedHour and not f"N{preDefinedHour[0]}" in limits and not f"N{preDefinedHour[0]}" in prefers:
            # Se o horário pré-definido poder (não for proibido pelas limits ou não for preferido)
            return preDefinedHour

        if f'{turm.name[0:-3]}-0' in self.classes: return 0 # Se não houver horários da turma

        # Pegando o melhor horário possível para o professor
        """
        goodOptions = 0
        for prefer in self.prefers[self.subjects.index(subject)].split(":")[1].split('-'):
            if 'S' in prefer and alreadyChose[f"{prefer[1]}"]:
                for hour in alreadyChose[f"{prefer[1]}"]: # Horários já escolhidos
                    print(hour)
                    #...
        """

        positionInList = self.subjects.index(f"{subject}:{turm.name.split('-')[1][0]}") # Pegar o local na lista onde está tal matéria

        # Random mode
        import random
        import re

        day = random.randint(2, 6)
        if self.types[positionInList] == 'Manha':
            hour = random.randint(1, 5) # 11:30 não pode começar um horário
        else:
            hour = random.randint(7, 11) # 17:30 não pode começar um horário

        try: # Se alreadyChose não existir dará um erro
            while re.findall(f"\'{hour}-", str(alreadyChose[f"{day}"])): # Tenta encontrar "'{hour}-" na lista de horários já escolhidos:
                day = random.randint(2, 6)
                if self.types[positionInList] == 'Manha':
                    hour = random.randint(1, 5)
                else:
                    hour = random.randint(7, 11)
        except:
            print('alreadyChose não existe ainda, o código continuará normalmente!')

        return [str(day), f'{str(hour)}-{subject}'] # Lista de retorno


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
