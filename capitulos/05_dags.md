# Grafos Dirigidos Acíclicos (DAGs) y Ordenamiento Topológico

Los Grafos Dirigidos Acíclicos, conocidos comúnmente como DAGs (por sus siglas en inglés, *Directed Acyclic Graphs*), ocupan un lugar especial en la teoría de grafos y la informática. Su estructura única, que representa dependencias direccionales sin ciclos, los convierte en la herramienta ideal para modelar flujos de trabajo, sistemas de compilación, análisis de datos y mucho más.

---

## Introducción a los DAGs

### Definición y Propiedades

Un **DAG** es un grafo dirigido que no contiene ningún ciclo dirigido. Es decir, no existe ninguna secuencia de vértices $v_1, v_2, \dots, v_k$ tal que existan aristas $(v_1, v_2), (v_2, v_3), \dots, (v_{k-1}, v_k)$ y $(v_k, v_1)$.

*   **Orden Parcial:** Un DAG define un ordenamiento parcial sobre sus vértices. Si existe una ruta de $u$ a $v$, decimos que $u$ precede a $v$ ($u \preceq v$). Si no hay ruta entre ellos, no son comparables.
*   **Fuentes y Sumideros:**
    *   **Fuente (Source):** Un vértice con grado de entrada 0 (nadie apunta a él). Todo DAG finito tiene al menos una fuente.
    *   **Sumidero (Sink):** Un vértice con grado de salida 0 (no apunta a nadie). Todo DAG finito tiene al menos un sumidero.

---

## Ordenamiento Topológico

El ordenamiento topológico es la operación fundamental sobre los DAGs. Consiste en una ordenación lineal de todos los vértices del grafo tal que, para cada arista dirigida $(u, v)$, el vértice $u$ aparece antes que el vértice $v$ en la secuencia.

*   **Existencia:** Un grafo tiene un ordenamiento topológico si y solo si es un DAG.
*   **Unicidad:** Un DAG puede tener múltiples ordenamientos topológicos válidos. Es único si y solo si tiene un camino hamiltoniano (un camino que visita todos los vértices).

### Algoritmo de Kahn (Basado en Grados de Entrada)

Este algoritmo es intuitivo y se basa en la idea de procesar iterativamente los nodos que no tienen dependencias pendientes.

#### Algoritmo Detallado

1.  Calcula el **grado de entrada** (in-degree) para cada vértice.
2.  Inicializa una cola con todos los vértices que tienen **grado de entrada 0** (fuentes).
3.  Mientras la cola no esté vacía:
    a.  Desencola un vértice `u`.
    b.  Añade `u` a la lista de `orden_topologico`.
    c.  Para cada vecino `v` de `u`:
        i.  Decrementa el grado de entrada de `v` en 1 (simulando que eliminamos la arista $u \to v$).
        ii. Si el grado de entrada de `v` llega a 0, encola `v`.
4.  Si la longitud del `orden_topologico` es menor que el número de vértices, el grafo tiene un ciclo.

#### Implementación en Python

```python
from collections import deque
from typing import List, Dict

# Asumimos GrafoListaAdyacencia del Cap 1

def ordenamiento_topologico_kahn(grafo) -> List[int]:
    """
    Realiza un ordenamiento topológico usando el algoritmo de Kahn.
    :param grafo: Instancia de GrafoListaAdyacencia (debe ser dirigido).
    :return: Lista de vértices en orden topológico.
    :raises ValueError: Si el grafo contiene un ciclo.
    """
    n = grafo.n
    grado_entrada = [0] * n

    # 1. Calcular grados de entrada
    for u in range(n):
        for v, _ in grafo.obtener_vecinos(u):
            grado_entrada[v] += 1

    # 2. Inicializar cola con fuentes
    cola = deque([u for u in range(n) if grado_entrada[u] == 0])
    orden = []

    # 3. Procesar vértices
    while cola:
        u = cola.popleft()
        orden.append(u)

        for v, _ in grafo.obtener_vecinos(u):
            grado_entrada[v] -= 1
            if grado_entrada[v] == 0:
                cola.append(v)

    # 4. Verificar ciclos
    if len(orden) != n:
        raise ValueError("El grafo contiene un ciclo, no es un DAG.")

    return orden
```

### Algoritmo Basado en DFS

Este enfoque utiliza la Búsqueda en Profundidad. La idea clave es que un vértice solo se añade a la lista ordenada cuando todos sus descendientes ya han sido visitados completamente.

#### Algoritmo Detallado

1.  Realiza un DFS completo sobre el grafo.
2.  Mantén un registro del tiempo de finalización o simplemente añade el vértice a una lista cuando la llamada recursiva de DFS termine para ese vértice.
3.  El ordenamiento topológico es la lista de vértices en **orden inverso** a su tiempo de finalización.

#### Implementación en Python

```python
def ordenamiento_topologico_dfs(grafo) -> List[int]:
    """
    Realiza un ordenamiento topológico usando DFS.
    :param grafo: Instancia de GrafoListaAdyacencia (debe ser dirigido).
    :return: Lista de vértices en orden topológico.
    :raises ValueError: Si se detecta un ciclo (back-edge).
    """
    n = grafo.n
    visitados = [0] * n # 0: no visitado, 1: visitando, 2: visitado
    orden = []

    def dfs(u):
        visitados[u] = 1 # Marcamos como visitando (gris)
        
        for v, _ in grafo.obtener_vecinos(u):
            if visitados[v] == 1:
                # Encontramos una arista hacia un nodo en proceso -> Ciclo
                raise ValueError("Ciclo detectado")
            if visitados[v] == 0:
                dfs(v)
        
        visitados[u] = 2 # Marcamos como visitado (negro)
        # Añadimos a la lista al terminar de procesar todos sus hijos
        orden.append(u)

    for i in range(n):
        if visitados[i] == 0:
            try:
                dfs(i)
            except ValueError as e:
                raise e

    # El resultado es el reverso del orden de finalización
    return orden[::-1]
```

---

## Aplicaciones Prácticas

### Resolución de Dependencias

Es el caso de uso clásico.
*   **Gestores de Paquetes (pip, npm):** Determinan el orden en que deben instalarse las librerías. Si A depende de B, B debe instalarse antes.
*   **Sistemas de Construcción (Make, Gradle):** Compilan primero los archivos fuente base antes que los que dependen de ellos.

### Planificación de Tareas (Scheduling)

Si tienes un conjunto de tareas donde algunas deben completarse antes de que otras puedan comenzar, el ordenamiento topológico te da una secuencia válida de ejecución. Esto se usa en diagramas de PERT y gestión de proyectos.

---

## Caminos Más Largos y Ruta Crítica

En grafos generales, encontrar el camino simple más largo es un problema **NP-difícil** (equivalente al problema del Camino Hamiltoniano). Sin embargo, en **DAGs**, este problema se puede resolver eficientemente en tiempo lineal $O(V+E)$.

Esto es crucial para el **Método de la Ruta Crítica (CPM)** en gestión de proyectos: la duración mínima de un proyecto está determinada por el camino más largo de dependencias secuenciales.

### Algoritmo usando Ordenamiento Topológico

La propiedad clave es que, si procesamos los vértices en orden topológico, al llegar a un vértice `u`, ya hemos procesado todos los posibles predecesores que podrían conducir a `u`.

1.  Obtener el ordenamiento topológico del grafo.
2.  Inicializar `dist[v] = -infinito` para todo `v`, excepto `dist[inicio] = 0`.
3.  Iterar por cada vértice `u` en orden topológico:
    *   Si `dist[u]` es finito:
        *   Para cada vecino `v` con peso `w`:
            *   `dist[v] = max(dist[v], dist[u] + w)` (Relajación para máximo).

#### Implementación en Python

```python
def camino_mas_largo_dag(grafo, inicio: int) -> List[float]:
    """
    Calcula la distancia del camino más largo desde 'inicio' a todos
    los demás nodos en un DAG.
    """
    try:
        orden_topo = ordenamiento_topologico_kahn(grafo)
    except ValueError:
        return [] # No es un DAG

    distancias = [float('-inf')] * grafo.n
    distancias[inicio] = 0

    # Procesar nodos en orden topológico garantiza que cuando procesamos u,
    # ya tenemos la distancia máxima correcta hacia u.
    for u in orden_topo:
        if distancias[u] != float('-inf'):
            for v, peso in grafo.obtener_vecinos(u):
                if distancias[u] + peso > distancias[v]:
                    distancias[v] = distancias[u] + peso

    return distancias
```

---