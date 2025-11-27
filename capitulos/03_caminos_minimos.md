# Caminos Más Cortos: Algoritmos Clásicos

Este capítulo se adentra en uno de los problemas fundamentales de la teoría de grafos: encontrar el camino más corto entre dos vértices. Exploraremos algoritmos clásicos y eficientes como Dijkstra, Bellman-Ford y Floyd-Warshall, entendiendo sus principios, implementaciones en Python y las condiciones bajo las cuales cada uno es más adecuado.

---

## Introducción al Problema del Camino Más Corto

### Definición del Problema

El **problema del camino más corto** consiste en encontrar una ruta entre dos vértices (o entre un vértice y todos los demás) en un grafo, tal que la suma de los pesos de las aristas a lo largo de esa ruta sea mínima.

*   **Camino Más Corto de Fuente Única (Single-Source Shortest Path - SSSP):** Encontrar el camino más corto desde un vértice `s` a todos los demás vértices en el grafo.
*   **Camino Más Corto de Todos los Pares (All-Pairs Shortest Path - APSP):** Encontrar los caminos más cortos entre cada par de vértices en el grafo.

### Tipos de Grafos y Consideraciones

La elección del algoritmo depende crucialmente del tipo de grafo:
*   **Grafos No Ponderados:** BFS puede encontrar los caminos más cortos (en número de aristas).
*   **Grafos Ponderados con Pesos No Negativos:** Algoritmo de Dijkstra.
*   **Grafos Ponderados con Pesos Negativos (sin ciclos negativos):** Algoritmo de Bellman-Ford.
*   **Grafos con Ciclos Negativos:** No existe un camino más corto bien definido (el camino puede ser infinitamente "corto" al recorrer el ciclo). Algunos algoritmos pueden detectarlos.

---

## Algoritmo de Dijkstra

Dijkstra es el algoritmo más conocido para encontrar los caminos más cortos desde un vértice fuente a todos los demás vértices en un grafo con aristas de pesos **no negativos**.

### Concepto y Funcionamiento

Dijkstra funciona como una "expansión de ondas", similar a BFS pero priorizando los vértices con la distancia más pequeña conocida hasta el momento. Mantiene y actualiza las distancias más cortas estimadas a cada vértice.

1.  **Inicialización:**
    *   Asigna una distancia de 0 al vértice fuente y `infinito` a todos los demás.
    *   Mantiene un conjunto de vértices "visitados" (o "finalizados").
    *   Utiliza una **cola de prioridad** (min-heap) para seleccionar eficientemente el vértice no visitado con la distancia más pequeña.
2.  **Iteración:**
    *   Extrae el vértice `u` con la distancia mínima de la cola de prioridad.
    *   Marca `u` como visitado.
    *   Para cada vecino `v` de `u`:
        *   **Relajación:** Si la distancia a `u` más el peso de la arista `(u, v)` es menor que la distancia actual a `v`, actualiza la distancia a `v` y (potencialmente) actualiza su posición en la cola de prioridad.

### Algoritmo Detallado

1.  `dist[v] = infinity` para todos los `v`, `dist[s] = 0`.
2.  `prev[v] = undefined` para todos los `v`.
3.  `min_heap = [(0, s)]` (distancia, vértice).
4.  Mientras `min_heap` no esté vacía:
    a.  `d_u, u = min_heap.pop_min()` (extrae el vértice `u` con la `d_u` más pequeña).
    b.  Si `d_u > dist[u]`, continuar (ya hemos encontrado un camino más corto a `u`).
    c.  Para cada arista `(u, v)` con peso `w`:
        i.  Si `dist[u] + w < dist[v]`:
            *   `dist[v] = dist[u] + w`.
            *   `prev[v] = u`.
            *   `min_heap.push((dist[v], v))`.

### Implementación en Python

Se utiliza `heapq` para la cola de prioridad.

```python
import heapq
from collections import deque
from typing import List, Tuple, Dict, Optional

# Asumimos que GrafoListaAdyacencia está definido como en el Capítulo 1
# y sus vecinos retornan (id_vecino, peso)

def dijkstra(grafo, inicio: int) -> Tuple[List[float], List[Optional[int]]]:
    """
    Calcula los caminos más cortos desde un vértice de inicio a todos
    los demás vértices en un grafo ponderado con pesos no negativos.
    :param grafo: Una instancia de GrafoListaAdyacencia.
    :param inicio: El vértice de inicio (entero).
    :return: Una tupla (distancias, predecesores).
             distancias[v] es la distancia más corta desde inicio a v.
             predecesores[v] es el vértice anterior a v en el camino más corto.
    """
    n = grafo.n
    distancias = [float('inf')] * n
    predecesores: List[Optional[int]] = [None] * n
    distancias[inicio] = 0

    # Cola de prioridad: (distancia_actual, vertice)
    cola_prioridad: List[Tuple[float, int]] = [(0, inicio)]

    while cola_prioridad:
        dist_u, u = heapq.heappop(cola_prioridad)

        # Si ya hemos encontrado un camino más corto a u
        # (por una entrada anterior en la cola de prioridad)
        if dist_u > distancias[u]:
            continue

        for v, peso_uv in grafo.obtener_vecinos(u):
            if distancias[u] + peso_uv < distancias[v]:
                distancias[v] = distancias[u] + peso_uv
                predecesores[v] = u
                heapq.heappush(cola_prioridad, (distancias[v], v))

    return distancias, predecesores

# Función para reconstruir el camino
def reconstruir_camino(predecesores: List[Optional[int]], inicio: int,
                       destino: int) -> List[int]:
    """
    Reconstruye el camino más corto desde el origen hasta el destino
    usando la lista de predecesores.
    :param predecesores: Lista de predecesores generada por Dijkstra/Bellman-Ford.
    :param inicio: El vértice de origen (para validación).
    :param destino: El vértice destino.
    :return: Una lista de vértices que forman el camino más corto.
    """
    camino = deque()
    actual = destino
    while actual is not None:
        camino.appendleft(actual)
        if actual == inicio:
            break
        actual = predecesores[actual]

    # Si el camino está vacío o el primer nodo no es el inicio,
    # significa que no hay conexión
    if not camino or camino[0] != inicio:
        return []

    return list(camino)

# Ejemplo de uso (asumiendo GrafoListaAdyacencia del Cap 1)
# g_pond = GrafoListaAdyacencia(5) # No dirigido por defecto
# g_pond.agregar_arista(0, 1, 10)
# g_pond.agregar_arista(0, 2, 3)
# g_pond.agregar_arista(1, 2, 1)
# g_pond.agregar_arista(1, 3, 2)
# g_pond.agregar_arista(2, 1, 4)
# g_pond.agregar_arista(2, 3, 8)
# g_pond.agregar_arista(2, 4, 2)
# g_pond.agregar_arista(3, 4, 5)

# dists, prevs = dijkstra(g_pond, 0)
# print(f"Distancias desde 0: {dists}") # [0, 4, 3, 6, 5]
# print(f"Camino a 4: {reconstruir_camino(prevs, 0, 4)}") # [0, 2, 4]
```

### Análisis de Complejidad

*   **Tiempo:** $O(E \\log V)$ si se usa una cola de prioridad basada en min-heap binario (como `heapq` de Python). Cada `heappush` y `heappop` cuesta $O(\\log K)$ donde $K$ es el tamaño del heap.
*   **Espacio:** $O(V + E)$ para almacenar distancias, predecesores y la cola de prioridad.

### Limitaciones

*   **No funciona con aristas de pesos negativos.** Si existen, puede dar resultados incorrectos.
*   En el peor caso, puede visitar múltiples veces el mismo nodo si su distancia se actualiza a un valor menor, lo que se gestiona eficientemente con la cola de prioridad.

---

## Algoritmo de Bellman-Ford

Bellman-Ford resuelve el problema del camino más corto de fuente única en grafos que pueden contener aristas con pesos **negativos**, siempre y cuando no haya **ciclos negativos** alcanzables desde la fuente. También puede detectar la presencia de tales ciclos negativos.

### Concepto y Funcionamiento

A diferencia de Dijkstra, Bellman-Ford no es "codicioso". En lugar de elegir siempre el vértice más cercano, relaja sistemáticamente *todas* las aristas del grafo varias veces. Se basa en la observación de que, en un camino más corto de $k$ aristas, la distancia a un vértice solo puede provenir de un vértice alcanzado con $k-1$ aristas.

1.  **Inicialización:** Similar a Dijkstra, asigna distancia 0 a la fuente y `infinito` a los demás.
2.  **Relajación en Fases:**
    *   Itera $V-1$ veces (donde $V$ es el número de vértices).
    *   En cada iteración, examina *todas* las aristas del grafo.
    *   Para cada arista `(u, v)` con peso `w`, intenta relajar la distancia a `v` usando la distancia a `u`.
3.  **Detección de Ciclos Negativos:** Después de $V-1$ iteraciones, si se puede realizar *otra* relajación en cualquier arista en la $V$-ésima iteración, significa que hay un ciclo negativo en el grafo (alcanzable desde la fuente).

### Algoritmo Detallado

1.  `dist[v] = infinity` para todos los `v`, `dist[s] = 0`.
2.  `prev[v] = undefined` para todos los `v`.
3.  Para `i` de 1 a $V-1$:
    a.  Para cada arista `(u, v)` con peso `w` en el grafo:
        i.  Si `dist[u] + w < dist[v]`:
            *   `dist[v] = dist[u] + w`.
            *   `prev[v] = u`.
4.  **Verificación de Ciclos Negativos:**
    a.  Para cada arista `(u, v)` con peso `w` en el grafo:
        i.  Si `dist[u] + w < dist[v]`:
            *   Retorna un error o flag indicando la presencia de un ciclo negativo.
5.  Retorna `dist` y `prev`.

### Implementación en Python

```python
from typing import List, Tuple, Optional, NamedTuple

# Asumimos que GrafoListaAdyacencia está definido como en el Capítulo 1
# Y que ahora tiene un método para obtener todas las aristas si se usa
# una lista de adyacencia (o se podría construir una lista de aristas)

class Edge(NamedTuple):
    u: int
    v: int
    peso: float

def bellman_ford(grafo, inicio: int) \
        -> Tuple[List[float], List[Optional[int]], bool]:
    """
    Calcula los caminos más cortos desde un vértice de inicio a todos
    los demás, y detecta ciclos negativos.
    :param grafo: Una instancia de GrafoListaAdyacencia.
    :param inicio: El vértice de inicio (entero).
    :return: Tupla (distancias, predecesores, hay_ciclo_negativo).
             Si hay_ciclo_negativo es True, distancias y predecesores
             pueden no ser válidos.
    """
    n = grafo.n
    distancias = [float('inf')] * n
    predecesores: List[Optional[int]] = [None] * n
    distancias[inicio] = 0

    # Construir una lista de todas las aristas para iterar fácilmente
    todas_las_aristas: List[Edge] = []
    for u_node in range(n):
        for v_node, peso in grafo.obtener_vecinos(u_node):
            todas_las_aristas.append(Edge(u_node, v_node, peso))

    # Relajación V-1 veces
    for _ in range(n - 1):
        for edge in todas_las_aristas:
            u, v, peso_uv = edge
            if distancias[u] != float('inf') \
                    and distancias[u] + peso_uv < distancias[v]:
                distancias[v] = distancias[u] + peso_uv
                predecesores[v] = u

    # Detectar ciclos negativos (V-ésima relajación)
    hay_ciclo_negativo = False
    for edge in todas_las_aristas:
        u, v, peso_uv = edge
        if distancias[u] != float('inf') \
                and distancias[u] + peso_uv < distancias[v]:
            hay_ciclo_negativo = True
            break # Ciclo negativo encontrado

    return distancias, predecesores, hay_ciclo_negativo

# Ejemplo de uso (asumiendo GrafoListaAdyacencia del Cap 1)
# g_neg = GrafoListaAdyacencia(4, dirigido=True)
# g_neg.agregar_arista(0, 1, 1)
# g_neg.agregar_arista(0, 2, 4)
# g_neg.agregar_arista(1, 2, -3)
# g_neg.agregar_arista(1, 3, 2)
# g_neg.agregar_arista(2, 3, 3)

# dists, prevs, neg_cycle = bellman_ford(g_neg, 0)
# if neg_cycle:
#     print("Ciclo negativo detectado!")
# else:
#     print(f"Distancias desde 0: {dists}") # [0, 1, -2, 1]
#     print(f"Camino a 3: {reconstruir_camino(prevs, 0, 3)}") # [0, 1, 2, 3]

# # Ejemplo con ciclo negativo
# g_neg_cycle = GrafoListaAdyacencia(3, dirigido=True)
# g_neg_cycle.agregar_arista(0, 1, 1)
# g_neg_cycle.agregar_arista(1, 2, -1)
# g_neg_cycle.agregar_arista(2, 0, -1) # Ciclo negativo 0 -> 1 -> 2 -> 0 (-1)
# dists, prevs, neg_cycle = bellman_ford(g_neg_cycle, 0)
# if neg_cycle:
#     print("Ciclo negativo detectado!") # Esto debería imprimirse
```

### Análisis de Complejidad

*   **Tiempo:** $O(V \\cdot E)$, ya que se itera $V-1$ veces y en cada iteración se recorren todas las $E$ aristas.
*   **Espacio:** $O(V + E)$ para almacenar distancias, predecesores y la lista de aristas.

### Ventajas y Desventajas

*   **Ventaja:** Maneja aristas con pesos negativos y detecta ciclos negativos.
*   **Desventaja:** Mucho más lento que Dijkstra para grafos sin pesos negativos.

---

## Algoritmo de Floyd-Warshall

Floyd-Warshall es un algoritmo de programación dinámica que encuentra los caminos más cortos **entre todos los pares de vértices** en un grafo ponderado (con o sin pesos negativos, pero sin ciclos negativos).

### Concepto y Funcionamiento

El algoritmo construye progresivamente una matriz de distancias. La idea central es considerar, en cada paso, un subconjunto de vértices intermedios (`k`) por los cuales los caminos pueden pasar.

1.  **Inicialización:**
    *   Una matriz de distancias $D[i][j]$ se inicializa con el peso directo de la arista $(i, j)$ si existe, 0 si $i=j$, e `infinito` si no hay arista directa.
2.  **Iteración Principal:**
    *   Para cada vértice `k` (de 0 a $V-1$):
        *   Considera a `k` como un posible vértice intermedio en todos los caminos.
        *   Para cada par de vértices `(i, j)`:
            *   `D[i][j] = min(D[i][j], D[i][k] + D[k][j])`. Esta operación intenta mejorar el camino de `i` a `j` pasando por `k`.
3.  **Detección de Ciclos Negativos:** Si después de todas las iteraciones, `D[i][i]` es negativo para cualquier `i`, existe un ciclo negativo en el grafo.

### Algoritmo Detallado

1.  Crear una matriz `dist[V][V]`.
2.  Inicializar `dist[i][j]` como:
    *   `peso(i, j)` si existe arista.
    *   `0` si `i == j`.
    *   `infinito` si no hay arista.
3.  Para `k` de 0 a $V-1$: (vértice intermedio)
    a.  Para `i` de 0 a $V-1$: (vértice de origen)
        i.  Para `j` de 0 a $V-1$: (vértice de destino)
            *   `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`.
4.  **Detección de Ciclos Negativos:** Después de las 3 bucles, si `dist[i][i] < 0` para cualquier `i`, hay un ciclo negativo.

### Implementación en Python

```python
import numpy as np
from typing import List, Tuple

# Asumimos que GrafoMatrizAdyacencia está definido como en el Capítulo 1
# o se puede construir una matriz de adyacencia/distancia inicial.

def floyd_warshall(grafo) -> Tuple[np.ndarray, bool]:
    """
    Calcula los caminos más cortos entre todos los pares de vértices.
    Detecta ciclos negativos.
    :param grafo: Una instancia de GrafoListaAdyacencia o GrafoMatrizAdyacencia.
                  Si es ListaAdyacencia, se construye la matriz inicial aquí.
    :return: Tupla (matriz_distancias, hay_ciclo_negativo).
             matriz_distancias[i][j] es la distancia más corta de i a j.
    """
    n = grafo.n
    # Inicializar matriz de distancias
    # numpy.full para eficiencia, float('inf') para aristas ausentes
    dist = np.full((n, n), float('inf'), dtype=float)

    # Distancia de un vértice a sí mismo es 0
    for i in range(n):
        dist[i][i] = 0

    # Llenar con pesos de aristas directas
    if hasattr(grafo, 'matriz'): # Si es GrafoMatrizAdyacencia
        # Asegurarse de no sobrescribir INF con 0 si es grafo no ponderado
        for i in range(n):
            for j in range(n):
                if grafo.matriz[i][j] != grafo.valor_no_arista:
                    dist[i][j] = grafo.matriz[i][j]
    else: # Si es GrafoListaAdyacencia
        for u in range(n):
            for v, peso in grafo.obtener_vecinos(u):
                dist[u][v] = peso

    # Algoritmo principal de Floyd-Warshall
    for k in range(n): # Vértice intermedio
        for i in range(n): # Vértice de origen
            for j in range(n): # Vértice de destino
                if dist[i][k] != float('inf') \
                        and dist[k][j] != float('inf') \
                        and dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    # Detectar ciclos negativos
    hay_ciclo_negativo = False
    for i in range(n):
        if dist[i][i] < 0:
            hay_ciclo_negativo = True
            break

    return dist, hay_ciclo_negativo

# Ejemplo de uso (asumiendo GrafoListaAdyacencia o Matriz)
# g_apsp = GrafoListaAdyacencia(4, dirigido=True)
# g_apsp.agregar_arista(0, 1, 3)
# g_apsp.agregar_arista(0, 3, 7)
# g_apsp.agregar_arista(1, 0, 8)
# g_apsp.agregar_arista(1, 2, 2)
# g_apsp.agregar_arista(2, 0, 5)
# g_apsp.agregar_arista(2, 3, 1)
# g_apsp.agregar_arista(3, 0, 2)

# dist_matrix, neg_cycle = floyd_warshall(g_apsp)
# if neg_cycle:
#     print("Ciclo negativo detectado!")
# else:
#     print("Matriz de distancias más cortas:")
#     print(dist_matrix)
#     # Expected:
#     # [[0., 3., 5., 6.],
#     #  [8., 0., 2., 3.],
#     #  [5., 8., 0., 1.],
#     #  [2., 5., 7., 0.]]
```

### Análisis de Complejidad

*   **Tiempo:** $O(V^3)$, debido a los tres bucles anidados sobre el número de vértices.
*   **Espacio:** $O(V^2)$ para almacenar la matriz de distancias.

### Ventajas y Desventajas

*   **Ventaja:** Resuelve APSP, puede manejar pesos negativos (sin ciclos negativos) y detecta ciclos negativos. Es conceptualmente simple de entender e implementar.
*   **Desventaja:** Alta complejidad temporal ($O(V^3)$), lo que lo hace impráctico para grafos grandes. No reconstruye los caminos directamente sin una matriz auxiliar de predecesores.

---

## Algoritmo A* (A-Star)

El algoritmo A\* es una extensión de Dijkstra, utilizado para encontrar el camino más corto entre dos vértices específicos en un grafo. Se destaca por su eficiencia en la práctica al utilizar una **función heurística** que guía la búsqueda hacia el destino.

### Concepto y Funcionamiento

A\* combina la "distancia real" recorrida desde el inicio (`g(n)`) con una "distancia estimada" al destino (`h(n)` - la heurística). La función de evaluación es `f(n) = g(n) + h(n)`. Prioriza la exploración de nodos que parecen estar en un camino prometedor hacia el objetivo.

*   **`g(n)`:** Costo del camino desde el nodo inicial hasta el nodo actual `n`.
*   **`h(n)`:** Estimación del costo del camino más barato desde el nodo actual `n` hasta el nodo objetivo. Esta es la función heurística. Para que A\* garantice el camino más corto, `h(n)` debe ser **admisible** (nunca sobreestima el costo real) y preferiblemente **monótona** (consistente).
*   **`f(n)`:** Costo total estimado del camino más barato a través de `n` hasta el objetivo.

### Algoritmo Detallado

Similar a Dijkstra, pero la cola de prioridad ordena por `f(n)`.

1.  `open_set`: Cola de prioridad (min-heap) que contiene los nodos a evaluar, ordenados por `f(n)`.
2.  `g_score[v] = infinity` para todos los `v`, `g_score[inicio] = 0`.
3.  `f_score[v] = infinity` para todos los `v`, `f_score[inicio] = h(inicio, destino)`.
4.  `came_from[v] = undefined` para todos los `v`.
5.  `open_set.push((f_score[inicio], inicio))`.
6.  Mientras `open_set` no esté vacía:
    a.  `current_f, current = open_set.pop_min()`.
    b.  Si `current == destino`, reconstruir camino y retornar.
    c.  Para cada vecino `neighbor` de `current` con peso `cost_to_neighbor`:
        i.  `tentative_g_score = g_score[current] + cost_to_neighbor`.
        ii. Si `tentative_g_score < g_score[neighbor]`:
            *   `came_from[neighbor] = current`.
            *   `g_score[neighbor] = tentative_g_score`.
            *   `f_score[neighbor] = g_score[neighbor] + h(neighbor, destino)`.
            *   `open_set.push((f_score[neighbor], neighbor))`.
7.  Si `open_set` se vacía y no se llegó al destino, no hay camino.

### Implementación en Python

Requiere una función heurística `h(actual, destino)`. Para un mapa, podría ser la distancia euclidiana.

```python
import heapq
from typing import List, Tuple, Dict, Optional, Callable

# Asumimos GrafoListaAdyacencia y la función reconstruir_camino del Cap 1/3

def a_star(grafo, inicio: int, destino: int,
           h_func: Callable[[int, int], float]) \
        -> Tuple[List[float], List[Optional[int]]]:
    """
    Implementación del algoritmo A* para encontrar el camino más corto
    entre un inicio y un destino usando una heurística.
    :param grafo: Una instancia de GrafoListaAdyacencia.
    :param inicio: Vértice de inicio.
    :param destino: Vértice de destino.
    :param h_func: Función heurística h(u, v) que estima la distancia de u a v.
                   Debe ser admisible y consistente para la optimalidad.
    :return: Una tupla (distancias_g, predecesores).
             distancias_g[v] es el costo del camino más corto desde inicio a v.
             predecesores[v] es el vértice anterior a v.
    """
    n = grafo.n
    g_score = [float('inf')] * n  # Costo real desde inicio a n
    g_score[inicio] = 0

    # f_score[n] = g_score[n] + h_func(n, destino)
    f_score = [float('inf')] * n
    f_score[inicio] = h_func(inicio, destino)

    predecesores: List[Optional[int]] = [None] * n

    # open_set: Cola de prioridad (f_score, vertice)
    open_set: List[Tuple[float, int]] = [(f_score[inicio], inicio)]

    while open_set:
        current_f, current = heapq.heappop(open_set)

        if current == destino:
            return g_score, predecesores

        # Si ya hemos encontrado un camino mejor a 'current'
        # (por una entrada anterior en la cola de prioridad)
        if current_f > f_score[current]:
            continue

        for vecino, peso_uv in grafo.obtener_vecinos(current):
            tentative_g_score = g_score[current] + peso_uv

            if tentative_g_score < g_score[vecino]:
                predecesores[vecino] = current
                g_score[vecino] = tentative_g_score
                f_score[vecino] = g_score[vecino] + h_func(vecino, destino)
                heapq.heappush(open_set, (f_score[vecino], vecino))

    return g_score, predecesores # No se encontró camino a destino

# Ejemplo de uso (heurística simple, e.g., distancia euclidiana para un grid)
# Supongamos que los vértices tienen coordenadas (x,y)
# class GrafoConCoords(GrafoListaAdyacencia):
#     def __init__(self, n_v: int, coords: List[Tuple[float, float]], dirigido=False):
#         super().__init__(n_v, dirigido)
#         self.coords = coords

# def distancia_euclidiana(u: int, v: int, grafo_con_coords: GrafoConCoords) -> float:
#     x1, y1 = grafo_con_coords.coords[u]
#     x2, y2 = grafo_con_coords.coords[v]
#     return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

# # Ejemplo de un grafo con 4 nodos y coordenadas
# coords_ej = [(0,0), (1,0), (1,1), (0,1)]
# g_a_star = GrafoConCoords(4, coords_ej, dirigido=False)
# g_a_star.agregar_arista(0, 1, 1)
# g_a_star.agregar_arista(1, 2, 1)
# g_a_star.agregar_arista(2, 3, 1)
# g_a_star.agregar_arista(3, 0, 1) # Es un cuadrado

# # Definir la heurística para este ejemplo
# h_ej = lambda u, v: distancia_euclidiana(u, v, g_a_star)

# dists_g, prevs_a_star = a_star(g_a_star, 0, 2, h_ej)
# print(f"Distancia más corta de 0 a 2 (A*): {dists_g[2]}") # Debería ser 2
# print(f"Camino de 0 a 2 (A*): {reconstruir_camino(prevs_a_star, 0, 2)}") # [0, 1, 2] o [0, 3, 2]
```

### Análisis de Complejidad

*   **Tiempo:** La complejidad de A\* es sensible a la calidad de la heurística. En el peor caso (heurística no informativa), es similar a Dijkstra: $O(E \\log V)$. Con una buena heurística, puede ser significativamente más rápido, acercándose a $O(V)$ en casos ideales.
*   **Espacio:** $O(V + E)$ para almacenar `g_score`, `f_score`, `predecesores` y la cola de prioridad.

### Propiedades y Usos

*   **Optimalidad:** A\* es óptimo (encuentra el camino más corto) si la función heurística `h(n)` es **admisible** (nunca sobreestima el costo real) y el costo de las aristas es no negativo. Si `h(n)` también es **consistente** (monótona), A\* es aún más eficiente.
*   **Completitud:** Si existe un camino, A\* lo encontrará.
*   **Aplicaciones:** Navegación en mapas (Google Maps, Waze), planificación de rutas en videojuegos, robótica y pathfinding en IA.

---
