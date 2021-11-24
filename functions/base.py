# Aqui se encontraram as funções que vamos usar no código teste
import pandas as pd


class Professor:
    def __init__(self, name):
        self.name = name
        # Grade de horários que o professor vai dar aula
        self.classes = {'segunda': [], 'terça': [], 'quarta': [], 'quinta': [], 'sexta': []}
        # Todos os horários do professor, Nodes
        self.subjects = set()
        # Preferências de dias que ele quer (primeira lista) ou não (segunda lista) dar aula para cada matéria
        self.prefer = [set(), set()]  # uma lista de 2 sets para cada matéria do professor
        # Limitações de dias que ele não pode dar aula
        self.limitations = set()
        # Número de aulas em todas as matérias que ela dá aula
        self.n_aulas = 0



class Sala:
    def __init__(self, local):
        # Número da sala
        self.local = local
        # Lista com todos os horários que a sala esta sendo usada, e portanto não pode ser usada pelo técnico.
        self.h_ocupados = {'segunda': [], 'terça': [], 'quarta': [], 'quinta': [], 'sexta': []}
        # Lista com os horários designados para a sala
        self.horarios = {'segunda': [], 'terça': [], 'quarta': [], 'quinta': [], 'sexta': []}


class Node:
    """Nodes são os horários, cada bloquinho de horário que corresponde a uma aula do professor"""
    def __init__(self, subject, teacher, classroom):
        self.teacher = teacher
        self.classroom = classroom
        self.subject = subject

        self.position = None

    def __repr__(self):
        return f'{self.teacher.name}_{self.subject}'

    def get_position(self, position):
        # Posição é uma tupla contendo (dia, horário)
        self.position = position




class Frontier:
    """
    Frontier é uma lista que possui todos os possíveis valore s dos quais ainda se pode evoluir
    """

    def __init__(self):
        self.frontier = []

    def add_node(self, node):
        """
        Ao se colocar um novo estado, ele deve estar em ordem crescente de custo,
        de forma que o mais barato seja sempre o primeiro
        :param node:
        :param state: Novo estado que será adicionado a lista de possiveis estados para se evoluir
        :return:
        """
        for node_in_frontier in range(0, len(self.frontier)):
            if node.cost <= self.frontier[node_in_frontier].cost:
                self.frontier.insert(node_in_frontier, node)

    def select_node(self):
        """
        Retira um valor da lista que deverá ser espandido
        :return: valor com o menor custo da lista, no caso o primeiro
        """
        lowest_cost_node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return lowest_cost_node


def cost(all_teachers):
    """
    Recebe a lista com os professores e retorna o valor daquela estrutura de horários
    Para isso devemos estipular valores para cada situação
    (X)Quão importante é um professor que quer dar aula nesse dia dar, 15
    (X)Quão importante é para os professores não terem horários picados durante o dia 10
    ( )Apenas uma pessoa saiu prejudicada ou a questão de horários seguidos e buracos foi distribuida igualmente
    :param state: Grade de horários atual
    :return: custo do caminho
    """
    week_h = {2: list(0 for c in range(0, 5)),
              3: list(0 for c in range(0, 5)),
              4: list(0 for c in range(0, 5)),
              5: list(0 for c in range(0, 5)),
              6: list(0 for c in range(0, 5))}
    value = 0
    for teacher in all_teachers:
        week_s = week_h.copy()
        for subj in teacher.subjects:
            # Primeira categoria de avaliação
            if subj.position[0] in teacher.prefer[0]:
                value += 15
            elif subj.position[0] in teacher.prefer[1]:
                value -= 15

            # Segunda categoria de avaliação
            print('week', week_s[subj.position[0]], subj.position[1])
            del week_s[subj.position[0]][subj.position[1]]
            week_s[subj.position[0]].insert(subj.position[1], subj)
        for day_h in week_s.values():
            # Se tem algum furo nesses horários
            for character in range(0, len(day_h)):
                if day_h[0] == 0:
                    del day_h[0]
                else:
                    pass
            for charac in range(0, len(day_h)):
                if day_h[-1] == 0:
                    del day_h[-1]
                else:
                    pass
            zeros = day_h.count(0)
            value -= zeros * 5
            if zeros == 0:
                value += 10
    return value





    # Diferença entre dois horários de um professor, não ter nenhum no meio
    # Se isso for colocado provavelmente ele colocará todos os horários de uma pessoa para depois colocar os outros


def proibitions(state):
    """
    Nos diz se a atual grade de horários pode ser usada ou não
    :param state: Grade de horários atual
    :return: True se estiver tudo ok, False se não for uma entrada válida
    """

    # diferença entre o último horário de um dia e o primeiro do próximo maior que 11h, pode
    # tempo de almoço menor que 3 horas, pode
    # Carga horária no dia de menor que 8h, pode


def is_final_result(state):
    """
    Analiza se o estado do node é o resultado final, se todos os professores que tinham aula já foram colocados
    :param state:
    :return:
    """


def check(resultado_do_programa):
    """
    :param resultado_do_programa: O resultado final do programa, a planilha
    :return: Se o resultado é válido True or False
    """
