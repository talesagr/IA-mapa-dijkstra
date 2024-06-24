import numpy as np
import random
import time

alpha = 0.1
gamma = 0.9
epsilon = 0.1
episodes = 1000
max_steps = 100

def inicializar_ambiente():
    ambiente = [['.' for _ in range(6)] for _ in range(6)]
    return ambiente

def definir_posicoes_iniciais(ambiente, entrada, saida, zumbis, presentes, paredes):
    ambiente[entrada[0]][entrada[1]] = 'E'
    ambiente[saida[0]][saida[1]] = 'S'
    for zumbi in zumbis:
        ambiente[zumbi[0]][zumbi[1]] = 'Z'
    for presente in presentes:
        ambiente[presente[0]][presente[1]] = 'P'
    for parede in paredes:
        ambiente[parede[0]][parede[1]] = '#'
    return ambiente

def exibir_ambiente(ambiente):
    print("Ambiente:")
    for linha in ambiente:
        print(" ".join(linha))

def posicao_valida(ambiente, pos):
    x, y = pos
    if x < 0 or x >= len(ambiente) or y < 0 or y >= len(ambiente[0]):
        return False
    if ambiente[x][y] in ['#', 'Z']:
        return False
    return True

def escolher_acao(estado, q_table):
    if random.uniform(0, 1) < epsilon:
        return random.choice(['cima', 'baixo', 'esquerda', 'direita'])
    else:
        return max(q_table[estado], key=q_table[estado].get)

def obter_nova_posicao(pos, acao):
    x, y = pos
    if acao == 'cima':
        return (x-1, y)
    elif acao == 'baixo':
        return (x+1, y)
    elif acao == 'esquerda':
        return (x, y-1)
    elif acao == 'direita':
        return (x, y+1)

def obter_recompensa(ambiente, pos):
    x, y = pos
    if ambiente[x][y] == 'P':
        return 10
    elif ambiente[x][y] == 'S':
        return 100
    else:
        return -1

entrada = (0, 0)
saida = (5, 0)
zumbis = [(0, 2), (1, 4), (2, 1), (3, 2), (4, 1), (4, 4), (5, 1), (5, 2)]
presentes = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 3), (5, 4)]
paredes = [(0, 2), (2, 0)]

ambiente = inicializar_ambiente()
ambiente = definir_posicoes_iniciais(ambiente, entrada, saida, zumbis, presentes, paredes)

q_table = {}
for i in range(6):
    for j in range(6):
        q_table[(i, j)] = {'cima': 0, 'baixo': 0, 'esquerda': 0, 'direita': 0}

for episode in range(episodes):
    estado = entrada
    total_recompensa = 0
    passos = 0

    while estado != saida and passos < max_steps:
        acao = escolher_acao(estado, q_table)
        nova_posicao = obter_nova_posicao(estado, acao)

        if not posicao_valida(ambiente, nova_posicao):
            continue

        recompensa = obter_recompensa(ambiente, nova_posicao)
        total_recompensa += recompensa

        proximo_estado = nova_posicao
        q_table[estado][acao] = q_table[estado][acao] + alpha * (
            recompensa + gamma * max(q_table[proximo_estado].values()) - q_table[estado][acao]
        )

        estado = proximo_estado
        passos += 1

    print(f"Episódio {episode + 1}: Recompensa total = {total_recompensa}")

estado = entrada
caminho = [estado]

while estado != saida:
    acao = escolher_acao(estado, q_table)
    nova_posicao = obter_nova_posicao(estado, acao)

    if not posicao_valida(ambiente, nova_posicao):
        continue
    estado = nova_posicao
    caminho.append(estado)

print("Caminho percorrido pelo agente:", caminho)
print("Fim da simulação.")
