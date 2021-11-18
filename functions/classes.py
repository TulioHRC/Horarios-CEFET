class Teacher:
    def __init__(self, name, subject, prefers, limits, classes):
        self.name = name
        self.subjects = [subject] # Formato = ['{subject}:{year}']
        self.prefers = [prefers] # Formato = ['{subject}:{prefers}']
        self.limits = limits
        self.classes = [classes] # Formato = [['{turma}{ano}-{número de horários}', ...]] Uma lista pra cada matéria

    def bestHour(self, turm, subject, preDefinedHour="", alreadyChose=""): # Definição do melhor horário para o professor

        # Formato dos argumentos: class="{turma}"
        #           preDefinedHour="{day}-{horario de 0 (7:50-8:40) até 9 (16:40-17:30)}"
        #           alreadyChose={'2': '{lista com os números dos horários já escolhidos}', ... (outros dias, até o 6)}

        if preDefinedHour and not f"N{preDefinedHour[0]}" in limits and not f"N{preDefinedHour[0]}" in prefers:
            # Se o horário pré-definido poder (não for proibido pelas limits ou não for preferido)
            return preDefinedHour

        if f'{turm.name[0:-3]}-0' in self.classes: return 0 # Se não houver horários da turma

        # Pegando o melhor horário possível para o professor
        goodOptions = 0
        for prefer in self.prefers[self.subjects.index(subject)].split(":")[1].split('-'):
            if 'S' in prefer and alreadyChose[f"{prefer[1]}"]:
                for hour in alreadyChose[f"{prefer[1]}"]:
                    #...

############# Falta forma de se pegar os "pontos" que o Samuel falou, ou seja, avaliação de cada possibilidade com um valor dependendo das suas
# conveniencias e dificuldades

class Turm:
    def __init__(self, name, year, preDefinedSchedule={'2': [],'3': [],'4': [],'5': [],'6': []}):
        self.name = f'{name}-{year}A'
        self.schedule = preDefinedSchedule # Horários de cada turma
        # Formato dos horários = '{horário de 0 a 9}-{matéria/subject}'


class Room:
    def __init__(self, name, position, limits, preDefinedSchedule={'2': [],'3': [],'4': [],'5': [],'6': []}):
        self.name = name
        self.position = position
        self.limits = limits
        self.schedule = preDefinedSchedule # Horários de cada sala
