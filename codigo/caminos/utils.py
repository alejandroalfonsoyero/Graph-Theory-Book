"""
Utilidades para algoritmos de caminos mínimos
"""

from typing import Dict, List, Optional


def reconstruir_camino(padre: Dict[int, Optional[int]], 
                       inicio: int, destino: int) -> Optional[List[int]]:
    """
    Reconstruye el camino desde inicio hasta destino usando diccionario de padres
    
    Args:
        padre: Diccionario {nodo: predecesor}
        inicio: Nodo inicial
        destino: Nodo destino
    
    Returns:
        Lista de nodos en el camino, o None si no alcanzable
    """
    if padre[destino] is None and destino != inicio:
        return None
    
    camino = []
    actual = destino
    while actual is not None:
        camino.append(actual)
        actual = padre[actual]
    
    return camino[::-1]


def distancia_camino(grafo, camino: List[int]) -> float:
    """
    Calcula el costo total de un camino
    
    Args:
        grafo: Grafo ponderado
        camino: Lista de nodos
    
    Returns:
        Suma de pesos de aristas en el camino
    """
    if len(camino) <= 1:
        return 0.0
    
    costo = 0.0
    for i in range(len(camino) - 1):
        u, v = camino[i], camino[i+1]
        # Buscar arista
        encontrada = False
        for arista in grafo.vecinos(u):
            if arista.destino == v:
                costo += arista.peso
                encontrada = True
                break
        
        if not encontrada:
            raise ValueError(f"No existe arista ({u}, {v}) en el grafo")
    
    return costo


def es_camino_valido(grafo, camino: List[int]) -> bool:
    """
    Verifica si una secuencia de nodos forma un camino válido en el grafo
    
    Args:
        grafo: Grafo
        camino: Lista de nodos
    
    Returns:
        True si es un camino válido
    """
    if len(camino) <= 1:
        return True
    
    for i in range(len(camino) - 1):
        u, v = camino[i], camino[i+1]
        existe_arista = any(arista.destino == v for arista in grafo.vecinos(u))
        if not existe_arista:
            return False
    
    return True
