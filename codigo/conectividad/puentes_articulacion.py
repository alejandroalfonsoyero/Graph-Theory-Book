"""
Algoritmos para encontrar puentes y puntos de articulación en grafos.
"""

from typing import Tuple, Set, List
from ..estructuras.grafo import Grafo

def encontrar_puntos_criticos(grafo: Grafo) -> Tuple[Set[int], List[Tuple[int, int]]]:
    """
    Encuentra puntos de articulación y puentes en un grafo no dirigido
    usando el algoritmo de Tarjan (basado en DFS).

    Args:
        grafo: Grafo no dirigido

    Returns:
        Tupla (puntos_articulacion, puentes)
        - puntos_articulacion: Conjunto de IDs de vértices que son puntos de articulación.
        - puentes: Lista de tuplas (u, v) representando aristas puente.

    Complejidad:
        Tiempo: O(V + E)
        Espacio: O(V)
    """
    n = grafo.n
    discovery = [-1] * n
    low = [-1] * n
    tiempo = 0
    
    puntos_articulacion = set()
    puentes = []
    
    def dfs(u: int, padre: int = -1):
        nonlocal tiempo
        discovery[u] = low[u] = tiempo
        tiempo += 1
        hijos = 0
        
        for arista in grafo.vecinos(u):
            v = arista.destino
            if v == padre:
                continue
            
            if discovery[v] != -1:
                # Back edge: v ya fue visitado y no es el padre inmediato.
                # Esto significa que hay un camino alternativo hacia un ancestro.
                low[u] = min(low[u], discovery[v])
            else:
                # Tree edge: v no ha sido visitado.
                hijos += 1
                dfs(v, u)
                
                # Al regresar de la recursión, actualizamos low[u] con lo que
                # v haya podido alcanzar.
                low[u] = min(low[u], low[v])
                
                # Chequeo de Puente
                # Si low[v] > discovery[u], significa que v (y su subárbol)
                # no tienen ninguna back-edge que suba a u o más arriba.
                if low[v] > discovery[u]:
                    puentes.append((u, v))
                
                # Chequeo de Punto de Articulación
                # Si low[v] >= discovery[u], significa que v no tiene back-edge
                # que suba estrictamente por encima de u. Por tanto, u es necesario
                # para conectar v con el resto del grafo (ancestros de u).
                if padre != -1 and low[v] >= discovery[u]:
                    puntos_articulacion.add(u)
        
        # Caso especial para la raíz del árbol DFS
        # La raíz es punto de articulación si tiene más de un hijo en el árbol DFS.
        # (Si tiene 1 hijo, quitar la raíz no desconecta nada más que la raíz misma
        # del resto, pero el resto sigue conectado entre sí).
        if padre == -1 and hijos > 1:
            puntos_articulacion.add(u)

    for i in range(n):
        if discovery[i] == -1:
            dfs(i)
            
    return puntos_articulacion, puentes
