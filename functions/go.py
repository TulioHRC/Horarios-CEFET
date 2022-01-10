from functions import loadData
#from functions import classes as c
from functions import result
from classes import Horario
import random

NUMERO_DE_REPETIÇÕES = 10

def mainFunction():  # A função principal do código, que retornará o resultado que nós esperamos
    # Mct 1 A  ->   MCT-1A
    # =================== Pegando os dados que nós fornecemos
    try:
        teachersData = loadData.getDatabase('../Planilha.xlsx')
        teachersColumns = loadData.getDatabase('../Planilha.xlsx', get="columns")
        roomsData = loadData.getDatabase('../Planilha sala.xlsx')
        pointsData = loadData.getPoints('../data/preferencias.txt')
        #print(
            #teachersData,
        #)
    except Exception as e:
        print(f"Houve um erro ao tentar pegar os dados das planilhas.\n{e}")
    # Unificando os nomes das salas
    #for turma in teachersData.keys()[7:]:

    # ==================== Criando os nodes
    todos_os_horarios = []
    for l in range(0, len(teachersData.values())):
        for coluna in list(teachersData.keys())[7:]:
            if not (str(teachersData[coluna][l]) == 'nan'):
                for h in range(0, int(teachersData[coluna][l])):  # Pego a quantidade de aulas que ele vai dar para essa turma nessa matéria
                    if teachersData['Tipo'][l] == 'Manha':
                        horario = Horario(
                            teacher=teachersData['Professor'][l],                                 # Professor
                            subject=teachersData['Materia'][l],                                   # Matéria
                            turm=f'{coluna}-{teachersData["Ano"][l]}',                            # Turma
                            possible_h=[1, 2, 3, 4, 5]                                            # Possíveis horários que podemos colocá-lo
                        )
                        todos_os_horarios.append(horario)
                    else:
                        horario = Horario(
                            teacher=teachersData['Professor'][l],                                 # Professor
                            subject=teachersData['Materia'][l],                                   # Matéria
                            turm=f'{coluna}-{teachersData["Ano"][l]}{teachersData["Letra"][l]}',  # Turma
                            possible_h=[6, 7, 8, 9, 10]                                           # Possíveis horários que podemos colocá-lo
                        )
                        todos_os_horarios.append(horario)
    print(todos_os_horarios)
    # ==================== Processando os dados: Gerando a planilha final com base nos dados
    for c in range(0, NUMERO_DE_REPETIÇÕES):

        lista_embaralhada = todos_os_horarios.copy()  # Lista com todos os nodes que ainda dever ser colocados
        random.shuffle(lista_embaralhada)
        """
        ramdom.shuffle(lista_dos_professore)
        for professor in lista_de_professores:
            horarios = professor.horarios
            horarios_individuais = []
            for h in horarios.items():
                materia = h[0]
                for turma in h[1].items():
                    turma_do_ horario = turma[0]
                    for c in range(0, turma[1]):
                        horarios_indiciduais.append({professor}{turma}{materia})   
            {MATEMATICA: {MCT: 2, MEC: 1, } 
        """
        while len(lista_embaralhada) != 0:
            # Retiro o primeiro item da lista e o coloco na variável node
            horario = lista_embaralhada[0]
            lista_embaralhada = lista_embaralhada[1:]



            # Seleciono qual o melhor estado para aquele node e o coloco nele





    # ====================== Gerando o resultado dos melhores horários

    for teacher in teachers:
        for subject in teacher.subjects:  # Por matéria do professor
            for turm in classes:
                if turm.name[-2] == subject[-1]:  # Se o ano da turma for igual ao da matéria
                    lastResp = "a"  # Ultima resposta
                    for i in range(teacher.getClassesNum(turm.name, subject)):  # Gera um para cada aula da matéria
                        resp = teacher.bestHour(turm, subject[0:-2], alreadyChose=turm.schedule, classNumber=i,
                                                points=pointsData, lastResp=lastResp)  # Melhor horário para cada turma

                        if resp == 0: continue  # Pula professor, não tem aula nessa matéria
                        # Salvando novo horário nos horários
                        turm.schedule[resp[0]].append(resp[1])  # -------------- turma
                        turm.schedule[resp[0]].sort(key=sortFunction)  # Coloca em ordem 1,2,3 nos horários

                        teacher.schedule[resp[0]].append(f"{resp[1]} - {turm.name}")  # ------------ professor
                        teacher.schedule[resp[0]].sort(key=sortFunction)

                        lastResp = resp

    # Criando planilhas
    for turm in classes:
        result.saveSheet(turm.name, turm.schedule, type='turm')
    for teacher in teachers:
        result.saveSheet(teacher.name, teacher.schedule, type='teacher')


def sortFunction(e):
    return int(e.split('-')[0])  # Função do sort de turm.schedule

mainFunction()