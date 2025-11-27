"""
Implementación del algoritmo de Floyd-Warshall
"""

import numpy as np
from typing import List, Optional, Tuple
import sys
sys.path.append('..')
from estructuras.grafo import Grafo


def floyd_warshall(grafo: Grafo) -> Tuple[np.ndarray, np.ndarray]:
    """
    Algoritmo de Floyd-Warshall para caminos más cortos entre todos los pares
    
    Args:
        grafo: Grafo ponderado
    
    Returns:
        Tupla (distancias, siguiente)
        - distancias[i][j]: distancia más corta de i a j
        - siguiente[i][j]: próximo nodo en el camino de i a j
    
    Complejidad: O(V³)
    Espacio: O(V²)
    """
    n = grafo.n
    INF = float('inf')
    
    # Inicializar matrices
    dist = np.full((n, n), INF)
    siguiente = np.full((n, n), -1, dtype=int)
    
    # Caso base
    for i in range(n):
        dist[i][i] = 0
        siguiente[i][i] = i
    
    for u in range(n):
        for arista in grafo.vecinos(u):
            v = arista.destino
            dist[u][v] = arista.peso
            siguiente[u][v] = v
    
    # DP: considerar cada vértice como intermedio
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    siguiente[i][j] = siguiente[i][k]
    
    return dist, siguiente


def reconstruir_camino_fw(siguiente: np.ndarray, i: int, j: int) -> Optional[List[int]]:
    """
    Reconstruye el camino de i a j usando la matriz 'siguiente'
    
    Args:
        siguiente: Matriz de siguiente nodo (de Floyd-Warshall)
        i: Nodo inicial
        j: Nodo destino
    
    Returns:
        Lista de nodos en el camino, o None si no alcanzable
    """
    if siguiente[i][j] == -1:
        return None
    
    camino = [i]
    while i != j:
        i = siguiente[i][j]
        camino.append(i)
    
    return camino


def detectar_ciclo_negativo_fw(dist: np.ndarray) -> bool:
    """
    Detecta si hay ciclo negativo verificando la diagonal
    
    Args:
        dist: Matriz de distancias (de Floyd-Warshall)
    
    Returns:
        True si existe ciclo negativo
    """
    n = dist.shape[0]
    return any(dist[i][i] < 0 for i in range(n))


def floyd_warshall_con_caminos(grafo: Grafo) -> Tuple[np.ndarray, List[List[Optional[List[int]]]]]:
    """
    Versión que retorna todos los caminos explícitamente
    Útil para grafos pequeños
    
    Complejidad: O(V³) tiempo, O(V⁴) espacio en el peor caso
    """
    dist, siguiente = floyd_warshall(grafo)
    n = grafo.n
    
    # Construir todos los caminos
    caminos = [[None for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if dist[i][j] != float('inf'):
                caminos[i][j] = reconstruir_camino_fw(siguiente, i, j)
    
    return dist, caminos
