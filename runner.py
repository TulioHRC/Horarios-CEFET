
from functions import *
from funcs import convert2day as convert
import pandas as pd

# Conjunto de todas as salas do DEMAT
dfrooms = pd.read_excel('Disponibilidade de salas.xlsx', 'Sheet1')
rooms = set()   # Lista de salas (em objetos)
for r in range(0, len(dfrooms['Salas'].values)):
    Room = Sala(int(dfrooms['Salas'].values[r]))
    for day in ['segunda', 'terça', 'quarta', 'quinta', 'sexta']:
        Room.h_ocupados[dfrooms[day]] = dfrooms[day].values[:]
    rooms.add(Room)

# Conjunto de todas as matérias do DEMAT
# Devemos adicionar essas informações por meio de uma outra planilha separada
"""
    dfSubjects = pd.read_excel('Materias.xlsx', 'Sheet1')
    for como o das salas, só que pode ser em dicionário ao ínves de objetos
"""

# Criar planilha de matérias e salas

# Criar um set com todos os professores
# Declarar todos eles também como sendo da classe professores
dfTeachers = pd.read_excel('Planilha esperada.xlsx', 'Sheet1')   # Lendo a planilha do excel, e Sheet1 é o nome da aba do excel para ler

professores_nomes = [] # Somente listas permitem usar metodos como o index
all_teachers = []
for p in range(0, len(dfTeachers['Professor'].values)):
    if dfTeachers['Professor'].values[p] in professores_nomes:
        teacher = all_teachers[professores_nomes.index(dfTeachers['Professor'].values[p])]
    else:
        teacher = Professor(dfTeachers['Professor'].values[p])
        professores_nomes.append(teacher.name)
        all_teachers.append(teacher)

    list_prefer = df['Preferências'].values[p].split('-')
    teacher.prefer.append([set(), set()])

    for prefer in list_prefer: # Adiciona os dias que se quer ou não dar aula ao objeto
        prefer = str(prefer)
        if 'S' in prefer.upper:
            teacher.prefer[len(teacher.subjects)][0].add(convert.convertNumToDay(prefer[1]))
        elif 'N' in prefer.upper:
            teacher.prefer[len(teacher.subjects)][1].add(convert.convertNumToDay(prefer[1]))

    limitations = df['Obrigações'].values[p].split('-')
    for limit in limitations:
        teacher.limitations.add(convert.convertNumToDay(limit[1])) # Adiciona os dias que não se pode dar aula

    """
        Dividir por ano (1ª, 2ª ou 3ª) as matérias, pois um professor pode dar uma mesma matéria para anos diferentes,
        mas contará como o mesmo no nosso código atual.
    """
    teacher.subjects.add(df['Matéria'].values[p]) # Adiciona a matéria ao objeto do professor


# State vai ser o dicionário final. Ele é o que deve ser trasformado em um data frame
# Apenas o state mais barato será trasformado em resultado final.
result_state = {}
for teacher in all_teachers:
    result_state[teacher.name] = teacher.classes

"""
    Olhei até aqui, Ass. Túlio
"""

dict_base = {}
for rooms_for_creat_initial_state in rooms:
    dict_base[rooms_for_creat_initial_state] = []
initial_state = {'segunda': dict_base[:], 'terça': dict_base[:], 'quarta': dict_base[:], 'quinta': dict_base[:], 'sexta': dict_base[:]}


# primeiro node
first_node = Node(initial_state[:], 0)
greedy = Frontier()
greedy.frontier.append(first_node)

# Expandir
Empty = 0   # Sempre que um horário for marcado como vazio, se coloca Empty no lugar da aula.
for day_of_week in initial_state.keys():
    # node será o node que será espandindo, dando origem a novos nodes
    # Os novos nodes serão analizados antes de serem adicionados ao frontier
    parent = greedy.select_node()

    if is_final_result(parent.state):
        RESULTADO = parent.state

    for teacher in all_teachers:
        # Como adicionar os nodes?
        # Para cada matéria que o professor der aula
            # Para cada sala que possa ter aquela matéria
            # Criar um node com esse estado.
        for subj_teacher in teacher.subjects:
            for rooms_of_subject in subjects[subj_teacher]['Salas que podem ser ocupadas']:
                n_state = parent.state[:]
                # A definição do horário será dada dessa maneira: (Qual o professor, qual a matéria)
                n_state[day_of_week][rooms_of_subject] = (teacher.name, subj_teacher)
                if proibitions(n_state):
                    # Vamos declarar isso como node apenas se for aceito o estado
                    x = Node(n_state[:], cost(n_state), parent)
                    greedy.add_node(x)
                    # Node adicionado ao frontier com suscesso
