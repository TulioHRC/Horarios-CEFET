# Aqui se encontraram as funções que vamos usar no código teste
import pandas as pd

df = pd.read_excel('Planilha esperada.xlsx', 'Sheet1')


class Professor:
    def __init__(self, name):
        self.name = name
        # Grade de horários que o professor vai dar aula
        self.classes = {'segunda': [], 'terça': [], 'quarta': [], 'quinta': [], 'sexta': []}
        # Matérias que o professor da aula
        self.subjects = set()
        # Preferências de dias que ele quer ou não dar aula
        self.prefer = [set(), set()]
        # Limitações de dias que ele não pode dar aula
        self.limitations = set()


class Sala:
    def __init__(self, local):
        # Número da sala
        self.local = local
        # Lista com todos os horários que a sala esta sendo sada por outro grupo.
        self.h_ocupados = {'segunda': [], 'terça': [], 'quarta': [], 'quinta': [], 'sexta': []}
        # Lista com os horários da sala
        self.horarios = {'segunda': [], 'terça': [], 'quarta': [], 'quinta': [], 'sexta': []}


class Node:
    def __init__(self, state_of_node, cost_of_node, parent=0):
        self.state = state_of_node
        self.cost = cost_of_node

        # Se o número de filhos for igual ao número de possiveis filhos. O node deve ser removido do frontier
        # caso contrário geraria um looping.
        self.number_sons = 0
        # A partir de qual node ela foi criada.
        self.parent = parent



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

def cost(state, new_h):
    """
    Recebe a grade de horários que foi criada até o momento e
    retorna quanto que aquele movimento custaria.
    Para isso devemos estipular valores para cada cituação
    Quão importante é um professor que quer dar aula nesse dia dar, 15
    Quão importante é para os professores não terem horários picados durante o dia 10
    Apenas uma pessoa saiu prejudicada ou a questão de horários seguidos e buracos foi distribuida igualmente
    :param state: Grade de horários atual
    :param new_h:
    :return: custo do caminho
    """
    # Diferença entre dois horários de um professor, não ter nenhum no meio
        # Se isso for colocado provavelmente ele colocará todos os horários de uma pessoa para depois colocar os outros


def proibitions(state, new_h):
    """
    Nos diz se a atual grade de horários pode ser usada ou não
    :param state: Grade de horários atual
    :param new_h: Novo horário
    :return: True se estiver tudo ok, False se não for uma entrada válida
    """

    # diferença entre o último horário de um dia e o primeiro do próximo maior que 11h, pode
    # tempo de almoço menor que 3 horas, pode
    # Carga horária no dia de menor que 8h, pode


def make_move(state): # O movimento deve ser sempre ao lado de algum horário que já tenha sido marcado
                      # Evita que sejam criados um monte de estados iniciais aleatórios




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


def check(resultado_do_programa):
    """
    :param resultado_do_programa: O resultado final do programa, a planilha
    :return: Se o resultado é válido True or False
    """