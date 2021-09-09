# Aqui se encontraram as funções que vamos usar no código teste
import pandas as pd

df = pd.read_excel('Planilha esperada.xlsx', 'Sheet1')


class Professor:
    def __init__(self, name, topicos, aulas):
        self.name = name

        # Quais matérias o professor dá aula
        self.topicos = topicos

        # uma lista contendo um dicinário para cada matéria
        # Exemplo: lista[matéria]['sala'] == numero de aulas naquela sala
        self.aulas = aulas


class Materia:
    def __init__(self, name, pode_ser_seguido=0, ):
        self.name = name
        self.pode_ser_seguido = pode_ser_seguido


class Sala:
    def __init__(self, horarios, local):
        # Lista com os horários da sala
        self.horarios = horarios

        # Número da sala
        self.local = local


def cost(horários, new_h):
    """
    Recebe a grade de horários que foi criada até o momento e
    retorna quanto que aquele movimento custaria.
    Para isso devemos estipular valores para cada cituação
    Quão importante é um professor que quer dar aula nesse dia dar,
    Quão importante é os alunos não terem duas aulas seguidas de matéria teóricas
    Quão importante é para os professores não terem horários picados durante o dia
    :param horários:
    :param new_h:
    :return:
    """


def proibitions(horários, new_h):
    """
    Nos diz se a atual grade de horários pode ser usada ou não
    :param horários: Grade de horários atual
    :param new_h: Novo horário
    :return: True se estiver tudo ok, False se não for uma entrada válida
    """


def agrupar_professores_sala(posição_sala):
    """
    Recebe a informação de qual sala estamos nos referindo
    Agrupa todos os professores que dão aula nessa sala
    :return: lista com todos os professores que dão aula nessa sala
    """
    list_p = []
    for p in df['Professor'].values:
        info = df(df['Professor'] == p)
        if info[posição_sala] >= 0:
            list_p.append(p)
