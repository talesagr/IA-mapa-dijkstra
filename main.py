import heapq

# Definição do ambiente
def inicializar_ambiente():
    ambiente = [['.' for _ in range(6)] for _ in range(6)]
    return ambiente

# Definição das posições iniciais dos elementos
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

# Definição da função para encontrar o menor caminho usando Dijkstra
def dijkstra(grafo, inicio, fim):
    fila = [(0, inicio, [])]
    visitados = set()
    heapq.heapify(fila)
    
    while fila:
        (custo, vertice, caminho) = heapq.heappop(fila)
        if vertice not in visitados:
            visitados.add(vertice)
            caminho = caminho + [vertice]
            if vertice == fim:
                return (custo, caminho)
            for vizinho in grafo[vertice]:
                if vizinho[0] not in visitados:
                    heapq.heappush(fila, (custo + vizinho[1], vizinho[0], caminho))
    
    return float("inf"), []

# Construção do grafo
def construir_grafo(ambiente):
    grafo = {}
    for i in range(len(ambiente)):
        for j in range(len(ambiente[i])):
            if ambiente[i][j] != '#':
                vizinhos = []
                if i > 0 and ambiente[i - 1][j] != '#':
                    vizinhos.append(((i - 1, j), 1))
                if i < len(ambiente) - 1 and ambiente[i + 1][j] != '#':
                    vizinhos.append(((i + 1, j), 1))
                if j > 0 and ambiente[i][j - 1] != '#':
                    vizinhos.append(((i, j - 1), 1))
                if j < len(ambiente[i]) - 1 and ambiente[i][j + 1] != '#':
                    vizinhos.append(((i, j + 1), 1))
                grafo[(i, j)] = vizinhos
    return grafo

# Exibição do ambiente
def exibir_ambiente(ambiente):
    print("Ambiente:")
    for linha in ambiente:
        print(" ".join(linha))

# Posições iniciais dos elementos
entrada = (0, 0)
saida = (5, 5)
zumbis = [(1, 1), (2, 2), (3, 3), (4, 4), (1, 5), (2, 4), (3, 1), (4, 2)]
presentes = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (5, 2), (5, 3), (5, 4)]
paredes = [(0, 2), (2, 0)]

ambiente = inicializar_ambiente()
ambiente = definir_posicoes_iniciais(ambiente, entrada, saida, zumbis, presentes, paredes)

grafo = construir_grafo(ambiente)

custo_caminho, caminho = dijkstra(grafo, entrada, saida)

for posicao in caminho:
    ambiente[entrada[0]][entrada[1]] = '.'  # Remover a posição atual do agente
    ambiente[posicao[0]][posicao[1]] = 'E'  # Atualizar a posição do agente
    entrada = posicao  # Atualizar a posição atual do agente
    exibir_ambiente(ambiente)
    input("Pressione Enter para continuar...")

print("Fim da simulação.")
