# Recorridos y Búsqueda en Grafos

Este capítulo explora los algoritmos fundamentales para explorar sistemáticamente los vértices y aristas de un grafo: la Búsqueda en Amplitud (BFS) y la Búsqueda en Profundidad (DFS). Ambos son pilares para una amplia gama de problemas y algoritmos más complejos en la teoría de grafos.

---

## 2.1. Introducción a los Recorridos en Grafos

### 2.1.1. ¿Qué es un Recorrido?

Un **recorrido en un grafo** es el proceso de visitar (examinar o procesar) sistemáticamente cada vértice y cada arista de un grafo de una manera estructurada. No se trata simplemente de pasar por los nodos, sino de explorar las relaciones entre ellos para obtener información sobre la estructura del grafo.

### 2.1.2. Aplicaciones Fundamentales

Los algoritmos de recorrido son la base para resolver numerosos problemas, incluyendo:

*   **Verificar Conectividad:** Determinar si un grafo es conexo o fuertemente conexo.
*   **Encontrar Caminos:** Descubrir si existe una ruta entre dos vértices y, en algunos casos, encontrar el camino más corto o más largo.
*   **Detectar Ciclos:** Identificar la presencia de ciclos en un grafo, crucial para DAGs.
*   **Construir Árboles de Expansión:** Generar un subgrafo que es un árbol y conecta todos los vértices.
*   **Determinar la Estructura del Grafo:** Comprender la topología, la densidad o la distribución de componentes.

---

## 2.2. Búsqueda en Amplitud (BFS - Breadth-First Search)

BFS es un algoritmo de recorrido de grafos que explora el grafo "capa por capa", visitando primero todos los vecinos directos de un nodo antes de pasar a los vecinos de esos vecinos.

### 2.2.1. Concepto y Funcionamiento

Imaginen que están tirando una piedra en un estanque. Las ondas se expanden concéntricamente desde el punto de impacto. BFS funciona de manera similar:

1.  Comienza en un **vértice inicial (fuente)**.
2.  Visita a **todos sus vecinos directos** (distancia 1).
3.  Luego visita a **todos los vecinos de esos vecinos** (distancia 2), y así sucesivamente.

![Exploración por Niveles en BFS](images/02_bfs_layers.png){ width=70% }

Para lograr esta expansión por capas, BFS utiliza una **cola (FIFO - First-In, First-Out)**. Los vértices se añaden a la cola y se procesan en el orden en que fueron descubiertos.

### 2.2.2. Algoritmo Detallado

1.  **Inicialización:**
    *   Crear una lista o conjunto `visitados` para mantener un registro de los vértices ya explorados (inicialmente, todos no están visitados).
    *   Crear una `cola` (usando `collections.deque` en Python).
    *   Marcar el `vértice_inicial` como visitado y añadirlo a la `cola`.
    *   Crear una lista `orden_recorrido` para almacenar el orden de visita.

2.  **Exploración (mientras la cola no esté vacía):**
    *   **Desencolar** un vértice `u` de la parte frontal de la `cola`.
    *   Añadir `u` a `orden_recorrido`.
    *   Para **cada vecino `v`** de `u`:
        *   Si `v` **no ha sido visitado**:
            *   Marcar `v` como visitado.
            *   **Encolar** `v` en la parte trasera de la `cola`.

### 2.2.3. Implementación en Python

Para una implementación eficiente de la cola en Python, se recomienda `collections.deque`.

```python
from collections import deque
from typing import List, Tuple

# Asumimos que GrafoListaAdyacencia está definido como en el Capítulo 1
# class GrafoListaAdyacencia:
#     def __init__(self, n_v: int, dirigido: bool = False): ...
#     def agregar_arista(self, u: int, v: int, p: float = 1.0): ...
#     def obtener_vecinos(self, u: int) -> List[Tuple[int, float]]: ...

def bfs(grafo, inicio: int) -> List[int]:
    """
    Realiza un recorrido BFS desde un vértice de inicio dado.
    :param grafo: Una instancia de GrafoListaAdyacencia.
    :param inicio: El vértice de inicio (entero).
    :return: Una lista de vértices en el orden BFS.
    """
    n = grafo.n
    visitados = [False] * n
    cola = deque()
    orden_recorrido = []

    if not (0 <= inicio < n):
        raise ValueError(f"Inicio {inicio} fuera del rango "
                         f"[0, {n-1}]")

    visitados[inicio] = True
    cola.append(inicio)

    while cola:
        u = cola.popleft()
        orden_recorrido.append(u)

        for v, _ in grafo.obtener_vecinos(u):
            if not visitados[v]:
                visitados[v] = True
                cola.append(v)
    return orden_recorrido

# Ejemplo de uso (descomentar para probar si se tiene la clase Grafo)
# g_no_dirigido = GrafoListaAdyacencia(5, dirigido=False)
# g_no_dirigido.agregar_arista(0, 1)
# g_no_dirigido.agregar_arista(0, 2)
# g_no_dirigido.agregar_arista(1, 3)
# g_no_dirigido.agregar_arista(2, 4)
# print(f"BFS desde 0: {bfs(g_no_dirigido, 0)}")
```

### 2.2.4. Análisis de Complejidad

*   **Tiempo:** $O(V + E)$, donde $V$ es el número de vértices y $E$ el número de aristas. Cada vértice se encola y desencola una vez, y para cada vértice, se recorren sus aristas una vez.
*   **Espacio:** $O(V)$ en el peor caso, para almacenar la lista `visitados` y los vértices en la `cola`.

### 2.2.5. Aplicaciones de BFS

*   **Caminos Más Cortos en Grafos No Ponderados:** BFS encuentra el camino más corto (en número de aristas) desde el inicio a todos los demás vértices.
*   **Detección de Componentes Conexas:** Múltiples llamadas a BFS (desde vértices no visitados) identifican las componentes conexas.
*   **Verificación de Bipartición (2-Coloreado):** BFS puede 2-colorear un grafo; si falla, no es bipartito.
*   **Nivelado de Redes (Layering):** Determina la distancia mínima (en aristas) desde un nodo fuente.

---

## 2.3. Búsqueda en Profundidad (DFS - Depth-First Search)

DFS es un algoritmo de recorrido que explora tan profundo como sea posible a lo largo de cada rama antes de retroceder.

### 2.3.1. Concepto y Funcionamiento

Imaginen que están explorando un laberinto con un trozo de cuerda. Siguen un camino hasta el final (o hasta que chocan con una pared o un camino ya explorado), luego retroceden un poco y toman un nuevo giro.

DFS funciona siguiendo un camino desde el nodo de inicio hasta que no puede avanzar más, marcando los nodos visitados en el camino. Una vez que llega a un "callejón sin salida" (un nodo sin vecinos no visitados), retrocede al nodo anterior y explora otra rama, utilizando una **pila (LIFO - Last-In, First-Out)** o la **pila de llamadas de función** en el caso de implementaciones recursivas.

### 2.3.2. Algoritmo Detallado

**Versión Recursiva:**

1.  Marcar el vértice actual `u` como visitado.
2.  Añadir `u` al `orden_recorrido`.
3.  Para **cada vecino `v`** de `u`:
    *   Si `v` **no ha sido visitado**:
        *   Llamar recursivamente a `dfs(grafo, v, visitados, orden_recorrido)`.

**Versión Iterativa (usando una pila explícita):**

1.  **Inicialización:**
    *   Crear una lista o conjunto `visitados`.
    *   Crear una `pila` (lista de Python).
    *   Añadir el `vértice_inicial` a la `pila`.
    *   Crear una lista `orden_recorrido`.

2.  **Exploración (mientras la pila no esté vacía):**
    *   **Desapilar** un vértice `u` de la cima de la `pila`.
    *   Si `u` **no ha sido visitado**:
        *   Marcar `u` como visitado.
        *   Añadir `u` a `orden_recorrido`.
        *   Para **cada vecino `v`** de `u`:
            *   Si `v` **no ha sido visitado**:
                *   **Apilar** `v` en la `pila`. (El orden de apilado puede afectar el `orden_recorrido` final, pero no la validez de la exploración).

### 2.3.3. Implementación en Python

#### Versión Recursiva

Esta es la forma más intuitiva y común de implementar DFS.

```python
from typing import List, Tuple

# Asumimos que GrafoListaAdyacencia está definido como en el Capítulo 1

def dfs_recursivo(grafo, u: int, visitados: List[bool],
                  orden_recorrido: List[int]):
    """
    Función auxiliar recursiva para DFS.
    :param grafo: Instancia de GrafoListaAdyacencia.
    :param u: Vértice actual.
    :param visitados: Lista booleana para rastrear vértices visitados.
    :param orden_recorrido: Lista para acumular el orden de visita.
    """
    visitados[u] = True
    orden_recorrido.append(u)

    for v, _ in grafo.obtener_vecinos(u):
        if not visitados[v]:
            dfs_recursivo(grafo, v, visitados, orden_recorrido)


def dfs(grafo, inicio: int) -> List[int]:
    """
    Realiza un recorrido DFS desde un vértice de inicio dado.
    :param grafo: Instancia de GrafoListaAdyacencia.
    :param inicio: El vértice de inicio (entero).
    :return: Una lista de vértices en el orden DFS.
    """
    n = grafo.n
    visitados = [False] * n
    orden_recorrido = []

    if not (0 <= inicio < n):
        raise ValueError(f"Inicio {inicio} fuera del rango "
                         f"[0, {n-1}]")

    dfs_recursivo(grafo, inicio, visitados, orden_recorrido)
    return orden_recorrido


# Ejemplo de uso (descomentar para probar si se tiene la clase Grafo)
# g_no_dirigido = GrafoListaAdyacencia(5, dirigido=False)
# g_no_dirigido.agregar_arista(0, 1)
# g_no_dirigido.agregar_arista(0, 2)
# g_no_dirigido.agregar_arista(1, 3)
# g_no_dirigido.agregar_arista(2, 4)
# print(f"DFS desde 0: {dfs(g_no_dirigido, 0)}")
# Salida: [0, 1, 3, 2, 4] o similar
```

#### Versión Iterativa

Útil para evitar límites de recursión en Python para grafos muy grandes.

```python
from typing import List, Tuple

# Asumimos que GrafoListaAdyacencia está definido como en el Capítulo 1

def dfs_iterativo(grafo, inicio: int) -> List[int]:
    """
    Realiza un recorrido DFS iterativo desde un vértice de inicio dado.
    :param grafo: Instancia de GrafoListaAdyacencia.
    :param inicio: El vértice de inicio (entero).
    :return: Una lista de vértices en el orden DFS.
    """
    n = grafo.n
    visitados = [False] * n
    pila = []
    orden_recorrido = []

    if not (0 <= inicio < n):
        raise ValueError(f"Inicio {inicio} fuera del rango "
                         f"[0, {n-1}]")

    pila.append(inicio)
    while pila:
        u = pila.pop()  # LIFO
        if not visitados[u]:
            visitados[u] = True
            orden_recorrido.append(u)
            # Empilar vecinos en orden inverso para que el primer vecino
            # en la lista de adyacencia se procese primero (comportamiento DFS)
            # Nota: el orden exacto de los vecinos puede influir en el
            # orden_recorrido final si el grafo permite múltiples caminos.
            for v, _ in reversed(grafo.obtener_vecinos(u)):
                if not visitados[v]:
                    pila.append(v)
    return orden_recorrido
```

### 2.3.4. Análisis de Complejidad

*   **Tiempo:** $O(V + E)$, similar a BFS, ya que cada vértice y arista se visita a lo sumo una vez.
*   **Espacio:**
    *   **Versión Recursiva:** $O(V)$ en el peor caso, limitado por la profundidad de la recursión.
    *   **Versión Iterativa:** $O(V)$ si se controla la duplicidad en la pila; sin embargo, implementaciones sencillas (como la mostrada arriba) pueden crecer hasta $O(E)$ en grafos densos al almacenar múltiples referencias al mismo vértice antes de visitarlo.

### 2.3.5. Aplicaciones de DFS

*   **Detección de Ciclos:** En un grafo dirigido, DFS detecta ciclos al encontrar una arista de retroceso a un vértice ya en la pila de recursión.
*   **Ordenamiento Topológico:** Para DAGs, el orden de finalización de DFS es el inverso de un ordenamiento topológico.
*   **Componentes Fuertemente Conexas (SCCs):** DFS es la base de algoritmos como Tarjan o Kosaraju para SCCs.
*   **Resolución de Laberintos:** DFS explora un camino hasta el final, luego retrocede y prueba otra rama.
*   **Búsqueda de Caminos:** Puede encontrar un camino entre dos vértices, no necesariamente el más corto.
*   **Conectividad:** Determina si un grafo es conexo (si todos los vértices son alcanzables desde un inicio).

---