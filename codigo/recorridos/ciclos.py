"""
Algoritmos para detección de ciclos en grafos
"""

from typing import List, Optional, Tuple
import sys
sys.path.append('..')
from estructuras.grafo import Grafo


def tiene_ciclo_no_dirigido(grafo: Grafo) -> bool:
    """
    Detecta si existe un ciclo en un grafo no dirigido
    
    Args:
        grafo: Instancia de Grafo no dirigido
    
    Returns:
        True si existe un ciclo, False en caso contrario
    
    Complejidad: O(V + E)
    """
    visitado = set()
    
    def dfs(u: int, padre: int) -> bool:
        visitado.add(u)
        
        for arista in grafo.vecinos(u):
            v = arista.destino
            
            if v not in visitado:
                if dfs(v, u):
                    return True
            elif v != padre:
                # Back edge encontrado (no es el padre)
                return True
        
        return False
    
    # Verificar cada componente
    for vertice in range(grafo.n):
        if vertice not in visitado:
            if dfs(vertice, -1):
                return True
    
    return False


def tiene_ciclo_dirigido(grafo: Grafo) -> bool:
    """
    Detecta si existe un ciclo en un grafo dirigido
    
    Args:
        grafo: Instancia de Grafo dirigido
    
    Returns:
        True si existe un ciclo, False en caso contrario
    
    Complejidad: O(V + E)
    """
    # 0: blanco (no visitado), 1: gris (visitando), 2: negro (procesado)
    color = [0] * grafo.n
    
    def dfs(u: int) -> bool:
        color[u] = 1  # Marcar como visitando
        
        for arista in grafo.vecinos(u):
            v = arista.destino
            
            if color[v] == 1:
                # Back edge - ciclo detectado
                return True
            
            if color[v] == 0 and dfs(v):
                return True
        
        color[u] = 2  # Marcar como procesado
        return False
    
    for vertice in range(grafo.n):
        if color[vertice] == 0:
            if dfs(vertice):
                return True
    
    return False


def encontrar_ciclo_dirigido(grafo: Grafo) -> Optional[List[int]]:
    """
    Encuentra un ciclo en un grafo dirigido (si existe)
    
    Returns:
        Lista de nodos que forman un ciclo, o None si no hay ciclo
    
    Complejidad: O(V + E)
    """
    color = [0] * grafo.n
    padre = [-1] * grafo.n
    ciclo = []
    
    def dfs(u: int) -> bool:
        color[u] = 1
        
        for arista in grafo.vecinos(u):
            v = arista.destino
            
            if color[v] == 1:
                # Ciclo encontrado - reconstruirlo
                ciclo.append(v)
                actual = u
                while actual != v:
                    ciclo.append(actual)
                    actual = padre[actual]
                ciclo.reverse()
                return True
            
            if color[v] == 0:
                padre[v] = u
                if dfs(v):
                    return True
        
        color[u] = 2
        return False
    
    for vertice in range(grafo.n):
        if color[vertice] == 0:
            if dfs(vertice):
                return ciclo
    
    return None


def es_aciclico(grafo: Grafo) -> bool:
    """
    Verifica si un grafo es acíclico (DAG si es dirigido)
    
    Complejidad: O(V + E)
    """
    if grafo.dirigido:
        return not tiene_ciclo_dirigido(grafo)
    else:
        return not tiene_ciclo_no_dirigido(grafo)
