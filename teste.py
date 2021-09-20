
from functions import *
import pandas as pd

# Demonstrando utilização do pandas
df = pd.read_excel('Planilha esperada.xlsx', 'Sheet1')   # Lendo a planilha do excel, e Sheet1 é o nome da aba do excel para ler
print(df) # Printando o dataframe encontrado na planilha

# Conjunto de todas as salas do DEMAT
dfrooms = pd.read_execel('Disponibilidade de salas', 'Sheet1')
rooms = set()   # Devemos adicionar manualmente as salas do DEMAT aqui
for r in range(0, len(dfrooms['Salas'].values)):
    Room = Sala(int(dfrooms['Salas'].values[r]))
    for day in range(1, 6):
        Room.h_ocupados[dfrooms.columns[day]] = dfrooms[dfrooms.columns[day]].values[:]
    rooms.add(Room)

# Criar um set com todos os professores
# Declarar todos eles também como sendo da classe professores
professores_nome = set()
professores_class = set()
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
    teacher.matérias.add(df['Matéria'].values[p])

    if not(p in professores_nome):  # Se o professor ainda não estiver na lista, adiciona ele
        professores_nome.add(df['Professor'].values[p])
        professores_class.add(teacher)


# State vai ser o dicionário final. Ele é o que deve ser trasformado em um data frame
# Apenas o state mais barato será trasformado em resultado final.
result_state = {}
for nome in range(len(professores_nome)):
    for teacher_in_class in professores_class:
        if nome == teacher_in_class.name:
            result_state[nome] = teacher_in_class.aulas

initial_state = {'segunda': {}, 'terça': {}, 'quarta': {}, 'quinta': {}, 'sexta': {}}
for room in rooms:
    S = Sala(room)





make_move(state):


for teacher_for_node in professores_class:  # Precisamos criar uma tupla contendo no primeiro termo o state referente e no segundo o custo.



