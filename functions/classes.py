import random
import re


class Teacher:
    def __init__(self, name, subject, type, prefers, limits, horaries):
        self.name = name
        self.subjects = [subject] # Formato = cada matéria será adicionada nesta lista, com a seguinte formatação nome:turma, ex.: Matematica:MCT-2A
        self.types = [type] # Formato = semelhante ao de cima, tendo as opções: manha, tarde ou noite
        self.prefers = [prefers] # Formato = haverá uma lista para cada uma das matérias, tendo o seguinte formato S ou N dia:horário inicial - horário final, ex.: S6:2-4, ou seja,
        # prefere dar aula na sexta entre os horários 2 e 4
        self.limits = [limits] # Formato = segue o mesmo do acima, tendo a formatação N dia:horário inicial - horário final, ex.: N5:3-5, ou seja, não pode quinta nos horários 3 a 5
        self.schedule = {'2': [],'3': [],'4': [],'5': [],'6': []} # Horários durante a semana do professor
        self.horaries = {subject: horaries} # Formato = {subject: {Turm: classesInTheTurm}}, ex.: {'Matematica': {MCT-1A: 4, ...}}
        self.classes = 0 # Número de aulas totais que está lecionando


class Turm:
    def __init__(self, name, year, group):
        self.name = f'{name}-{year}{group}' # ex.: MEC-3B
        self.schedule = {'2': [],'3': [],'4': [],'5': [],'6': []} # Horários durante a semana da turma

""" Ainda não foi adicionada
class Room:
    def __init__(self, name, position, limits, preDefinedSchedule=''):
        self.name = name
        self.position = position
        self.limits = limits
        if preDefinedSchedule:
            self.schedule = preDefinedSchedule # Horários de cada sala
        else:
            self.schedule = {'2': [],'3': [],'4': [],'5': [],'6': []}
"""

class Horario:
    def __init__(self, teacher, subject, turm, possible_h=0):
        self.teacher = teacher
        self.subject = subject
        self.turm = turm
        self.possible_h = possible_h
        #self.position = None

    def __repr__(self):
        return f'{self.teacher}-{self.subject}'
