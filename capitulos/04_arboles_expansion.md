# Árboles de Expansión Mínima (MST)

Este capítulo introduce el concepto fundamental de los Árboles de Expansión Mínima (MST) y explora dos de los algoritmos más conocidos para encontrarlos: el algoritmo de Prim y el algoritmo de Kruskal. Entenderemos sus principios, implementaciones en Python y cuándo aplicar cada uno.

---

## Introducción a los Árboles de Expansión Mínima

### ¿Qué es un Árbol de Expansión?

Un **árbol de expansión (spanning tree)** de un grafo conexo no dirigido es un subgrafo que es un árbol (acíclico y conexo) y que incluye a todos los vértices del grafo original. Si el grafo no es conexo, no tiene un único árbol de expansión, sino un *bosque de expansión* (spanning forest).

*   **Propiedades de un Árbol de Expansión:**
    *   Contiene todos los $V$ vértices del grafo original.
    *   Es conexo.
    *   Es acíclico.
    *   Contiene exactamente $V-1$ aristas.

### El Problema del Árbol de Expansión Mínima (MST)

En un grafo conexo, no dirigido y ponderado, un **Árbol de Expansión Mínima (MST - Minimum Spanning Tree)** es un árbol de expansión cuyas aristas suman el menor peso posible.

![Ejemplo de MST (aristas rojas)](images/04_mst.png){ width=50% }

*   **Aplicaciones:** Los MST son fundamentales en problemas de diseño de redes, como:
    *   Diseño de redes de comunicación, eléctricas o de tuberías para minimizar costos.
    *   Clustering de datos (agrupamiento).
    *   Circuitos impresos.

### Propiedades Clave del MST

Dos propiedades son cruciales para el funcionamiento de los algoritmos de MST:

1.  **Propiedad del Corte (Cut Property):** Para cualquier corte (partición de los vértices del grafo en dos conjuntos no vacíos), si una arista tiene un peso estrictamente menor que cualquier otra arista que cruza el corte, entonces esa arista debe pertenecer a *todo* MST del grafo. Si hay varias aristas con el mismo peso mínimo, al menos una de ellas pertenece a un MST.
2.  **Propiedad del Ciclo (Cycle Property):** Si una arista tiene un peso estrictamente mayor que cualquier otra arista en un ciclo, entonces esa arista no puede pertenecer a *ningún* MST del grafo. Si hay varias aristas con el mismo peso máximo, al menos una de ellas no pertenece a ningún MST.

---

## Algoritmo de Prim

El algoritmo de Prim es un algoritmo "codicioso" que construye un MST de forma incremental. Comienza desde un vértice arbitrario y va añadiendo la arista de menor peso que conecta el árbol de expansión parcial con un vértice que aún no está en él.

### Concepto y Funcionamiento

Prim se enfoca en hacer crecer un solo componente conexo (el MST parcial) hasta que abarque todos los vértices.

1.  **Inicialización:**
    *   Elija un vértice de inicio arbitrario y añádalo al MST.
    *   Mantenga un registro de la arista de menor peso que conecta cada vértice fuera del MST al MST.
    *   Utilice una **cola de prioridad** (min-heap) para almacenar las aristas candidatas que conectan un vértice fuera del MST al MST parcial.
2.  **Iteración:**
    *   Extraiga de la cola de prioridad la arista de menor peso `(u, v)` donde `u` está en el MST parcial y `v` no.
    *   Añada `v` y la arista `(u, v)` al MST.
    *   Para cada vecino `x` de `v` que aún no está en el MST, actualice su arista candidata si se ha encontrado un camino más corto a través de `v`.

### Algoritmo Detallado

1.  `min_cost[v] = infinity` para todos los `v`, excepto `min_cost[s] = 0` (s es el vértice de inicio).
2.  `parent[v] = None` para todos los `v`.
3.  `in_mst[v] = False` para todos los `v`.
4.  `min_heap = [(0, s)]` (costo, vértice).
5.  `mst_edges = []`
6.  Mientras `min_heap` no esté vacía Y `len(mst_edges) < V-1`:
    a.  `cost_u, u = heapq.heappop(min_heap)`.
    b.  Si `in_mst[u]`, continuar (ya procesado).
    c.  `in_mst[u] = True`.
    d.  Si `parent[u]` no es `None`, añadir `(parent[u], u, cost_u)` a `mst_edges`.
    e.  Para cada arista `(u, v)` con peso `w`:
        i.  Si `not in_mst[v]` Y `w < min_cost[v]` (o `cost_u + w < min_cost[v]` si se usa variante de Dijkstra):
            *   `min_cost[v] = w` (o `cost_u + w`).
            *   `parent[v] = u`.
            *   `heapq.heappush(min_heap, (min_cost[v], v))`.

### Implementación en Python

Se utiliza `heapq` para la cola de prioridad.

```python
import heapq
from typing import List, Tuple, Optional, NamedTuple

# Asumimos que GrafoListaAdyacencia está definido como en el Capítulo 1
# y sus vecinos retornan (id_vecino, peso)

class MSTEdge(NamedTuple):
    u: int
    v: int
    peso: float

def prim(grafo, inicio: int = 0) -> Tuple[List[MSTEdge], float]:
    """
    Calcula el Árbol de Expansión Mínima (MST) usando el algoritmo de Prim.
    :param grafo: Una instancia de GrafoListaAdyacencia.
                  Debe ser no dirigido.
    :param inicio: El vértice de inicio (entero).
    :return: Una tupla (mst_aristas, costo_total_mst).
             mst_aristas es una lista de objetos MSTEdge.
             costo_total_mst es la suma de los pesos de las aristas del MST.
    """
    n = grafo.n
    min_costo_a_mst = [float('inf')] * n
    vertice_padre = [None] * n
    en_mst = [False] * n

    # Cola de prioridad: (costo_arista_al_mst, vertice)
    # Inicialmente, solo el vértice de inicio tiene costo 0 para entrar al MST.
    pq: List[Tuple[float, int]] = [(0, inicio)]
    min_costo_a_mst[inicio] = 0

    mst_aristas: List[MSTEdge] = []
    costo_total_mst = 0.0

    while pq and len(mst_aristas) < n - 1:
        costo_u, u = heapq.heappop(pq)

        if en_mst[u]:
            continue

        en_mst[u] = True
        costo_total_mst += costo_u
        if vertice_padre[u] is not None:
            # Añadir la arista que conectó `u` al MST
            mst_aristas.append(
                MSTEdge(vertice_padre[u], u, costo_u))

        # Relajar aristas de `u` a sus vecinos
        for v, peso_uv in grafo.obtener_vecinos(u):
            if not en_mst[v] and peso_uv < min_costo_a_mst[v]:
                min_costo_a_mst[v] = peso_uv
                vertice_padre[v] = u
                heapq.heappush(pq, (peso_uv, v))
    
    # Verificar si el grafo es conexo (si se encontró un MST completo)
    if len(mst_aristas) == n - 1:
        return mst_aristas, costo_total_mst
    else:
        # No se pudo formar un MST que cubra todos los vértices
        # (grafo no conexo o error)
        return [], float('inf')


# Ejemplo de uso (asumiendo GrafoListaAdyacencia del Cap 1, no dirigido)
# g_prim = GrafoListaAdyacencia(5, dirigido=False)
# g_prim.agregar_arista(0, 1, 2)
# g_prim.agregar_arista(0, 3, 6)
# g_prim.agregar_arista(1, 2, 3)
# g_prim.agregar_arista(1, 3, 8)
# g_prim.agregar_arista(1, 4, 5)
# g_prim.agregar_arista(2, 4, 7)
# g_prim.agregar_arista(3, 4, 9)

# mst_aristas, costo = prim(g_prim, 0)
# print(f"Aristas del MST de Prim: {mst_aristas}")
# # Expected: [(0, 1, 2), (1, 2, 3), (1, 4, 5), (0, 3, 6)]
# print(f"Costo total del MST: {costo}") # Expected: 16.0
```

### Análisis de Complejidad

*   **Tiempo:** $O(E \\log V)$ si se usa una cola de prioridad basada en min-heap binario (como `heapq` de Python). Cada vez que se añade un vértice al MST, se pueden añadir hasta `grado(u)` aristas a la cola de prioridad. Las operaciones de heap cuestan $O(\\log E)$ o $O(\\log V)$ si las aristas duplicadas se gestionan con cuidado.
*   **Espacio:** $O(V + E)$ para la cola de prioridad, las listas de costos y padres.

### Limitaciones

*   Requiere un grafo conexo. Si el grafo no es conexo, Prim encontrará un MST para la componente conexa del vértice de inicio.
*   Funciona solo para grafos no dirigidos.

---

## Algoritmo de Kruskal

El algoritmo de Kruskal es otro algoritmo "codicioso" para encontrar el MST. A diferencia de Prim, que expande un solo componente, Kruskal construye el MST añadiendo las aristas de menor peso en todo el grafo, siempre y cuando no formen un ciclo con las aristas ya elegidas.

### Concepto y Funcionamiento

Kruskal se basa en la propiedad del ciclo: una arista solo se añade si no forma un ciclo. Para verificar rápidamente si añadir una arista formaría un ciclo, se utiliza una estructura de datos llamada **Union-Find (Disjoint Set Union - DSU)**.

1.  **Inicialización:**
    *   Coloque cada vértice en su propio conjunto disjunto.
    *   Ordene todas las aristas del grafo en orden ascendente de peso.
    *   Inicialice una lista vacía para las aristas del MST.
2.  **Iteración:**
    *   Para cada arista `(u, v)` (con peso `w`) en el orden ascendente:
        *   Si `u` y `v` pertenecen a conjuntos disjuntos diferentes (es decir, añadir la arista no forma un ciclo):
            *   Añada la arista `(u, v)` al MST.
            *   Una los conjuntos que contienen a `u` y `v` (operación `union`).
    *   Deténgase cuando el MST tenga $V-1$ aristas o cuando se hayan considerado todas las aristas.

### La Estructura de Datos Union-Find (DSU)

Union-Find es una estructura de datos que gestiona un conjunto de elementos particionados en un número de conjuntos disjuntos. Ofrece dos operaciones clave:

*   **`find(i)`:** Determina a qué conjunto pertenece el elemento `i` (normalmente retorna el representante del conjunto).
*   **`union(i, j)`:** Une los dos conjuntos que contienen a `i` y `j` en un solo conjunto.

Para optimizar DSU, se utilizan dos técnicas:

1.  **Compresión de Caminos (Path Compression):** Durante la operación `find`, hace que cada nodo en el camino al representante apunte directamente al representante.
2.  **Unión por Rango/Tamaño (Union by Rank/Size):** Al unir dos conjuntos, adjunta el árbol más pequeño bajo la raíz del árbol más grande, manteniendo los árboles planos y reduciendo la altura.

#### Implementación de Union-Find en Python

```python
class UnionFind:
    """
    Implementación de la estructura de datos Union-Find (Disjoint Set Union - DSU)
    con compresión de caminos y unión por tamaño/rango.
    """
    def __init__(self, n_elementos: int):
        self.padre = list(range(n_elementos))
        self.tamano = [1] * n_elementos # Usamos tamaño para la unión por tamaño

    def find(self, i: int) -> int:
        """
        Encuentra el representante (raíz) del conjunto al que pertenece i.
        Realiza compresión de caminos.
        """
        if self.padre[i] == i:
            return i
        self.padre[i] = self.find(self.padre[i])
        return self.padre[i]

    def union(self, i: int, j: int) -> bool:
        """
        Une los conjuntos que contienen a i y j.
        Retorna True si los conjuntos eran diferentes y se unieron, False si ya
        estaban en el mismo conjunto.
        Realiza unión por tamaño.
        """
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            # Unir el árbol más pequeño bajo la raíz del más grande
            if self.tamano[root_i] < self.tamano[root_j]:
                self.padre[root_i] = root_j
                self.tamano[root_j] += self.tamano[root_i]
            else:
                self.padre[root_j] = root_i
                self.tamano[root_i] += self.tamano[root_j]
            return True
        return False

# Ejemplo de uso UnionFind
# uf = UnionFind(5)
# uf.union(0, 1) # {0,1}, {2}, {3}, {4}
# uf.union(2, 3) # {0,1}, {2,3}, {4}
# uf.union(0, 2) # {0,1,2,3}, {4}
# print(uf.find(1) == uf.find(3)) # True
# print(uf.find(1) == uf.find(4)) # False
```

### Implementación de Kruskal en Python

```python
from typing import List, Tuple, NamedTuple

# Asumimos que GrafoListaAdyacencia está definido como en el Capítulo 1
# y que la clase UnionFind está definida arriba.

# Usaremos la misma NamedTuple MSTEdge para las aristas del MST

def kruskal(grafo) -> Tuple[List[MSTEdge], float]:
    """
    Calcula el Árbol de Expansión Mínima (MST) usando el algoritmo de Kruskal.
    :param grafo: Una instancia de GrafoListaAdyacencia.
                  Debe ser no dirigido (el algoritmo solo añade aristas una vez).
    :return: Una tupla (mst_aristas, costo_total_mst).
             mst_aristas es una lista de objetos MSTEdge.
             costo_total_mst es la suma de los pesos de las aristas del MST.
    """
    n = grafo.n
    todas_las_aristas: List[MSTEdge] = []
    
    # Recopilar todas las aristas del grafo.
    # Para grafos no dirigidos, NetworkX retorna (u,v) y (v,u) si es bidireccional,
    # pero aquí nuestra GrafoListaAdyacencia solo guarda (u,v).
    # Debemos asegurarnos de no añadir aristas duplicadas (u,v) y (v,u)
    # en la lista de todas_las_aristas para Kruskal.
    # Una forma es usar un set para evitar duplicados o solo iterar en una dirección.
    # Aquí asumimos que grafo.obtener_vecinos(u) para u < v es suficiente si
    # el grafo es conceptualmente no dirigido.
    aristas_procesadas = set() # Para evitar añadir (u,v) y (v,u)
    for u in range(n):
        for v, peso in grafo.obtener_vecinos(u):
            if u < v: # Añadir solo una vez por arista no dirigida
                todas_las_aristas.append(MSTEdge(u, v, peso))

    # 1. Ordenar todas las aristas por peso ascendente
    todas_las_aristas.sort(key=lambda edge: edge.peso)

    # 2. Inicializar la estructura Union-Find
    uf = UnionFind(n)

    mst_aristas: List[MSTEdge] = []
    costo_total_mst = 0.0

    # 3. Iterar sobre las aristas ordenadas
    for edge in todas_las_aristas:
        u, v, peso = edge
        if uf.union(u, v): # Si u y v no están en el mismo componente y se unen
            mst_aristas.append(edge)
            costo_total_mst += peso
            if len(mst_aristas) == n - 1:
                break # MST completo

    # Verificar si el grafo es conexo (si se encontró un MST completo)
    if len(mst_aristas) == n - 1:
        return mst_aristas, costo_total_mst
    else:
        # No se pudo formar un MST que cubra todos los vértices
        # (grafo no conexo o error)
        return [], float('inf')

# Ejemplo de uso (asumiendo GrafoListaAdyacencia del Cap 1, no dirigido)
# g_kruskal = GrafoListaAdyacencia(5, dirigido=False)
# g_kruskal.agregar_arista(0, 1, 2)
# g_kruskal.agregar_arista(0, 3, 6)
# g_kruskal.agregar_arista(1, 2, 3)
# g_kruskal.agregar_arista(1, 3, 8)
# g_kruskal.agregar_arista(1, 4, 5)
# g_kruskal.agregar_arista(2, 4, 7)
# g_kruskal.agregar_arista(3, 4, 9)

# mst_aristas, costo = kruskal(g_kruskal)
# print(f"Aristas del MST de Kruskal: {mst_aristas}")
# # Expected: [(0, 1, 2), (1, 2, 3), (1, 4, 5), (0, 3, 6)] (orden puede variar ligeramente)
# print(f"Costo total del MST: {costo}") # Expected: 16.0
```

### Análisis de Complejidad

*   **Tiempo:** $O(E \\log E)$ o $O(E \\log V)$.
    *   $O(E \\log E)$ para ordenar las aristas.
    *   $O(E \\alpha(V))$ para las operaciones de Union-Find, donde $\\alpha$ es la función inversa de Ackermann, extremadamente lenta pero en la práctica casi constante.
    *   Dominado por la ordenación de las aristas. Dado que $E \\le V^2$, $E \\log E$ es a lo sumo $V^2 \\log(V^2) = 2V^2 \\log V$, pero típicamente $E \\log E$ es más cercano a $E \\log V$.
*   **Espacio:** $O(V + E)$ para almacenar la estructura Union-Find y las aristas.

### Comparativa Prim vs. Kruskal

| Característica         | Algoritmo de Prim        | Algoritmo de Kruskal       |
| :--------------------- | :----------------------- | :------------------------- |
| **Enfoque**            | Crece un componente único | Une componentes pequeños    |
| **Estructura Clave**   | Cola de prioridad (Min-Heap) | Union-Find (DSU)          |
| **Grafo Ideal**        | Densos ($E \approx V^2$) | Dispersos ($E \approx V$) |
| **Complejidad Temporal** | $O(E \log V)$           | $O(E \log E)$             |
| **Requiere Conexión**  | Sí (para un MST completo) | Sí (para un MST completo) |
| **Fácil Detección de Ciclos** | Implícito (crece un árbol) | Explícito (con Union-Find) |

---