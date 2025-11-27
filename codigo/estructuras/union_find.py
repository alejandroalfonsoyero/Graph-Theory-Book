"""
Union-Find (Disjoint Set Union) con optimizaciones
"""

from typing import List


class UnionFind:
    """
    Estructura Union-Find con path compression y union by rank
    
    Complejidad: O(α(n)) amortizado, donde α es la inversa de Ackermann
    """
    
    def __init__(self, n: int):
        """
        Args:
            n: Número de elementos (0 a n-1)
        """
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
        self.num_components = n
    
    def find(self, x: int) -> int:
        """
        Encuentra el representante del conjunto de x
        Usa path compression para optimización
        Complejidad: O(α(n)) amortizado
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x: int, y: int) -> bool:
        """
        Une los conjuntos que contienen x e y
        Usa union by rank para optimización
        
        Returns:
            True si los elementos estaban en diferentes conjuntos
        
        Complejidad: O(α(n)) amortizado
        """
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x
        
        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        
        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1
        
        self.num_components -= 1
        return True
    
    def connected(self, x: int, y: int) -> bool:
        """Verifica si x e y están en el mismo conjunto"""
        return self.find(x) == self.find(y)
    
    def component_size(self, x: int) -> int:
        """Retorna el tamaño del conjunto que contiene x"""
        return self.size[self.find(x)]
    
    def num_sets(self) -> int:
        """Retorna el número de conjuntos disjuntos"""
        return self.num_components
