
from functions import *
import pandas as pd

# Demonstrando utilização do pandas
df = pd.read_excel('Planilha esperada.xlsx', 'Sheet1')   # Lendo a planilha do excel, e Sheet1 é o nome da aba do excel para ler

# Conjunto de todas as salas do DEMAT
dfrooms = pd.read_execel('Disponibilidade de salas', 'Sheet1')
rooms = set()   # Devemos adicionar manualmente as salas do DEMAT aqui
for r in range(0, len(dfrooms['Salas'].values)):
    Room = Sala(int(dfrooms['Salas'].values[r]))
    for day in range(1, 6):
        Room.h_ocupados[dfrooms.columns[day]] = dfrooms[dfrooms.columns[day]].values[:]
    rooms.add(Room)

# Conjunto de todas as matérias do DEMAT
# Devemos adicionar essas informações manualmente 'nome': quantidade de horários seguidos que deve ter
subjects = {'Matéria':{'numero de horários seguidos': 'N', 'Salas que pode ser ocupadas': []}}


# Criar um set com todos os professores
# Declarar todos eles também como sendo da classe professores
professores_nome = set()
all_teachers = set()
for p in range(0, len(df['Professor'].values)):
    teacher = Professor(df['Professor'].values[p])

    str_prefer = df['Preferências'].values[p]
    list_prefer = str_prefer.split('-')

    for preferencias_do_professor in list_prefer:
        if 'N' in preferencias_do_professor.upper:
            teacher.prefer[0].add(preferencias_do_professor)
        elif 'S' in preferencias_do_professor.upper:
            teacher.prefer[1].add(preferencias_do_professor)

    teacher.limitations.add(df['Limitações'].values[p])
    teacher.subjects.add(df['Matéria'].values[p])

    if not(p in professores_nome):  # Se o professor ainda não estiver na lista, adiciona ele
        professores_nome.add(df['Professor'].values[p])
        all_teachers.add(teacher)


# State vai ser o dicionário final. Ele é o que deve ser trasformado em um data frame
# Apenas o state mais barato será trasformado em resultado final.
result_state = {}
for nome in range(len(professores_nome)):
    for teacher_in_class in all_teachers:
        if nome == teacher_in_class.name:
            result_state[nome] = teacher_in_class.classes

dict_base = {}
for rooms_for_creat_initial_state in rooms:
    dict_base[rooms_for_creat_initial_state] = []
initial_state = {'segunda': dict_base[:], 'terça': dict_base[:], 'quarta': dict_base[:], 'quinta': dict_base[:], 'sexta': dict_base[:]}


# primeiro node
first_node = Node(initial_state[:], 0)
greedy = Frontier()
greedy.frontier.append(first_node)

# Espandir
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




