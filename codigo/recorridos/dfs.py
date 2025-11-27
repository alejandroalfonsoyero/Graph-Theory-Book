"""
Implementaciones de DFS (Depth-First Search)
"""

from typing import List, Set, Callable, Optional
import sys
sys.path.append('..')
from estructuras.grafo import Grafo


def dfs_iterativo(grafo: Grafo, inicio: int) -> List[int]:
    """
    DFS iterativo usando stack explícito
    
    Args:
        grafo: Instancia de Grafo
        inicio: Nodo inicial
    
    Returns:
        Lista de nodos en orden de visita
    
    Complejidad: O(V + E)
    Espacio: O(V)
    """
    visitado = set()
    stack = [inicio]
    orden_visita = []
    
    while stack:
        u = stack.pop()
        if u in visitado:
            continue
        
        visitado.add(u)
        orden_visita.append(u)
        
        # Agregar vecinos en orden reverso para mantener orden lexicográfico
        for arista in reversed(grafo.vecinos(u)):
            v = arista.destino
            if v not in visitado:
                stack.append(v)
    
    return orden_visita


def dfs_recursivo(grafo: Grafo, inicio: int) -> List[int]:
    """
    DFS recursivo
    
    Complejidad: O(V + E)
    Espacio: O(V) para visitados + O(V) para call stack
    """
    visitado = set()
    orden_visita = []
    
    def dfs(u: int):
        visitado.add(u)
        orden_visita.append(u)
        for arista in grafo.vecinos(u):
            v = arista.destino
            if v not in visitado:
                dfs(v)
    
    dfs(inicio)
    return orden_visita


def dfs_con_callback(grafo: Grafo, inicio: int, 
                     pre_visita: Optional[Callable[[int], None]] = None,
                     post_visita: Optional[Callable[[int], None]] = None) -> None:
    """
    DFS genérico con callbacks para pre-orden y post-orden
    
    Útil para implementar diversos algoritmos sobre DFS
    
    Args:
        grafo: Instancia de Grafo
        inicio: Nodo inicial
        pre_visita: Función a ejecutar al visitar un nodo (pre-orden)
        post_visita: Función a ejecutar al terminar de procesar un nodo (post-orden)
    """
    visitado = set()
    
    def dfs(u: int):
        visitado.add(u)
        
        if pre_visita:
            pre_visita(u)
        
        for arista in grafo.vecinos(u):
            v = arista.destino
            if v not in visitado:
                dfs(v)
        
        if post_visita:
            post_visita(u)
    
    dfs(inicio)
