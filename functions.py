# Aqui se encontraram as funções que vamos usar no código teste

class Professor:
    def __init__(self, name, topicos, aulas):
        self.name = name

        # Quais matérias o professor dá aula
        self.topicos = topicos

        # uma lista contendo um dicinário para cada matéria
        # Exemplo: lista[matéria]['sala'] == numero de aulas naquela sala
        self.aulas = aulas


def agrupar_professores()