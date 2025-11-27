"""
Algoritmos de ordenamiento topológico para DAGs
"""

from collections import deque
from typing import List, Optional
import sys
sys.path.append('..')
from estructuras.grafo import Grafo


def ordenamiento_topologico_kahn(grafo: Grafo) -> Optional[List[int]]:
    """
    Ordenamiento topológico usando el algoritmo de Kahn (basado en BFS)
    
    Args:
        grafo: Instancia de Grafo dirigido
    
    Returns:
        Lista ordenada de vértices, o None si el grafo tiene un ciclo
    
    Complejidad: O(V + E)
    """
    # Calcular grado de entrada
    grado_entrada = [0] * grafo.n
    for u in range(grafo.n):
        for arista in grafo.vecinos(u):
            grado_entrada[arista.destino] += 1
    
    # Cola con nodos sin dependencias (grado entrada = 0)
    queue = deque([i for i in range(grafo.n) if grado_entrada[i] == 0])
    orden = []
    
    while queue:
        u = queue.popleft()
        orden.append(u)
        
        # Remover aristas salientes
        for arista in grafo.vecinos(u):
            v = arista.destino
            grado_entrada[v] -= 1
            if grado_entrada[v] == 0:
                queue.append(v)
    
    # Si no procesamos todos los nodos, hay un ciclo
    return orden if len(orden) == grafo.n else None


def ordenamiento_topologico_dfs(grafo: Grafo) -> Optional[List[int]]:
    """
    Ordenamiento topológico usando DFS
    
    Args:
        grafo: Instancia de Grafo dirigido
    
    Returns:
        Lista ordenada de vértices, o None si el grafo tiene un ciclo
    
    Complejidad: O(V + E)
    """
    color = [0] * grafo.n  # 0: blanco, 1: gris, 2: negro
    orden = []
    tiene_ciclo = False
    
    def dfs(u: int):
        nonlocal tiene_ciclo
        
        color[u] = 1
        
        for arista in grafo.vecinos(u):
            v = arista.destino
            if color[v] == 1:
                # Ciclo detectado
                tiene_ciclo = True
                return
            if color[v] == 0:
                dfs(v)
        
        color[u] = 2
        orden.append(u)
    
    for vertice in range(grafo.n):
        if color[vertice] == 0:
            dfs(vertice)
            if tiene_ciclo:
                return None
    
    return orden[::-1]  # Invertir orden (post-orden inverso)


def todos_ordenamientos_topologicos(grafo: Grafo) -> List[List[int]]:
    """
    Genera todos los ordenamientos topológicos posibles de un DAG
    
    Útil para casos pequeños donde se necesitan todas las soluciones
    
    Args:
        grafo: Instancia de Grafo dirigido acíclico
    
    Returns:
        Lista de todas las ordenaciones topológicas válidas
    
    Complejidad: O(V! × E) en el peor caso
    """
    # Calcular grados de entrada
    grado_entrada = [0] * grafo.n
    for u in range(grafo.n):
        for arista in grafo.vecinos(u):
            grado_entrada[arista.destino] += 1
    
    resultados = []
    orden_actual = []
    visitado = [False] * grafo.n
    
    def backtrack():
        if len(orden_actual) == grafo.n:
            resultados.append(orden_actual[:])
            return
        
        # Probar todos los nodos disponibles (grado entrada = 0)
        for u in range(grafo.n):
            if not visitado[u] and grado_entrada[u] == 0:
                # Marcar como visitado
                visitado[u] = True
                orden_actual.append(u)
                
                # Reducir grados de entrada de vecinos
                for arista in grafo.vecinos(u):
                    grado_entrada[arista.destino] -= 1
                
                backtrack()
                
                # Backtrack
                for arista in grafo.vecinos(u):
                    grado_entrada[arista.destino] += 1
                orden_actual.pop()
                visitado[u] = False
    
    backtrack()
    return resultados


def es_dag(grafo: Grafo) -> bool:
    """
    Verifica si un grafo dirigido es acíclico (DAG)
    
    Complejidad: O(V + E)
    """
    return ordenamiento_topologico_kahn(grafo) is not None
