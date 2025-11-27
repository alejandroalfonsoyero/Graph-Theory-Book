"""
Implementación del algoritmo A* (A-Star)
"""

import heapq
from typing import Callable, Tuple, List, Optional
import sys
sys.path.append('..')
from estructuras.grafo import Grafo


def astar(grafo: Grafo, inicio: int, destino: int, 
          heuristica: Callable[[int, int], float]) -> Tuple[float, Optional[List[int]]]:
    """
    Algoritmo A* para encontrar camino más corto con heurística
    
    Args:
        grafo: Grafo ponderado
        inicio: Nodo inicial
        destino: Nodo destino
        heuristica: Función h(nodo, destino) -> costo_estimado
                   Debe ser admisible (nunca sobreestimar)
    
    Returns:
        Tupla (distancia, camino)
        - distancia: costo del camino encontrado
        - camino: lista de nodos, o None si no existe
    
    Complejidad: O(E log V) en el mejor caso (con buena heurística)
                O((V+E) log V) en el peor caso (como Dijkstra)
    """
    g_score = {i: float('inf') for i in range(grafo.n)}
    g_score[inicio] = 0
    
    f_score = {i: float('inf') for i in range(grafo.n)}
    f_score[inicio] = heuristica(inicio, destino)
    
    padre = {i: None for i in range(grafo.n)}
    
    # Cola de prioridad: (f_score, nodo)
    pq = [(f_score[inicio], inicio)]
    visitado = set()
    
    while pq:
        _, u = heapq.heappop(pq)
        
        if u == destino:
            # Reconstruir camino
            camino = []
            actual = destino
            while actual is not None:
                camino.append(actual)
                actual = padre[actual]
            return g_score[destino], camino[::-1]
        
        if u in visitado:
            continue
        
        visitado.add(u)
        
        for arista in grafo.vecinos(u):
            v = arista.destino
            tentative_g = g_score[u] + arista.peso
            
            if tentative_g < g_score[v]:
                padre[v] = u
                g_score[v] = tentative_g
                f_score[v] = g_score[v] + heuristica(v, destino)
                heapq.heappush(pq, (f_score[v], v))
    
    return float('inf'), None


def heuristica_euclidiana(coord1: Tuple[float, float], 
                          coord2: Tuple[float, float]) -> float:
    """
    Heurística de distancia euclidiana (para grafos geométricos)
    Admisible para movimiento en 8 direcciones o continuo
    
    Args:
        coord1: (x, y) del nodo actual
        coord2: (x, y) del nodo destino
    
    Returns:
        Distancia euclidiana
    """
    dx = coord1[0] - coord2[0]
    dy = coord1[1] - coord2[1]
    return (dx**2 + dy**2)**0.5


def heuristica_manhattan(coord1: Tuple[float, float],
                        coord2: Tuple[float, float]) -> float:
    """
    Heurística de distancia Manhattan (para grillas)
    Admisible para movimiento en 4 direcciones
    
    Args:
        coord1: (x, y) del nodo actual
        coord2: (x, y) del nodo destino
    
    Returns:
        Distancia Manhattan (L1)
    """
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])


def heuristica_chebyshev(coord1: Tuple[float, float],
                        coord2: Tuple[float, float]) -> float:
    """
    Heurística de distancia Chebyshev (para grillas con diagonales)
    Admisible para movimiento en 8 direcciones con costo uniforme
    
    Args:
        coord1: (x, y) del nodo actual
        coord2: (x, y) del nodo destino
    
    Returns:
        Distancia Chebyshev (L∞)
    """
    return max(abs(coord1[0] - coord2[0]), abs(coord1[1] - coord2[1]))


def greedy_best_first(grafo: Grafo, inicio: int, destino: int,
                     heuristica: Callable[[int, int], float]) -> Optional[List[int]]:
    """
    Búsqueda voraz guiada solo por heurística
    Rápido pero NO garantiza optimalidad
    
    Args:
        grafo: Grafo ponderado
        inicio: Nodo inicial
        destino: Nodo destino
        heuristica: Función de estimación
    
    Returns:
        Camino encontrado (no necesariamente óptimo), o None
    
    Complejidad: generalmente más rápido que A*, pero sin garantías
    """
    pq = [(heuristica(inicio, destino), inicio)]
    padre = {inicio: None}
    visitado = set()
    
    while pq:
        _, u = heapq.heappop(pq)
        
        if u == destino:
            camino = []
            actual = destino
            while actual is not None:
                camino.append(actual)
                actual = padre[actual]
            return camino[::-1]
        
        if u in visitado:
            continue
        
        visitado.add(u)
        
        for arista in grafo.vecinos(u):
            v = arista.destino
            if v not in padre:
                padre[v] = u
                heapq.heappush(pq, (heuristica(v, destino), v))
    
    return None
