"""
Implementación del algoritmo de Bellman-Ford
"""

from typing import Dict, List, Optional, Tuple
import sys
sys.path.append('..')
from estructuras.grafo import Grafo


def bellman_ford(grafo: Grafo, inicio: int) -> Tuple[Dict[int, float], Dict[int, Optional[int]], bool]:
    """
    Algoritmo de Bellman-Ford para caminos más cortos
    Maneja pesos negativos y detecta ciclos negativos
    
    Args:
        grafo: Grafo (puede tener pesos negativos)
        inicio: Nodo inicial
    
    Returns:
        Tupla (distancias, padres, tiene_ciclo_negativo)
        - Si tiene_ciclo_negativo=True, las distancias no son confiables
    
    Complejidad: O(VE)
    """
    distancia = {i: float('inf') for i in range(grafo.n)}
    distancia[inicio] = 0
    padre = {i: None for i in range(grafo.n)}
    
    # Relajar todas las aristas V-1 veces
    for _ in range(grafo.n - 1):
        for u in range(grafo.n):
            for arista in grafo.vecinos(u):
                v = arista.destino
                peso = arista.peso
                
                if distancia[u] != float('inf') and distancia[u] + peso < distancia[v]:
                    distancia[v] = distancia[u] + peso
                    padre[v] = u
    
    # Verificar ciclos negativos
    tiene_ciclo_negativo = False
    for u in range(grafo.n):
        for arista in grafo.vecinos(u):
            v = arista.destino
            peso = arista.peso
            
            if distancia[u] != float('inf') and distancia[u] + peso < distancia[v]:
                tiene_ciclo_negativo = True
                break
        if tiene_ciclo_negativo:
            break
    
    return distancia, padre, tiene_ciclo_negativo


def encontrar_ciclo_negativo(grafo: Grafo, inicio: int) -> Optional[List[int]]:
    """
    Encuentra un ciclo negativo si existe
    
    Args:
        grafo: Grafo dirigido
        inicio: Nodo desde donde empezar la búsqueda
    
    Returns:
        Lista de nodos en el ciclo, o None si no hay ciclo negativo
    
    Complejidad: O(VE)
    """
    distancia = {i: float('inf') for i in range(grafo.n)}
    distancia[inicio] = 0
    padre = {i: None for i in range(grafo.n)}
    
    # Bellman-Ford estándar
    for _ in range(grafo.n - 1):
        for u in range(grafo.n):
            for arista in grafo.vecinos(u):
                v = arista.destino
                peso = arista.peso
                
                if distancia[u] != float('inf') and distancia[u] + peso < distancia[v]:
                    distancia[v] = distancia[u] + peso
                    padre[v] = u
    
    # Encontrar nodo en ciclo negativo
    nodo_ciclo = None
    for u in range(grafo.n):
        for arista in grafo.vecinos(u):
            v = arista.destino
            peso = arista.peso
            
            if distancia[u] != float('inf') and distancia[u] + peso < distancia[v]:
                nodo_ciclo = v
                break
        if nodo_ciclo is not None:
            break
    
    if nodo_ciclo is None:
        return None
    
    # Retroceder V pasos para asegurar estar en el ciclo
    for _ in range(grafo.n):
        nodo_ciclo = padre[nodo_ciclo]
    
    # Recolectar nodos del ciclo
    ciclo = [nodo_ciclo]
    actual = padre[nodo_ciclo]
    while actual != nodo_ciclo:
        ciclo.append(actual)
        actual = padre[actual]
    
    ciclo.reverse()
    return ciclo


def bellman_ford_mejorado(grafo: Grafo, inicio: int) -> Tuple[Dict[int, float], Dict[int, Optional[int]], bool]:
    """
    Versión mejorada que termina early si no hay cambios en una iteración
    
    Complejidad: O(VE) en el peor caso, pero típicamente más rápido
    """
    distancia = {i: float('inf') for i in range(grafo.n)}
    distancia[inicio] = 0
    padre = {i: None for i in range(grafo.n)}
    
    # Relajar hasta que no haya cambios
    for iteracion in range(grafo.n - 1):
        cambios = False
        
        for u in range(grafo.n):
            for arista in grafo.vecinos(u):
                v = arista.destino
                peso = arista.peso
                
                if distancia[u] != float('inf') and distancia[u] + peso < distancia[v]:
                    distancia[v] = distancia[u] + peso
                    padre[v] = u
                    cambios = True
        
        if not cambios:
            # No hubo cambios, terminamos early
            break 
    
    # Verificar ciclos negativos
    tiene_ciclo_negativo = False
    for u in range(grafo.n):
        for arista in grafo.vecinos(u):
            v = arista.destino
            peso = arista.peso
            
            if distancia[u] != float('inf') and distancia[u] + peso < distancia[v]:
                tiene_ciclo_negativo = True
                break
        if tiene_ciclo_negativo:
            break
    
    return distancia, padre, tiene_ciclo_negativo
