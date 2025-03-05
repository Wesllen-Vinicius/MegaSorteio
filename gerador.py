import random
import os
from collections import Counter

def carregar_numeros_excluidos(tipo_jogo):
    arquivo = f"numeros/sorteados_{tipo_jogo}.txt"
    if not os.path.exists(arquivo):
        return set()
    with open(arquivo, 'r') as file:
        return {tuple(map(int, linha.split())) for linha in file if len(linha.split()) in [6, 15, 5]}

def eh_primo(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def eh_fibonacci(n):
    a, b = 0, 1
    while b < n:
        a, b = b, a + b
    return b == n or a == n

def calcular_frequencias(tipo_jogo):
    arquivo = f"numeros/sorteados_{tipo_jogo}.txt"
    if not os.path.exists(arquivo):
        return Counter()
    with open(arquivo, 'r') as file:
        return Counter(int(n) for linha in file for n in linha.split())

def gerar_numeros(quantidade, intervalo, numeros_excluidos, frequencia_numeros):
    max_tentativas = 1000
    for _ in range(max_tentativas):
        numeros_possiveis = list(range(1, intervalo + 1))
        numeros_possiveis.sort(key=lambda x: frequencia_numeros.get(x, 0), reverse=True)
        numeros_gerados = tuple(sorted(random.sample(numeros_possiveis, quantidade)))
        
        if intervalo == 25:
            if not (5 <= sum(1 for n in numeros_gerados if n % 2 == 0) <= 10):
                continue
        
        elif intervalo == 60:
            if not (2 <= sum(1 for n in numeros_gerados if eh_primo(n)) <= 4):
                continue
        
        elif intervalo == 80:
            if not (1 <= sum(1 for n in numeros_gerados if eh_fibonacci(n)) <= 3):
                continue
        
        if numeros_gerados not in numeros_excluidos:
            return numeros_gerados
    raise ValueError(f"Não foi possível gerar um conjunto válido para {quantidade} números dentro de {intervalo} opções.")

JOGOS = {
    "mega": {"quantidade": 6, "intervalo": 60},
    "loto": {"quantidade": 15, "intervalo": 25},
    "quina": {"quantidade": 5, "intervalo": 80},
}

def gerar_sorteio(tipo_jogo):
    if tipo_jogo not in JOGOS:
        raise ValueError("Tipo de jogo inválido!")
    config = JOGOS[tipo_jogo]
    numeros_excluidos = carregar_numeros_excluidos(tipo_jogo)
    frequencia_numeros = calcular_frequencias(tipo_jogo)
    return gerar_numeros(config["quantidade"], config["intervalo"], numeros_excluidos, frequencia_numeros)
