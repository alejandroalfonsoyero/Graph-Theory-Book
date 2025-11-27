"""
Algoritmos para encontrar componentes conectados
"""

from typing import List, Set
import sys
sys.path.append('..')
from estructuras.grafo import Grafo


def componentes_conectados(grafo: Grafo) -> List[Set[int]]:
    """
    Encuentra todos los componentes conectados de un grafo no dirigido
    
    Args:
        grafo: Instancia de Grafo no dirigido
    
    Returns:
        Lista de conjuntos, cada uno representa un componente
    
    Complejidad: O(V + E)
    Espacio: O(V)
    """
    visitado = set()
    componentes = []
    
    def dfs(u: int, componente: Set[int]):
        visitado.add(u)
        componente.add(u)
        for arista in grafo.vecinos(u):
            v = arista.destino
            if v not in visitado:
                dfs(v, componente)
    
    for vertice in range(grafo.n):
        if vertice not in visitado:
            componente = set()
            dfs(vertice, componente)
            componentes.append(componente)
    
    return componentes


def es_conexo(grafo: Grafo) -> bool:
    """
    Verifica si un grafo no dirigido es conexo
    
    Args:
        grafo: Instancia de Grafo no dirigido
    
    Returns:
        True si el grafo es conexo, False en caso contrario
    
    Complejidad: O(V + E)
    """
    if grafo.n == 0:
        return True
    
    visitado = set()
    stack = [0]
    
    while stack:
        u = stack.pop()
        if u in visitado:
            continue
        visitado.add(u)
        
        for arista in grafo.vecinos(u):
            stack.append(arista.destino)
    
    return len(visitado) == grafo.n


def numero_componentes(grafo: Grafo) -> int:
    """
    Cuenta el número de componentes conectados
    
    Complejidad: O(V + E)
    """
    return len(componentes_conectados(grafo))


def mismo_componente(grafo: Grafo, u: int, v: int) -> bool:
    """
    Verifica si dos nodos están en el mismo componente conexo
    
    Complejidad: O(V + E) en el peor caso
    """
    visitado = set()
    stack = [u]
    
    while stack:
        actual = stack.pop()
        if actual == v:
            return True
        
        if actual in visitado:
            continue
        visitado.add(actual)
        
        for arista in grafo.vecinos(actual):
            stack.append(arista.destino)
    
    return False
