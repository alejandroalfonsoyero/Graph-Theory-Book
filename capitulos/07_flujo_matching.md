# Flujo Máximo y Matching

El problema del flujo máximo es uno de los pilares de la optimización combinatoria.
Se ocupa de encontrar la mayor cantidad de "flujo" (agua, tráfico, datos) que se
puede enviar a través de una red con capacidades limitadas en sus enlaces. Este
capítulo explora los algoritmos clásicos para resolverlo y cómo estos se aplican
sorprendentemente a problemas de emparejamiento (matching).

---

## Redes de Flujo

Una **red de flujo** es un grafo dirigido $G = (V, E)$ donde cada arista $(u, v)$
tiene una capacidad no negativa $c(u, v) \ge 0$. Distinguimos dos vértices
especiales:
*   **Fuente ($s$):** Un vértice sin aristas entrantes (idealmente), donde se
    origina el flujo.
*   **Sumidero ($t$):** Un vértice sin aristas salientes (idealmente), donde
    termina el flujo.

![Red de Flujo con Capacidades](images/07_flow_network.png){ width=70% }

### Propiedades del Flujo

Un **flujo** es una función $f(u, v)$ que asigna un valor a cada arista,
cumpliendo dos condiciones:

1.  **Restricción de Capacidad:** Para toda arista, el flujo no puede superar la
    capacidad: $0 \le f(u, v) \le c(u, v)$.
2.  **Conservación del Flujo:** Para todo vértice $u$ (excepto la fuente y el
    sumidero), el flujo total que entra debe ser igual al flujo total que sale:
    $\sum_{v \in V} f(v, u) = \sum_{v \in V} f(u, v)$.

El valor del flujo total de la red es la cantidad total que sale de la fuente
hacia el sumidero. El objetivo es maximizar este valor.

---

## Algoritmo de Ford-Fulkerson

El método de Ford-Fulkerson es un enfoque general para resolver el problema del
flujo máximo. Se basa en la idea de encontrar caminos por donde todavía se puede
enviar más flujo y saturarlos progresivamente.

### Conceptos Clave

*   **Red Residual ($G_f$):** Un grafo que indica cuánto flujo adicional se puede
    enviar. Si por una arista $(u, v)$ pasa un flujo $f(u, v)$ y tiene capacidad
    $c(u, v)$:
    *   La **capacidad residual** directa es $c_f(u, v) = c(u, v) - f(u, v)$.
    *   Aparece una **arista de retroceso** $(v, u)$ con capacidad residual
        $f(u, v)$, que representa la posibilidad de "cancelar" o devolver flujo.
*   **Camino Aumentante:** Un camino simple desde la fuente $s$ al sumidero $t$
    en la red residual $G_f$, donde todas las aristas tienen capacidad residual
    positiva.

### Algoritmo Detallado

1.  Inicializar el flujo en todas las aristas a 0.
2.  Mientras exista un camino aumentante $p$ en la red residual $G_f$:
    *   Encontrar la capacidad residual mínima $b$ ("cuello de botella") a lo
        largo del camino $p$.
    *   Aumentar el flujo a lo largo de $p$ en $b$:
        *   Para cada arista $(u, v)$ en $p$:
            *   Incrementar $f(u, v)$ en $b$.
            *   Decrementar $f(v, u)$ en $b$ (en la lógica de la red residual).
3.  Retornar el flujo total acumulado.

---

## Algoritmo de Edmonds-Karp

El algoritmo de Edmonds-Karp es una implementación específica del método de
Ford-Fulkerson. La diferencia clave es cómo encuentra el camino aumentante:
Edmonds-Karp utiliza **BFS (Búsqueda en Amplitud)** para encontrar siempre el
camino aumentante con el **menor número de aristas**.

Esta simple elección garantiza que el algoritmo termine y tenga una complejidad
temporal polinomial de $O(V E^2)$, a diferencia de Ford-Fulkerson genérico (usando DFS),
que puede depender del valor del flujo máximo y ser muy lento con capacidades
grandes irracionales.

### Implementación en Python

```python
from collections import deque

class GrafoFlujo:
    """
    Grafo dirigido para problemas de flujo máximo.
    Soporta capacidades en las aristas.
    """
    def __init__(self, n_vertices: int):
        self.n = n_vertices
        # Matriz de capacidades para acceso rápido.
        # graph[u][v] almacena la capacidad residual de u a v.
        self.capacity = [[0] * n_vertices for _ in range(n_vertices)]
        # Lista de adyacencia para iterar eficientemente sobre vecinos
        self.graph = {i: [] for i in range(n_vertices)}

    def agregar_arista(self, u: int, v: int, capacidad: int):
        # Arista directa con capacidad
        self.graph[u].append(v)
        self.graph[v].append(u) # Arista inversa para el grafo residual
        self.capacity[u][v] = capacidad

    def bfs(self, s: int, t: int, parent: list) -> bool:
        """
        Busca un camino aumentante usando BFS.
        Llena el array 'parent' para reconstruir el camino.
        """
        visited = [False] * self.n
        queue = deque([s])
        visited[s] = True
        parent[s] = -1

        while queue:
            u = queue.popleft()

            for v in self.graph[u]:
                # Si no visitado y hay capacidad residual
                if not visited[v] and self.capacity[u][v] > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == t:
                        return True
        return False

    def edmonds_karp(self, source: int, sink: int) -> int:
        """
        Calcula el flujo máximo desde source a sink.
        """
        parent = [-1] * self.n
        max_flow = 0

        # Mientras exista un camino aumentante en el grafo residual
        while self.bfs(source, sink, parent):
            # Encontrar el cuello de botella (flujo mínimo) en el camino
            path_flow = float('inf')
            v = sink
            while v != source:
                u = parent[v]
                path_flow = min(path_flow, self.capacity[u][v])
                v = u

            # Actualizar capacidades residuales
            max_flow += path_flow
            v = sink
            while v != source:
                u = parent[v]
                self.capacity[u][v] -= path_flow # Reducir capacidad directa
                self.capacity[v][u] += path_flow # Aumentar capacidad inversa
                v = u

        return max_flow

# Ejemplo de uso
# g_flujo = GrafoFlujo(6)
# g_flujo.agregar_arista(0, 1, 16)
# g_flujo.agregar_arista(0, 2, 13)
# g_flujo.agregar_arista(1, 2, 10)
# g_flujo.agregar_arista(1, 3, 12)
# g_flujo.agregar_arista(2, 1, 4)
# g_flujo.agregar_arista(2, 4, 14)
# g_flujo.agregar_arista(3, 2, 9)
# g_flujo.agregar_arista(3, 5, 20)
# g_flujo.agregar_arista(4, 3, 7)
# g_flujo.agregar_arista(4, 5, 4)

# print(f"Flujo Máximo: {g_flujo.edmonds_karp(0, 5)}") # Salida esperada: 23
```

---

## Matching en Grafos Bipartitos

El problema del emparejamiento máximo (Maximum Bipartite Matching) consiste en
encontrar el mayor número de aristas en un grafo bipartito tal que ningún par de
aristas comparta un vértice común.

### Aplicaciones

*   **Asignación de Tareas:** Asignar empleados a tareas, donde cada empleado
    puede hacer ciertas tareas.
*   **Residencia Médica:** Asignar estudiantes a hospitales.

### Reducción a Flujo Máximo

Podemos resolver este problema modelándolo como una red de flujo:

1.  Crear un **super-origen $s$** y un **super-sumidero $t$**.
2.  Conectar $s$ a todos los nodos del conjunto izquierdo del grafo bipartito con
    aristas de capacidad 1.
3.  Mantener las aristas del grafo bipartito (de izquierda a derecha) como
    aristas dirigidas con capacidad 1 (o infinita).
4.  Conectar todos los nodos del conjunto derecho a $t$ con aristas de capacidad
    1.
5.  El flujo máximo en esta red es igual al tamaño del matching máximo.

### Teorema de Flujo Máximo - Corte Mínimo

Este teorema fundamental establece que el valor del flujo máximo de una red es
igual a la capacidad del corte mínimo. Un **corte** es una partición de los
vértices en dos conjuntos disjuntos, uno que contiene la fuente y otro el
sumidero. La capacidad del corte es la suma de las capacidades de las aristas
que van del conjunto de la fuente al del sumidero.

Esto tiene aplicaciones directas en visión por computadora (segmentación de
imágenes) y minería de datos.

### Implementación de Matching Bipartito (vía Flujo)

Usando la clase `GrafoFlujo` anterior:

```python
def matching_bipartito(n_izq: int, n_der: int,
                       aristas: list[tuple[int, int]]) -> int:
    """
    Calcula el matching máximo en un grafo bipartito.
    :param n_izq: Número de nodos en el conjunto izquierdo.
    :param n_der: Número de nodos en el conjunto derecho.
    :param aristas: Lista de tuplas (u, v) donde u está en izq y v en der.
                    u va de 0 a n_izq-1, v va de 0 a n_der-1.
    """
    # Total nodos = fuente + n_izq + n_der + sumidero
    # IDs: fuente=0, izq=1..n_izq, der=n_izq+1..n_izq+n_der, sumidero=total-1
    total_nodes = 1 + n_izq + n_der + 1
    source = 0
    sink = total_nodes - 1
    
    g = GrafoFlujo(total_nodes)

    # Conectar fuente a conjunto izquierdo
    for i in range(n_izq):
        # Nodos izq mapeados a 1 ... n_izq
        g.agregar_arista(source, i + 1, 1)

    # Conectar conjunto derecho a sumidero
    for j in range(n_der):
        # Nodos der mapeados a n_izq + 1 ... n_izq + n_der
        node_der_id = n_izq + 1 + j
        g.agregar_arista(node_der_id, sink, 1)

    # Conectar aristas del grafo bipartito
    for u, v in aristas:
        u_id = u + 1
        v_id = n_izq + 1 + v
        g.agregar_arista(u_id, v_id, 1)

    return g.edmonds_karp(source, sink)

# Ejemplo de Matching
# 3 candidatos (0,1,2), 3 trabajos (0,1,2)
# Candidato 0 puede hacer trabajo 1
# Candidato 1 puede hacer trabajo 0 y 2
# Candidato 2 puede hacer trabajo 0
# Aristas: (0,1), (1,0), (1,2), (2,0)
# matching = matching_bipartito(3, 3, [(0,1), (1,0), (1,2), (2,0)])
# print(f"Matching Máximo: {matching}") # Salida esperada: 3
```
