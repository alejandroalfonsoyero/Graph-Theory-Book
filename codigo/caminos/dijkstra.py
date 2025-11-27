"""
Implementación del algoritmo de Dijkstra para caminos mínimos
"""

import heapq
from typing import Dict, List, Optional, Tuple
import sys
sys.path.append('..')
from estructuras.grafo import Grafo


def dijkstra(grafo: Grafo, inicio: int) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
    """
    Algoritmo de Dijkstra para caminos más cortos desde un nodo fuente
    
    Requisito: Todos los pesos deben ser no negativos
    
    Args:
        grafo: Grafo con pesos no negativos
        inicio: Nodo inicial
    
    Returns:
        Tupla (distancias, padres)
        - distancias: {nodo: distancia_mínima_desde_inicio}
        - padres: {nodo: nodo_predecesor} para reconstruir caminos
    
    Complejidad: O((V + E) log V) con binary heap
                O(V log V + E) con Fibonacci heap
    """
    distancia = {i: float('inf') for i in range(grafo.n)}
    distancia[inicio] = 0
    padre = {i: None for i in range(grafo.n)}
    
    # Cola de prioridad: (distancia, nodo)
    pq = [(0, inicio)]
    visitado = set()
    
    while pq:
        dist_u, u = heapq.heappop(pq)
        
        if u in visitado:
            continue
        
        visitado.add(u)
        
        # Relajar aristas salientes
        for arista in grafo.vecinos(u):
            v = arista.destino
            peso = arista.peso
            
            if distancia[u] + peso < distancia[v]:
                distancia[v] = distancia[u] + peso
                padre[v] = u
                heapq.heappush(pq, (distancia[v], v))
    
    return distancia, padre


def dijkstra_camino(grafo: Grafo, inicio: int, destino: int) -> Tuple[float, Optional[List[int]]]:
    """
    Versión de Dijkstra que retorna distancia y camino a un destino específico
    
    Returns:
        Tupla (distancia, camino)
        - distancia: distancia mínima o inf si no alcanzable
        - camino: lista de nodos o None si no alcanzable
    """
    from .utils import reconstruir_camino
    
    distancias, padres = dijkstra(grafo, inicio)
    camino = reconstruir_camino(padres, inicio, destino)
    
    return distancias[destino], camino


def dijks

tra_early_stop(grafo: Grafo, inicio: int, destino: int) -> Tuple[float, List[int]]:
    """
    Dijkstra optimizado que termina al alcanzar el destino
    Útil cuando solo necesitamos un camino específico
    """
    distancia = {i: float('inf') for i in range(grafo.n)}
    distancia[inicio] = 0
    padre = {i: None for i in range(grafo.n)}
    
    pq = [(0, inicio)]
    visitado = set()
    
    while pq:
        dist_u, u = heapq.heappop(pq)
        
        if u == destino:
            # Encontramos el destino, reconstruir camino
            camino = []
            actual = destino
            while actual is not None:
                camino.append(actual)
                actual = padre[actual]
            return dist_u, camino[::-1]
        
        if u in visitado:
            continue
        
        visitado.add(u)
        
        for arista in grafo.vecinos(u):
            v = arista.destino
            peso = arista.peso
            
            if distancia[u] + peso < distancia[v]:
                distancia[v] = distancia[u] + peso
                padre[v] = u
                heapq.heappush(pq, (distancia[v], v))
    
    return float('inf'), []
