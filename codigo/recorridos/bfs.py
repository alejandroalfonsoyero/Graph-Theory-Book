"""
Implementaciones de BFS (Breadth-First Search)
"""

from collections import deque
from typing import Dict, List, Optional
import sys
sys.path.append('..')
from estructuras.grafo import Grafo


def bfs(grafo: Grafo, inicio: int) -> List[int]:
    """
    BFS básico usando cola
    
    Args:
        grafo: Instancia de Grafo
        inicio: Nodo inicial
    
    Returns:
        Lista de nodos en orden de visita
    
    Complejidad: O(V + E)
    Espacio: O(V)
    """
    visitado = set([inicio])
    queue = deque([inicio])
    orden_visita = []
    
    while queue:
        u = queue.popleft()
        orden_visita.append(u)
        
        for arista in grafo.vecinos(u):
            v = arista.destino
            if v not in visitado:
                visitado.add(v)
                queue.append(v)
    
    return orden_visita


def bfs_distancias(grafo: Grafo, inicio: int) -> Dict[int, int]:
    """
    BFS que calcula distancias desde un nodo fuente
    
    Returns:
        Diccionario {nodo: distancia_minima}
    
    Complejidad: O(V + E)
    """
    distancia = {inicio: 0}
    queue = deque([inicio])
    
    while queue:
        u = queue.popleft()
        
        for arista in grafo.vecinos(u):
            v = arista.destino
            if v not in distancia:
                distancia[v] = distancia[u] + 1
                queue.append(v)
    
    return distancia


def bfs_camino(grafo: Grafo, inicio: int, destino: int) -> Optional[List[int]]:
    """
    BFS que reconstruye el camino más corto
    
    Args:
        grafo: Instancia de Grafo
        inicio: Nodo inicial
        destino: Nodo destino
    
    Returns:
        Lista de nodos en el camino más corto, o None si no existe camino
    
    Complejidad: O(V + E)
    """
    if inicio == destino:
        return [inicio]
    
    padre = {inicio: None}
    queue = deque([inicio])
    
    while queue:
        u = queue.popleft()
        
        for arista in grafo.vecinos(u):
            v = arista.destino
            if v not in padre:
                padre[v] = u
                queue.append(v)
                
                if v == destino:
                    # Reconstruir camino
                    camino = []
                    actual = destino
                    while actual is not None:
                        camino.append(actual)
                        actual = padre[actual]
                    return camino[::-1]
    
    return None  # No existe camino


def bfs_multi_source(grafo: Grafo, fuentes: List[int]) -> Dict[int, int]:
    """
    BFS desde múltiples fuentes simultáneamente
    
    Útil para encontrar distancia al nodo más cercano de un conjunto
    
    Args:
        grafo: Instancia de Grafo
        fuentes: Lista de nodos fuente
    
    Returns:
        Diccionario {nodo: distancia_minima_a_cualquier_fuente}
    
    Complejidad: O(V + E)
    """
    distancia = {}
    queue = deque()
    
    # Inicializar todas las fuentes con distancia 0
    for fuente in fuentes:
        distancia[fuente] = 0
        queue.append(fuente)
    
    while queue:
        u = queue.popleft()
        
        for arista in grafo.vecinos(u):
            v = arista.destino
            if v not in distancia:
                distancia[v] = distancia[u] + 1
                queue.append(v)
    
    return distancia
