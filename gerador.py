import random

def carregar_numeros_excluidos(arquivo):
    """
    Lê os números do arquivo e retorna uma lista de conjuntos de números que foram excluídos.
    Cada linha do arquivo deve representar um conjunto de 6 números.
    """
    with open(arquivo, 'r') as file:
        conteudo = file.read().strip().splitlines()  # Lê as linhas do arquivo
        # Para cada linha, convertemos os números para um conjunto de inteiros
        conjuntos_excluidos = {tuple(map(int, linha.split())) for linha in conteudo}
    return conjuntos_excluidos

def gerar_numeros(numeros_excluidos):
    """
    Gera um novo conjunto de 6 números aleatórios entre 1 e 60, garantindo que o conjunto
    não tenha sido sorteado anteriormente.
    """
    # Inicializamos uma variável para o novo conjunto de números
    while True:
        # Gerar um conjunto de 6 números aleatórios entre 1 e 60
        numeros_gerados = tuple(sorted(random.sample(range(1, 61), 6)))
        
        # Verificar se esse conjunto de números já foi sorteado
        if numeros_gerados not in numeros_excluidos:
            return numeros_gerados
