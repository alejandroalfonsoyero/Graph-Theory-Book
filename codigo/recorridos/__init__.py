"""
Algoritmos de recorrido de grafos (DFS y BFS)

Este módulo contiene implementaciones de los algoritmos fundamentales
de recorrido de grafos y sus aplicaciones principales.
"""

from .dfs import dfs_iterativo, dfs_recursivo, dfs_con_callback
from .bfs import bfs, bfs_distancias, bfs_camino, bfs_multi_source
from .componentes import componentes_conectados, es_conexo, numero_componentes
from .ciclos import (
    tiene_ciclo_no_dirigido, 
    tiene_ciclo_dirigido,
    encontrar_ciclo_dirigido,
    es_aciclico
)
from .topological_sort import (
    ordenamiento_topologico_kahn,
    ordenamiento_topologico_dfs,
    todos_ordenamientos_topologicos,
    es_dag
)

__all__ = [
    # DFS
    'dfs_iterativo',
    'dfs_recursivo',
    'dfs_con_callback',
    # BFS
    'bfs',
    'bfs_distancias',
    'bfs_camino',
    'bfs_multi_source',
    # Componentes
    'componentes_conectados',
    'es_conexo',
    'numero_componentes',
    # Ciclos
    'tiene_ciclo_no_dirigido',
    'tiene_ciclo_dirigido',
    'encontrar_ciclo_dirigido',
    'es_aciclico',
    # Topological Sort
    'ordenamiento_topologico_kahn',
    'ordenamiento_topologico_dfs',
    'todos_ordenamientos_topologicos',
    'es_dag',
]
