class Teacher:
    def __init__(self, name, subject, year, prefers, limits, classes):
        self.name = name
        self.subject = subject
        self.year = year
        self.prefers = prefers
        self.limits = limits
        self.classes = classes # Formato = ['{turma}-{número de horários}', ...]

    def bestHour(self, turm, preDefinedHour="", alreadyChose=""): # Definição do melhor horário para o professor

        # Formato dos argumentos: class="{turma}"
        #           preDefinedHour="{day}-{horario de 0 (7:50-8:40) até 9 (16:40-17:30)}"
        #           alreadyChose={2: '{números dos horários já escolhidos}', ... (outros dias, até o 6)}

        if preDefinedHour and not f"N{preDefinedHour[0]}" in limits and not f"N{preDefinedHour[0]}" in prefers:
            # Se o horário pré-definido poder (não for proibido pelas limits ou não for preferido)
            return preDefinedHour

        if f'{turm}-0' in self.classes: return 0 # Se não houver horários da turma

        # Pegando o melhor horário possível para o professor
        goodOptions = 0
        for prefer in self.prefers.split('-'):
            if 'S' in prefer and prefer[-1] in alread

############# Falta forma de se pegar os "pontos" que o Samuel falou, ou seja, avaliação de cada possibilidade com um valor dependendo das suas
# conveniencias e dificuldades

class Turm:
    def __init__(self, name):
        self.name = name
        self.schedule1 = { # Horários de cada turma
            '2': [],
            '3': [],
            '4': [],
            '5': [],
            '6': [],
        }
        self.schedule2 = self.schedule1.copy() # 2 ano
        self.schedule3 = self.schedule1.copy() # 3 ano
        # Formato dos horários = '{horário de 0 a 9}-{matéria/subject}'
