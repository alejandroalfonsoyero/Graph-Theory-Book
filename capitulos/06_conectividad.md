# Conectividad y Componentes Fuertemente Conexas (SCC)

La conectividad es una propiedad fundamental que determina qué tan robusta o
integrada es una red. En este capítulo, exploraremos cómo identificar las partes
críticas de un grafo, como los "puntos de fallo único" (puentes y puntos de
articulación), y cómo descomponer grafos dirigidos en sus estructuras cíclicas
básicas: las Componentes Fuertemente Conexas (SCC).

---

## Conectividad en Grafos No Dirigidos

En un grafo no dirigido, la conectividad se refiere a la capacidad de llegar de
cualquier vértice a cualquier otro.

### Conceptos Clave

*   **Componente Conexa:** Un subconjunto maximal de vértices tal que existe un
    camino entre cada par de ellos.
*   **Punto de Articulación (Cut Vertex):** Un vértice que, si se elimina (junto
    con sus aristas incidentes), aumenta el número de componentes conexas del
    grafo. Representan vulnerabilidades o "cuellos de botella".
*   **Puente (Bridge):** Una arista que, si se elimina, aumenta el número de
    componentes conexas. En una red de computadoras, un puente es un cable
    crítico cuya falla desconecta la red.

### Algoritmo para Encontrar Puentes (Tarjan)

El método ingenuo para encontrar puentes consiste en eliminar cada arista una
por una y verificar con BFS/DFS si el grafo sigue conexo ($O(E \cdot (V+E))$).
Sin embargo, podemos hacerlo mucho más rápido, en $O(V+E)$, usando un solo
recorrido DFS.

#### Lógica del Algoritmo (Discovery Time y Low-Link)

Para cada nodo `u` en el árbol DFS, mantenemos dos valores:

1.  **`disc[u]` (Discovery Time):** El tiempo (o contador) en el que el nodo
    `u` fue visitado por primera vez durante el DFS.
2.  **`low[u]` (Low-Link Value):** El menor `disc` alcanzable desde `u` (incluido
    él mismo) en el subárbol DFS de `u`, posiblemente utilizando una
    **arista de retroceso** (back-edge), pero no la arista directa hacia su padre.

**Condición de Puente:** Una arista `(u, v)` es un puente si y solo si
`low[v] > disc[u]`.

Esto significa que no hay ninguna arista de retroceso desde el subárbol de `v`
que conecte con `u` o con cualquiera de sus ancestros. Por lo tanto, la única
forma de llegar a `v` desde `u` es a través de la arista `(u, v)`.

#### Implementación en Python

```python
def encontrar_puentes(grafo) -> list[tuple[int, int]]:
    """
    Encuentra todos los puentes en un grafo no dirigido usando DFS.
    :param grafo: Instancia de GrafoListaAdyacencia (no dirigido).
    :return: Lista de tuplas (u, v) representando los puentes.
    """
    n = grafo.n
    disc = [-1] * n
    low = [-1] * n
    tiempo = 0
    puentes = []

    def dfs(u: int, padre: int = -1):
        nonlocal tiempo
        disc[u] = low[u] = tiempo
        tiempo += 1

        for v, _ in grafo.obtener_vecinos(u):
            if v == padre:
                continue

            if disc[v] != -1:
                # v ya visitado: es una arista de retroceso
                low[u] = min(low[u], disc[v])
            else:
                # v no visitado: es una arista del árbol (tree-edge)
                dfs(v, u)

                # Al regresar, actualizamos low[u] basado en el hijo
                low[u] = min(low[u], low[v])

                # Chequeo de puente
                if low[v] > disc[u]:
                    puentes.append((u, v))

    for i in range(n):
        if disc[i] == -1:
            dfs(i)

    return puentes

# Ejemplo de uso
# g = GrafoListaAdyacencia(5, dirigido=False)
# g.agregar_arista(1, 0); g.agregar_arista(0, 2)
# g.agregar_arista(2, 1); g.agregar_arista(0, 3)
# g.agregar_arista(3, 4)
# print(encontrar_puentes(g))
# Salida esperada: [(3, 4), (0, 3)]
```

---

## Conectividad en Grafos Dirigidos

En grafos dirigidos, la conectividad es más compleja debido a la dirección de
las aristas.

### Componentes Fuertemente Conexas (SCC)

Una **Componente Fuertemente Conexa (SCC)** es un subgrafo maximal donde para
cada par de vértices $u, v$, existe un camino de $u$ a $v$ **Y** un camino de
$v$ a $u$.

Si contraemos cada SCC en un solo super-nodo, el grafo resultante es siempre un
**DAG** (Grafo Acíclico Dirigido), conocido como el **Grafo de Condensación**.

### Algoritmo de Kosaraju

Existen varios algoritmos lineales ($O(V+E)$) para encontrar SCCs (Tarjan,
Kosaraju, Gabow). El algoritmo de **Kosaraju** es conceptualmente el más
sencillo de entender y se basa en dos pasadas de DFS.

#### Pasos del Algoritmo

1.  **Primera Pasada (DFS):** Realizar un DFS completo sobre el grafo original
    $G$ y almacenar los vértices en una pila en orden de **finalización** (cuando
    la llamada recursiva retorna). El nodo que termina último estará en el tope.
2.  **Transponer el Grafo ($G^T$):** Crear un nuevo grafo con las mismas aristas
    pero en dirección opuesta (si $u \to v$ existe en $G$, entonces $v \to u$
    existe en $G^T$).
3.  **Segunda Pasada (DFS en $G^T$):** Procesar los vértices uno a uno sacándolos
    de la pila creada en el paso 1. Si un vértice no ha sido visitado en esta
    segunda pasada, iniciar un DFS desde él en $G^T$. Todos los vértices
    alcanzables en este DFS forman una nueva SCC.

#### Implementación en Python

```python
def encontrar_scc_kosaraju(grafo) -> list[list[int]]:
    """
    Encuentra las Componentes Fuertemente Conexas (SCC) usando el
    algoritmo de Kosaraju.
    :param grafo: Instancia de GrafoListaAdyacencia (dirigido).
    :return: Lista de listas, donde cada sublista es una SCC.
    """
    n = grafo.n
    visitados = [False] * n
    pila = []

    # 1. Primera pasada: Llenar la pila por orden de finalización
    def dfs_llenar_pila(u):
        visitados[u] = True
        for v, _ in grafo.obtener_vecinos(u):
            if not visitados[v]:
                dfs_llenar_pila(v)
        pila.append(u)

    for i in range(n):
        if not visitados[i]:
            dfs_llenar_pila(i)

    # 2. Transponer el grafo (invertir aristas)
    # Nota: Esto requiere acceso a la estructura interna o un método
    # `transponer`. Aquí lo construimos manualmente para el ejemplo.
    grafo_t = {i: [] for i in range(n)}
    for u in range(n):
        for v, _ in grafo.obtener_vecinos(u):
            grafo_t[v].append(u) # Arista v -> u

    # 3. Segunda pasada: DFS en el grafo transpuesto
    visitados = [False] * n
    sccs = []

    def dfs_scc(u, componente_actual):
        visitados[u] = True
        componente_actual.append(u)
        for v in grafo_t[u]:
            if not visitados[v]:
                dfs_scc(v, componente_actual)

    while pila:
        u = pila.pop()
        if not visitados[u]:
            componente_actual = []
            dfs_scc(u, componente_actual)
            sccs.append(componente_actual)

    return sccs

# Ejemplo de uso
# g_dir = GrafoListaAdyacencia(5, dirigido=True)
# g_dir.agregar_arista(1, 0)
# g_dir.agregar_arista(0, 2)
# g_dir.agregar_arista(2, 1) # Ciclo 0-1-2
# g_dir.agregar_arista(0, 3)
# g_dir.agregar_arista(3, 4)
# print(encontrar_scc_kosaraju(g_dir))
# Salida esperada: [[0, 2, 1], [3], [4]] (el orden dentro de SCC puede variar)
```

---

## Aplicaciones Prácticas

### Análisis de Redes y Vulnerabilidad

La identificación de puntos de articulación y puentes es crucial en el diseño
de redes de telecomunicaciones, eléctricas o de transporte.
*   **Robustez:** Una red es robusta si no tiene puntos de articulación (es decir,
    es biconexa). Esto garantiza que la falla de un solo nodo no desconectará
    la red.
*   **Diseño:** Al diseñar una red, se busca minimizar el número de puentes
    añadiendo redundancia estratégica.

### Resolución de 2-Satisfacibilidad (2-SAT)

El problema de satisfacibilidad booleana (SAT) es en general NP-completo. Sin
embargo, el caso especial **2-SAT** (donde cada cláusula tiene a lo sumo 2
literales) se puede resolver en tiempo polinomial usando SCCs.

1.  Se construye un grafo de implicación donde las variables y sus negaciones
    son nodos. La cláusula $(A \lor B)$ equivale a $(\neg A \implies B)$ y
    $(\neg B \implies A)$.
2.  Se calculan las SCCs del grafo.
3.  Si una variable $x$ y su negación $\neg x$ están en la misma SCC, la fórmula
    es insatisfacible (porque $x \implies \dots \implies \neg x \implies \dots
    \implies x$, una contradicción).
4.  Si no, se puede encontrar una asignación de verdad válida usando el orden
    topológico de las SCCs.

### Optimización de Consultas en Grafos Web

En el análisis de la web, las SCCs ayudan a agrupar páginas que se enlazan
fuertemente entre sí. El "Grafo de la Web" se puede simplificar contrayendo
millones de páginas en sus respectivas SCCs, resultando en una estructura
"Bow-tie" (Moño) que facilita el análisis macroscópico y algoritmos como
PageRank.