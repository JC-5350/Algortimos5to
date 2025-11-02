# Programa: cableado y análisis de grafo de colonias

import math
import networkx as nx
import itertools

# 1️ Leer el archivo de entrada
with open("entrada.txt", "r") as f:
    lineas = [line.strip() for line in f.readlines() if line.strip()]

# Número de colonias
N = int(lineas[0])

# Matriz de distancias
inicio_dist = 1
fin_dist = inicio_dist + N
matriz_dist = [list(map(int, lineas[i].split())) for i in range(inicio_dist, fin_dist)]

# Matriz de capacidades
inicio_cap = fin_dist
fin_cap = inicio_cap + N
matriz_cap = [list(map(int, lineas[i].split())) for i in range(inicio_cap, fin_cap)]

# Coordenadas 
coords = [tuple(map(int, lineas[i].replace("(", "").replace(")", "").split(",")))
          for i in range(fin_cap, len(lineas))]

# Nombres de colonias
nombres = [chr(65 + i) for i in range(N)]  # A, B, C, D...

# 2️ Forma óptima de cablear con fibra óptica 
G = nx.Graph()
for i in range(N):
    for j in range(i + 1, N):
        if matriz_dist[i][j] != 0:
            G.add_edge(nombres[i], nombres[j], weight=matriz_dist[i][j])

mst = nx.minimum_spanning_tree(G)
print("1️ Forma de cablear con fibra óptica (árbol de expansión mínima):")
print(list(mst.edges(data="weight")))
print()

# 3️ Ruta más corta que visite todas las colonias
# Nota: se usa fuerza bruta 
mejor_ruta = None
min_dist = float("inf")

for perm in itertools.permutations(range(1, N)):
    ruta = [0] + list(perm) + [0]
    dist = sum(matriz_dist[ruta[i]][ruta[i + 1]] for i in range(N))
    if dist < min_dist:
        min_dist = dist
        mejor_ruta = ruta

ruta_letras = [nombres[i] for i in mejor_ruta]
print("2 Ruta más corta del repartidor (TSP):")
print(" → ".join(ruta_letras), f"Distancia total = {min_dist} km")
print()

# 4️ Flujo máximo entre nodo inicial y final (Ford-Fulkerson / Edmonds–Karp)
Gflujo = nx.DiGraph()
for i in range(N):
    for j in range(N):
        if matriz_cap[i][j] > 0:
            Gflujo.add_edge(nombres[i], nombres[j], capacity=matriz_cap[i][j])

flujo_max, flujo_dict = nx.maximum_flow(Gflujo, nombres[0], nombres[-1])
print("3️ Flujo máximo de información (de", nombres[0], "a", nombres[-1], "):", flujo_max)
print()

# 5️ Calcular central más cercana a cada punto (uso de distancia euclidiana)
def distancia(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

poligonos = []
for i, p1 in enumerate(coords):
    mas_cercano = min(coords, key=lambda p2: distancia(p1, p2) if p1 != p2 else float("inf"))
    poligonos.append([p1, mas_cercano])

print("4️ Lista de polígonos (pares de puntos más cercanos):")
for poly in poligonos:
    print(poly)
