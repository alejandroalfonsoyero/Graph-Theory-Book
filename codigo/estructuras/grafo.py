"""
Implementación de grafos usando lista de adyacencia
"""

from typing import List, Dict, Set, Optional
from dataclasses import dataclass


@dataclass
class Arista:
    """Representa una arista en el grafo"""
    destino: int
    peso: float = 1.0
    
    def __repr__(self):
        return f"({self.destino}, w={self.peso})"


class Grafo:
    """
    Grafo no dirigido usando lista de adyacencia
    
    Complejidad espacial: O(V + E)
    """
    
    def __init__(self, n_vertices: int, dirigido: bool = False):
        """
        Args:
            n_vertices: Número de vértices (0 a n-1)
            dirigido: Si el grafo es dirigido
        """
        self.n = n_vertices
        self.dirigido = dirigido
        self.adyacencia: Dict[int, List[Arista]] = {i: [] for i in range(n_vertices)}
        self._n_aristas = 0
    
    def agregar_arista(self, u: int, v: int, peso: float = 1.0):
        """
        Agrega una arista al grafo
        Complejidad: O(1)
        """
        self.adyacencia[u].append(Arista(v, peso))
        if not self.dirigido and u != v:
            self.adyacencia[v].append(Arista(u, peso))
        self._n_aristas += 1
    
    def vecinos(self, u: int) -> List[Arista]:
        """
        Retorna los vecinos de u
        Complejidad: O(1)
        """
        return self.adyacencia[u]
    
    def tiene_arista(self, u: int, v: int) -> bool:
        """
        Verifica si existe arista u -> v
        Complejidad: O(grado(u))
        """
        return any(arista.destino == v for arista in self.adyacencia[u])
    
    def grado(self, u: int) -> int:
        """Retorna el grado del vértice u"""
        return len(self.adyacencia[u])
    
    @property
    def num_aristas(self) -> int:
        """Número total de aristas"""
        return self._n_aristas
    
    def __repr__(self):
        return f"Grafo(V={self.n}, E={self._n_aristas}, dirigido={self.dirigido})"


class GrafoDirigido(Grafo):
    """Grafo dirigido - alias de Grafo con dirigido=True"""
    
    def __init__(self, n_vertices: int):
        super().__init__(n_vertices, dirigido=True)
    
    def grafo_transpuesto(self) -> 'GrafoDirigido':
        """
        Retorna el grafo transpuesto (invierte todas las aristas)
        Útil para algoritmos como Kosaraju
        Complejidad: O(V + E)
        """
        transpuesto = GrafoDirigido(self.n)
        for u in range(self.n):
            for arista in self.adyacencia[u]:
                transpuesto.agregar_arista(arista.destino, u, arista.peso)
        return transpuesto
