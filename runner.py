from functions.base import *
from functions import convert2day as convert
import pandas as pd
import random

# ================================================
# ============== RECEBE INFORMAÇÕES ==============
# ================================================

df = pd.read_excel('Planilha.xlsx', 'Sheet1')
# Coloca todos os professores na classe professor
all_teacher_names = set()
all_teachers = []
for teacher in range(0, len(df['Professor'])):
    if df['Professor'][teacher] not in all_teacher_names:
        P = Professor(df['Professor'][teacher])
        all_teachers.append(P)

    # Transformamos os inputs em listas e então adicionamos aos seus respectivos lugares na classe professor
    preferencias = str(df['Preferencias'][teacher]).split('-')
    limitacoes = str(df['Limitacoes'][teacher]).split('-')
    P.prefer[0].add(p for p in preferencias if 'S' in p)
    P.prefer[1].add(p for p in preferencias if 'N' in p)
    P.limitations.add(l[1] for l in limitacoes if str(l) != 'nan')

    n_aulas = 0   # Será usado para checar se há algum erra no código ao final

    for colum_name in df.columns[5:]:
        n_aulas += df[colum_name][teacher]
    P.n_aulas += n_aulas
    lin = list(df.loc[teacher])
    for classes in range(5, len(lin)):
        if str(lin[classes]) != 'nan':
            for aulas in range(0, int(lin[classes])):
                x = Node(
                    subject=df['Materia'][teacher],
                    teacher=P,
                    classroom=df.columns[classes]
                )
                P.subjects.add(x)

# Lista com os dias da semana
week_days = [2, 3, 4, 5, 6]

# Organizar all_teacher de modo que os primeiros sejam os com maiores restrições
for teacher in all_teachers:
    c = 0
    while len(teacher.limitations) < len(all_teachers[c].limitations):
        c += 1
    all_teachers.remove(teacher)
    all_teachers.insert(c, teacher)

# Lista com todas as aulas
all_classes = []

# ===================================================
# ============== PROCESSAR INFORMAÇÕES ==============
# ===================================================

# Criar planilha inicial (aleatória)
planilha = {}  # {Sala: [horários], ...}
for colum_name in df.columns[5:]:
    planilha[colum_name] = {2: [],
                            3: [],
                            4: [],
                            5: [],
                            6: []}

for teacher in all_teachers:
    for subj in teacher.subjects:
        # (matéria, numero de aulas, sala)
        # Colocar cada uma das aulas desse professor na planilha
        # Colocar todas as aulas do professor na segunda, se não couber colocar na terça, e assim por adiante
        day = 2
        while len(planilha[subj.classroom][day]) == 6:   # Não está passando daqui
            day += 1
            if len(planilha[subj.classroom][day]) > 6:
                print(planilha[subj.classroom][day])
                print('Error: len(planilha[subj[2]][day) > 6')
        if day in teacher.limitations:
            day += 1
        planilha[subj.classroom][day].append(subj)
        subj.get_position((day, planilha[subj.classroom][day].index(subj)))
        all_classes.append(subj)
NONE = 0
for info in planilha.values():
    for horario in info.values():
        n_zeros_para_colocar = 6 - len(horario)
        for c in range(0, n_zeros_para_colocar):
            horario.append(NONE)
for key in planilha.keys():
    print(key)
    for value in planilha[key].values():
        print(value)


# Expandir planilha e selecionar qual o melhor | Aprimoramento
# Quando um estado transitório possui esse ganho ou maior, ele já será automaticamente escolhido
best_cost = 0
while True:

    achamos_o_resultado_individual = True  # Se depois de tudo ainda for 'Sim' então a planilha inicial vai ser a melhor
    achamos_o_resultado_membro = True

    # Selecionar um grupo de 10 horários
    big_group = all_classes[:10]
    # Selecionar outros 10 que serão modificados separadamente
    individuals = [i for i in all_classes[10:20]]

    # expandir cada um 10X: criar 10 estados a partir de cada um deles
    used_position = set()
    for indivi in individuals:
        original_position = indivi.position
        used_position.clear()
        # selecionar qual a sala
        for c in range(0, 10):
            planilha_transitoria = planilha.copy()
            print(planilha_transitoria)
            # Item aleatório da lista de dias da semana
            while True:
                day = random.choice(week_days)
                if not (day in indivi.teacher.limitations):
                    break
            # Item aleatório dos horários desse dia
            while True:   # Falta ainda colocar se esse horário está condizendo com as leis trabalhistas
                print(planilha_transitoria[indivi.classroom][day])
                selected_h = random.choice(planilha_transitoria[indivi.classroom][day])
                print(selected_h)
                if not ((day, selected_h) in used_position):
                    break
            # Efetuar a troca entre esses horários
            position_h = planilha_transitoria[indivi.classroom][day].index(selected_h)
            planilha_transitoria[indivi.classroom][day].remove(selected_h)
            planilha_transitoria[indivi.classroom][day].insert(position_h, indivi)

            planilha_transitoria[indivi.classroom][indivi.position[0]].remove(indivi)
            planilha_transitoria[indivi.classroom][indivi.position[0]].insert(indivi.position[1], selected_h)

            if selected_h != 0:
                selected_h.get_position((indivi.position[0], indivi.position[1]))
            indivi.get_position((day, position_h))

            # Adicionar esse novo estado à states.
            used_position.add((day, position_h))

            # Avaliar se o estado atual é o melhor ou não
            if best_cost < cost(all_teachers):
                best_state = planilha_transitoria.copy()
                best_cost = cost(all_teachers)
                #Atualizar a posição do position do Node
                best_state_positions_indivi = indivi.position
                achamos_o_resultado = False
        indivi.get_position(original_position)
    # Expandir o grupo de 10
    planilha_transitoria2 = planilha.copy()

    for turn in range(0, 10):
        origanal_positions = []
        for member in big_group:
            original_positions.append((member, member.position))
            # Repetimos o mesmo processo acima representado
            # Selecionamos um horário aleatório, trocamos de posição com o horário member e então criamos um novo estado
            day = random.choice(week_days)
            selected_h = rendom.choice(planilha_transitoria2[member.classroom][day])
            position_h = planilha_transitoria2[member.classroom][day].index(selected_h)

            planilha_transitoria2[member.classroom][day].remove(selected_h)
            planilha_transitoria2[member.classroom][day].insert(member)

            planilha_transitoria2[member.classroom][member.position[0]].remove(member)
            planilha_transitoria2[member.classroom][member.position[0]].insert(member.position[1], selected_h)

            selected_h.get_position((member.position[0], member.position[1]))
            member.get_position((day, position_h))


        achamos_o_resultado_membro = False
        if cost(planilha_transitoria2) > best_cost:
            best_state = planilha_transitoria2.copy()
            best_cost = cost(all_teachers)
        else:
            for member in big_group:
                for thing in original_position:
                    if member == thing[0]:
                        member.position = thing[1]

# Se a melhor planilha for a inicial, antes de ser expandida, achamos o nosso resultado
    if achamos_o_resultado_individual or achamos_o_resultado_membro:
        result = planilha.copy()
        break
    else:
        planilha = best_state.copy()
        best_cost = cost(planilha)
# Converter resultado em um resultado final
#    xData terão o formato: {"COLLUMN 1, dia": [valores], ...}
#    yData será a primeira coluna da planilha, tendo o formato: {"Nome das linhas": [lista de nomes das linhas]}
#    # Formato dos valores xData -> ['2-Desenho Técnico', '3-Desenho Técnico', '5-EAP', '7-Circuitos Elétricos 2:2', '9-Circuitos Elétricos 2:2', '10-EAP:3', '11-EAP:2', '12-Circuitos Elétricos 2:2']
#   ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
#xData =