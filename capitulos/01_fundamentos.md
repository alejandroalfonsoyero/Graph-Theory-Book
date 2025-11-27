# Fundamentos de Grafos y Representaciones Eficientes

Este capítulo introduce los conceptos fundamentales de la teoría de grafos, explorando su importancia en diversos campos de la computación y presentando las formas más comunes y eficientes de representarlos en código, con un enfoque particular en Python.

---

## Introducción a los Grafos: ¿Por Qué Son Tan Ubicuos?

La teoría de grafos no es una abstracción puramente matemática; es un marco conceptual que subyace a innumerables estructuras y problemas en el mundo real y la computación. Comprender los grafos es fundamental para cualquier desarrollador de software que busque modelar sistemas complejos y diseñar algoritmos eficientes.

### Contexto Histórico y Orígenes

Los orígenes de la teoría de grafos se remontan al siglo XVIII, con el famoso problema de los **Puentes de Königsberg** planteado por Leonhard Euler en 1736. La ciudad de Königsberg (actual Kaliningrado) estaba dividida por el río Pregel y contenía siete puentes que conectaban dos islas y las dos orillas del río. El problema consistía en determinar si era posible dar un paseo que cruzara cada uno de los siete puentes exactamente una vez y regresara al punto de partida.

Euler modeló este problema simplificándolo a puntos (las masas de tierra) y líneas (los puentes), sentando las bases de lo que hoy conocemos como grafo. Su conclusión de que tal paseo era imposible no solo resolvió el enigma, sino que también inauguró una nueva rama de las matemáticas.

### El Mundo es un Grafo: Ejemplos Intuitivos y Avanzados

Hoy en día, los grafos son omnipresentes y se utilizan para modelar una vasta gama de fenómenos y sistemas:

*   **Redes Sociales:** Plataformas como Facebook, Twitter o LinkedIn pueden verse como grafos gigantes. Los **usuarios** son los vértices (nodos) y las **amistades**, **seguimientos** o **conexiones** son las aristas. El análisis de estas estructuras permite identificar comunidades, predecir tendencias y optimizar la publicidad.
*   **Internet y Redes de Computadoras:** La propia estructura de la World Wide Web puede modelarse como un grafo donde las **páginas web** son nodos y los **hipervínculos** son aristas dirigidas. Las **redes de computadoras** tienen **routers** o **servidores** como vértices y los **cables** o **conexiones inalámbricas** como aristas.
*   **Logística y Transporte:** Sistemas de **navegación** como Google Maps, redes de **transporte público** o rutas de **entrega** utilizan grafos. Las **ciudades** o **intersecciones** son nodos, y las **calles**, **carreteras** o **líneas de metro** son aristas, a menudo con pesos que representan la distancia, el tiempo de viaje o el costo.
*   **Sistemas de Recomendación:** Tiendas online como Amazon o servicios de streaming como Netflix usan grafos para conectar **usuarios** con **productos** o **películas** basándose en interacciones (compras, visualizaciones, valoraciones). Esto permite sugerir nuevos ítems a los usuarios.
*   **Bioinformática:** En biología computacional, los grafos se utilizan para modelar **redes de interacción proteica**, **redes genéticas** o para el **ensamblaje de genomas**, donde fragmentos de ADN se conectan para reconstruir una secuencia completa.
*   **Ciencia de Datos y Machine Learning:** Los **grafos de conocimiento** representan relaciones semánticas entre entidades. Además, una rama emergente, las **Graph Neural Networks (GNNs)**, extiende las técnicas de aprendizaje profundo a datos estructurados en grafos, abriendo nuevas posibilidades para el análisis de redes complejas.

---

## Definiciones Fundamentales y Terminología

Para trabajar eficazmente con grafos, es crucial dominar la terminología básica.

### Componentes Básicos

Un **grafo** $G$ se define formalmente como un par ordenado de conjuntos $G = (V, E)$, donde:
*   **Vértices (Nodos):** $V$ es un conjunto finito y no vacío de elementos llamados vértices. Se suelen denotar como $v_1, v_2, \ldots, v_n$.
*   **Aristas (Enlaces, Arcos):** $E$ es un conjunto de pares de vértices, llamados aristas. Las aristas conectan dos vértices y representan una relación entre ellos. Se suelen denotar como $e_1, e_2, \ldots, e_m$.

### Tipos de Grafos

La naturaleza de las aristas y vértices determina el tipo de grafo:

*   **Grafo No Dirigido:** Las aristas no tienen una dirección específica. Si una arista conecta el vértice $u$ con el vértice $v$, entonces la relación es bidireccional, es decir, $(u, v)$ es lo mismo que $(v, u)$.

    ![Grafo No Dirigido](images/01_undirected.png){ width=50% }

    *   **Ejemplo:** Una red de amistades en la que la amistad es mutua.

*   **Grafo Dirigido (Dígrafo):** Las aristas tienen una dirección clara, del vértice origen al vértice destino. Una arista $(u \to v)$ es diferente de una arista $(v \to u)$.

    ![Grafo Dirigido](images/01_directed.png){ width=50% }

    *   **Ejemplo:** Seguir a alguien en Twitter (el seguimiento no es necesariamente mutuo), una carretera de sentido único.

*   **Grafo Ponderado:** Cada arista tiene asociado un valor numérico, llamado **peso**, **costo** o **distancia**, $w(u, v) \in \mathbb{R}$. Estos pesos pueden representar distancias físicas, tiempos de viaje, costos, capacidades, etc.

    ![Grafo Ponderado](images/01_weighted.png){ width=50% }

    *   **Ejemplo:** Un mapa de carreteras donde el peso es la distancia entre ciudades.

*   **Grafo No Ponderado:** Las aristas no tienen un peso explícito. A menudo, se asume un peso unitario para todas las aristas si se calculan distancias.
    *   **Ejemplo:** Un diagrama de flujo donde solo importa la secuencia, no la "costo" de la transición.

*   **Grafo Simple:** Un grafo que no contiene lazos (aristas que conectan un vértice consigo mismo, ej., $(v, v)$) ni aristas múltiples (más de una arista entre el mismo par de vértices).
    *   **La mayoría de los algoritmos de grafos asumen grafos simples.**

*   **Multígrafo:** Un grafo que permite la existencia de múltiples aristas entre el mismo par de vértices.
    *   **Ejemplo:** Múltiples líneas de autobús que conectan dos paradas.

*   **Pseudógrafo:** Un grafo que permite lazos y aristas múltiples.

### Terminología de Vértices y Aristas

*   **Vértices Adyacentes (Vecinos):** Dos vértices $u$ y $v$ son adyacentes si existe una arista que los conecta. En un grafo dirigido, $u$ es adyacente a $v$ si existe una arista $(u \to v)$.
*   **Incidencia:** Una arista es incidente a los vértices que conecta. Por ejemplo, la arista $(u, v)$ es incidente a $u$ y a $v$.
*   **Grado de un Vértice (No Dirigido):** El número de aristas incidentes a un vértice. Se denota como $\text{grado}(v)$. Un lazo contribuye dos veces al grado.
*   **Grado de Entrada y Salida (Dirigido):**
    *   **Grado de Entrada ($\text{grado}^-(v)$):** Número de aristas que tienen a $v$ como vértice destino.
    *   **Grado de Salida ($\text{grado}^+(v)$):** Número de aristas que tienen a $v$ como vértice origen.
*   **Vértice Aislado:** Un vértice con grado 0 (no está conectado a ningún otro vértice).
*   **Vértice Pendiente (Hoja):** Un vértice con grado 1.
*   **Subgrafo:** Un grafo $G'=(V', E')$ es subgrafo de $G=(V, E)$ si $V' \subseteq V$ y $E' \subseteq E$.
    *   **Subgrafo Inducido:** Es un subgrafo definido por un subconjunto de vértices $V' \subseteq V$ que incluye *todas* las aristas de $E$ cuyos extremos están en $V'$.
    *   **Supergrafo:** Un grafo $G$ es supergrafo de $G'$ si $G'$ es subgrafo de $G$.

### Caminos y Conectividad

*   **Camino (Paseo/Walk):** Una secuencia de vértices $v_0, v_1, \ldots, v_k$ tal que cada par $(v_i, v_{i+1})$ es una arista. En general, se permiten vértices y aristas repetidos.
    *   **Camino Simple:** Un camino en el que todos los vértices son distintos.
*   **Ciclo:** Un camino cerrado (comienza y termina en el mismo vértice, $v_0 = v_k$) con longitud $k \geq 1$.
    *   **Ciclo Simple:** Un ciclo donde todos los vértices son distintos, excepto el primero y el último ($v_0=v_k$).
*   **Longitud de un Camino/Ciclo:**
    *   En grafos no ponderados, es el número de aristas en el camino/ciclo.
    *   En grafos ponderados, es la suma de los pesos de las aristas en el camino/ciclo.
*   **Conectividad (en Grafos No Dirigidos):**
    *   **Grafo Conexo:** Si existe al menos un camino entre cada par de vértices en el grafo.
    *   **Componente Conexa:** Un subgrafo maximal conexo. Un grafo no conexo se compone de varias componentes conexas.
*   **Conectividad (en Grafos Dirigidos):**
    *   **Fuertemente Conexo:** Si existe un camino de $u$ a $v$ Y un camino de $v$ a $u$ para *cada* par de vértices $(u, v)$ en el grafo.
    *   **Débilmente Conexo:** Si el grafo subyacente (el grafo no dirigido que se obtiene al ignorar las direcciones de las aristas) es conexo.
*   **Distancia:** En un grafo ponderado (o no ponderado), la distancia entre dos vértices $u$ y $v$ es la longitud del camino más corto entre ellos.
*   **Diámetro:** La mayor de todas las distancias de caminos más cortos entre todos los pares de vértices en el grafo.

---

## Representaciones Computacionales de Grafos

La elección de cómo representar un grafo en la memoria de una computadora es crucial, ya que afecta directamente la eficiencia (tiempo y espacio) de los algoritmos que se ejecutarán sobre él.

### Consideraciones de Diseño

Al elegir una representación, es importante evaluar:

*   **Espacio (Complejidad Espacial):** ¿Cuánta memoria utiliza la estructura de datos para almacenar el grafo? Esto a menudo depende del número de vértices ($V$) y el número de aristas ($E$).
*   **Tiempo de Operaciones Clave (Complejidad Temporal):** La eficiencia de las operaciones más frecuentes:
    *   **Agregar/Eliminar un Vértice:** Costo de añadir o quitar un nodo.
    *   **Agregar/Eliminar una Arista:** Costo de establecer o romper una conexión.
    *   **Consultar si Existe una Arista $(u, v)$:** ¿Es $u$ adyacente a $v$?
    *   **Obtener Todos los Vecinos de un Vértice $u$:** ¿Cuáles son los nodos directamente conectados a $u$?
    *   **Iterar Sobre Todas las Aristas del Grafo:** Costo de recorrer todas las conexiones.
*   **Tipos de Grafos (Denso vs. Disperso):**
    *   **Grafo Denso:** Un grafo con un número elevado de aristas, cercano al máximo posible ($E \approx V^2$). Para $V=100$, un grafo denso podría tener miles de aristas.
    *   **Grafo Disperso (Sparse):** Un grafo con relativamente pocas aristas ($E \approx V$). Para $V=100$, un grafo disperso podría tener solo unos cientos de aristas.

### Lista de Adyacencia (Adjacency List)

Esta es una de las representaciones más comunes y flexibles.

*   **Concepto:** Cada vértice se asocia con una lista (o arreglo) de sus vértices adyacentes. Si el grafo es ponderado, la lista contendrá pares (vecino, peso).

*   **Estructuras de Datos en Python:**
    *   Para grafos no ponderados, un diccionario donde las claves son vértices y los valores son listas de enteros (vecinos): `dict[int, list[int]]`.
    *   Para grafos ponderados, un diccionario donde las claves son vértices y los valores son listas de tuplas `(vecino, peso)`: `dict[int, list[tuple[int, float]]]`.

*   **Implementación de Clases en Python:**

    ```python
    class GrafoListaAdyacencia:
        """
        Representación de un grafo mediante lista de adyacencia.
        Soporta grafos dirigidos/no dirigidos y ponderados/no
        ponderados. Los vértices se identifican por enteros de 0 a
        n_vertices - 1.
        """
        def __init__(self, n_vertices: int, dirigido: bool = False):
            """
            Inicializa un grafo con n_vertices.
            :param n_vertices: Número total de vértices en el grafo.
            :param dirigido: True si el grafo es dirigido, False si es no
                             dirigido.
            """
            self.n = n_vertices
            self.dirigido = dirigido
            # Un diccionario donde cada clave (vértice) mapea a una lista
            # de sus vecinos. Cada vecino es una tupla (ID_vecino, peso_arista)
            self.adyacencia: dict[int, list[tuple[int, float]]] = \
                {i: [] for i in range(n_vertices)}

        def agregar_arista(self, u: int, v: int, peso: float = 1.0):
            """
            Agrega una arista al grafo.
            :param u: Vértice de origen.
            :param v: Vértice de destino.
            :param peso: Peso de la arista (por defecto 1.0 para no ponderados).
            """
            if not (0 <= u < self.n and 0 <= v < self.n):
                raise ValueError(f"Vértices {u} o {v} fuera del rango "
                                 f"[0, {self.n-1}]")

            # Para evitar aristas duplicadas si ya existe (u,v)
            if not self.tiene_arista(u, v):
                self.adyacencia[u].append((v, peso))

            if not self.dirigido and not self.tiene_arista(v, u):
                # Añade también (v,u) si no es dirigido
                self.adyacencia[v].append((u, peso))

        def obtener_vecinos(self, u: int) -> list[tuple[int, float]]:
            """
            Retorna la lista de tuplas (vecino, peso) para el vértice u.
            :param u: Vértice del cual obtener los vecinos.
            :return: Lista de vecinos y sus pesos.
            """
            if not (0 <= u < self.n):
                raise ValueError(f"Vértice {u} fuera del rango "
                                 f"[0, {self.n-1}]")
            return self.adyacencia[u]

        def tiene_arista(self, u: int, v: int) -> bool:
            """
            Verifica si existe una arista entre u y v.
            :param u: Vértice de origen.
            :param v: Vértice de destino.
            :return: True si la arista existe, False en caso contrario.
            """
            if not (0 <= u < self.n and 0 <= v < self.n):
                # O lanzar ValueError, dependiendo de la política deseada
                return False
            return any(vecino_id == v for vecino_id, _ in self.adyacencia[u])

        def __str__(self):
            s = (f"Grafo (Lista de Adyacencia, "
                 f"{'Dirigido' if self.dirigido else 'No Dirigido'}):\\n")
            for u in range(self.n):
                s += f"{u}: "
                vecinos_str = [f"({v}, p={p:.2f})"
                               for v, p in self.adyacencia[u]]
                s += ", ".join(vecinos_str) + "\\n"
            return s
    ```

*   **Análisis de Complejidad:**
    *   **Espacio:** $O(V + E)$, donde $V$ es el número de vértices y $E$ es el número de aristas. Para cada vértice, almacenamos su lista de adyacencia, y cada arista se almacena una vez (en grafos dirigidos) o dos veces (en grafos no dirigidos). Esta eficiencia espacial la hace ideal para **grafos dispersos**.
    *   **Tiempo:**
        *   **Agregar Arista:** $O(1)$ en promedio (si se evita duplicados, podría ser $O(\text{grado}(u))$).
        *   **Consultar Arista $(u, v)$:** $O(\text{grado}(u))$ en el peor caso (hay que recorrer la lista de adyacencia de $u$).
        *   **Obtener Vecinos de $u$:** $O(\text{grado}(u))$.
        *   **Iterar Todas las Aristas:** $O(V + E)$ para recorrer todas las listas de adyacencia.

### Matriz de Adyacencia (Adjacency Matrix)

Esta representación es útil en escenarios específicos, principalmente con grafos densos.

*   **Concepto:** Un grafo con $V$ vértices se representa mediante una matriz cuadrada $V \times V$.
    *   Para grafos no ponderados, `matriz[i][j]` es 1 si existe una arista de $i$ a $j$, y 0 en caso contrario.
    *   Para grafos ponderados, `matriz[i][j]` almacena el peso de la arista de $i$ a $j$. Si no hay arista, se puede usar 0, `None`, o infinito ($\infty$) para indicar su ausencia.

*   **Estructuras de Datos en Python:**
    *   Listas anidadas de Python (`list[list[float]]`).
    *   Para mayor eficiencia numérica y de memoria, se prefiere `numpy.ndarray`.

*   **Implementación de Clases en Python:**

    ```python
    import numpy as np

    class GrafoMatrizAdyacencia:
        """
        Representación de un grafo mediante matriz de adyacencia.
        Soporta grafos dirigidos/no dirigidos y ponderados/no
        ponderados. Los vértices se identifican por enteros de 0 a
        n_vertices - 1.
        """
        def __init__(self, n_vertices: int, dirigido: bool = False,
                     valor_no_arista: float = 0.0):
            """
            Inicializa un grafo con n_vertices.
            :param n_vertices: Número total de vértices en el grafo.
            :param dirigido: True si el grafo es dirigido, False si es no
                             dirigido.
            :param valor_no_arista: Valor para indicar la ausencia de una
                                    arista (0.0 o float('inf')).
            """
            self.n = n_vertices
            self.dirigido = dirigido
            self.valor_no_arista = valor_no_arista
            # Inicializa la matriz con el valor_no_arista
            self.matriz = np.full((n_vertices, n_vertices),
                                  valor_no_arista, dtype=float)

        def agregar_arista(self, u: int, v: int, peso: float = 1.0):
            """
            Agrega una arista al grafo.
            :param u: Vértice de origen.
            :param v: Vértice de destino.
            :param peso: Peso de la arista.
            """
            if not (0 <= u < self.n and 0 <= v < self.n):
                raise ValueError(f"Vértices {u} o {v} fuera del rango "
                                 f"[0, {self.n-1}]")

            self.matriz[u][v] = peso
            if not self.dirigido:
                self.matriz[v][u] = peso

        def tiene_arista(self, u: int, v: int) -> bool:
            """
            Verifica si existe una arista entre u y v.
            :param u: Vértice de origen.
            :param v: Vértice de destino.
            :return: True si la arista existe, False en caso contrario.
            """
            if not (0 <= u < self.n and 0 <= v < self.n):
                return False
            return self.matriz[u][v] != self.valor_no_arista

        def obtener_peso_arista(self, u: int, v: int) -> float:
            """
            Retorna el peso de la arista entre u y v.
            :param u: Vértice de origen.
            :param v: Vértice de destino.
            :return: Peso de la arista o valor_no_arista si no existe.
            """
            if not (0 <= u < self.n and 0 <= v < self.n):
                raise ValueError(f"Vértices {u} o {v} fuera del rango "
                                 f"[0, {self.n-1}]")
            return self.matriz[u][v]

        def obtener_vecinos(self, u: int) -> list[int]:
            """
            Retorna la lista de IDs de los vértices adyacentes a u.
            :param u: Vértice del cual obtener los vecinos.
            :return: Lista de vecinos.
            """
            if not (0 <= u < self.n):
                raise ValueError(f"Vértice {u} fuera del rango "
                                 f"[0, {self.n-1}]")
            return [v for v in range(self.n) if self.tiene_arista(u, v)]

        def __str__(self):
            s = (f"Grafo (Matriz de Adyacencia, "
                 f"{'Dirigido' if self.dirigido else 'No Dirigido'}):\\n")
            s += str(self.matriz) + "\\n"
            return s
    ```

*   **Análisis de Complejidad:**
    *   **Espacio:** $O(V^2)$, ya que la matriz siempre ocupa $V \times V$ posiciones, independientemente del número de aristas. Esto la hace muy eficiente para **grafos densos**, pero derrochadora para grafos dispersos.
    *   **Tiempo:**
        *   **Agregar Arista:** $O(1)$.
        *   **Consultar Arista $(u, v)$:** $O(1)$. Esta es su mayor ventaja.
        *   **Obtener Vecinos de $u$:** $O(V)$ (hay que recorrer la fila completa de $u$).
        *   **Iterar Todas las Aristas:** $O(V^2)$ (hay que recorrer toda la matriz).

### Lista de Aristas (Edge List)

Esta es la representación más sencilla, pero a menudo la menos eficiente para operaciones de grafo generales.

*   **Concepto:** El grafo se representa como una lista o colección de todas sus aristas. Cada arista se almacena como una tupla `(u, v, peso)` o un objeto `Edge`.

*   **Estructuras de Datos en Python:** `list[tuple[int, int, float]]` o una lista de instancias de una clase `Edge` personalizada.

*   **Implementación de Clases en Python:**

    ```python
    from dataclasses import dataclass

    from dataclasses import dataclass

    @dataclass
    class Arista:
        """
        Clase para representar una arista con origen, destino y peso.
        """
        u: int
        v: int
        peso: float = 1.0

    class GrafoListaAristas:
        """
        Representación de un grafo mediante una lista de aristas.
        Soporta grafos dirigidos/no dirigidos y ponderados/no
        ponderados. Los vértices se identifican por enteros de 0 a
        n_vertices - 1.
        """
        def __init__(self, n_vertices: int, dirigido: bool = False):
            """
            Inicializa un grafo con n_vertices.
            :param n_vertices: Número total de vértices en el grafo.
            :param dirigido: True si el grafo es dirigido, False si es no
                             dirigido.
            """
            self.n = n_vertices
            self.dirigido = dirigido
            self.aristas: list[Arista] = []
            # Para algunas operaciones eficientes, es útil tener también un
            # set de vértices
            self.vertices: set[int] = set(range(n_vertices))

        def agregar_arista(self, u: int, v: int, peso: float = 1.0):
            """
            Agrega una arista al grafo.
            Para grafos no dirigidos, se añade una arista en cada dirección.
            :param u: Vértice de origen.
            :param v: Vértice de destino.
            :param peso: Peso de la arista.
            """
            if not (0 <= u < self.n and 0 <= v < self.n):
                raise ValueError(f"Vértices {u} o {v} fuera del rango "
                                 f"[0, {self.n-1}]")

            # Podríamos añadir lógica para evitar duplicados si es necesario,
            # pero típicamente en esta representación se añaden todas las
            # aristas explícitamente.
            self.aristas.append(Arista(u, v, peso))
            if not self.dirigido:
                self.aristas.append(Arista(v, u, peso))

        # Nota: obtener_vecinos y tiene_arista son inherentemente ineficientes
        # en esta representación si no se mantiene una estructura auxiliar.
        # Sus complejidades serían O(E) en el peor caso ya que requieren
        # recorrer la lista de aristas.

        def __str__(self):
            s = (f"Grafo (Lista de Aristas, "
                 f"{'Dirigido' if self.dirigido else 'No Dirigido'}):\\n")
            for arista in self.aristas:
                s += (f"  ({arista.u} --({arista.peso:.2f})--> "
                      f"{arista.v})\\n")
            return s
    ```

*   **Análisis de Complejidad:**
    *   **Espacio:** $O(E)$, ya que solo se almacenan las aristas.
    *   **Tiempo:**
        *   **Agregar Arista:** $O(1)$.
        *   **Consultar Arista $(u, v)$:** $O(E)$ (hay que recorrer toda la lista).
        *   **Obtener Vecinos de $u$:** $O(E)$ (hay que recorrer toda la lista para encontrar aristas incidentes a $u$).
        *   **Iterar Todas las Aristas:** $O(E)$.
    *   **Ventaja:** Simplicidad. Es particularmente útil para algoritmos que procesan *todas* las aristas del grafo de forma independiente o que requieren ordenar las aristas (como el algoritmo de Kruskal para MST).

---

## Comparación y Elección de Representaciones

La elección de la representación adecuada del grafo es un primer paso crítico en el diseño de cualquier algoritmo de grafos eficiente.

### Tabla Comparativa Detallada

| Operación / Característica | Lista de Adyacencia | Matriz de Adyacencia | Lista de Aristas |
| :------------------------- | :------------------ | :------------------- | :--------------- |
| **Espacio**                | $O(V + E)$          | $O(V^2)$             | $O(E)$           |
| **Agregar Arista**         | $O(1)$              | $O(1)$               | $O(1)$           |
| **Consultar Arista $(u, v)$** | $O(\text{grado}(u))$ | $O(1)$               | $O(E)$           |
| **Obtener Vecinos de $u$** | $O(\text{grado}(u))$ | $O(V)$               | $O(E)$           |
| **Iterar Todas las Aristas** | $O(V + E)$          | $O(V^2)$             | $O(E)$           |
| **Adecuado para Grafos**   | Dispersos           | Densos               | Ciertos algoritmos (ej. Kruskal) |

### Casos de Uso

*   **Lista de Adyacencia:**
    *   Es la representación **predominante** para la mayoría de los algoritmos de grafos, especialmente aquellos basados en recorridos (BFS, DFS) y problemas de caminos más cortos (Dijkstra, Bellman-Ford).
    *   Excelente para **grafos dispersos** donde $E \ll V^2$, ya que su consumo de memoria es proporcional al número real de conexiones.
    *   Cuando las operaciones más frecuentes son "obtener los vecinos de un vértice" o "recorrer el grafo".

*   **Matriz de Adyacencia:**
    *   Ideal para **grafos densos** donde $E \approx V^2$.
    *   Cuando se necesita una **consulta de existencia de aristas extremadamente rápida ($O(1)$)**.
    *   Útil en algoritmos que implican iterar sobre todos los pares de vértices o en algoritmos de programación dinámica como Floyd-Warshall.
    *   Su desventaja es el alto consumo de memoria $O(V^2)$, lo que la hace impráctica para grafos con muchos vértices.

*   **Lista de Aristas:**
    *   Menos versátil como representación general.
    *   Principalmente útil para algoritmos que necesitan **procesar todas las aristas de forma independiente**, como el algoritmo de Kruskal para el Árbol de Expansión Mínima (donde las aristas se ordenan por peso).
    *   También es conveniente cuando la definición del grafo se basa puramente en la colección de sus conexiones.

### Librerías de Grafos en Python (Introducción)

Si bien entender las representaciones subyacentes es vital, en la práctica, los desarrolladores de Python a menudo recurren a librerías maduras que abstraen estas complejidades y ofrecen una API de alto nivel. La más popular es **NetworkX**:

*   **NetworkX:** Una potente librería de Python para la creación, manipulación y estudio de la estructura, dinámica y funciones de redes complejas. Permite crear grafos de manera sencilla, añadir nodos y aristas, y proporciona implementaciones de la mayoría de los algoritmos de grafos. Utiliza internamente una variante de lista de adyacencia (diccionario de diccionarios) y ofrece métodos muy optimizados.

    ```python
    import networkx as nx

    # Crear un grafo no dirigido
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3])
    G.add_edge(0, 1, weight=1.0)
    G.add_edge(0, 2, weight=2.0)
    G.add_edge(1, 3, weight=3.0)
    G.add_edge(2, 3, weight=1.5)

    print("Grafo NetworkX (no dirigido):")
    # Mostrar aristas con sus datos (pesos)
    print(list(G.edges(data=True)))

    # Crear un grafo dirigido
    D = nx.DiGraph()
    D.add_edges_from([(0, 1), (0, 2), (1, 3), (2, 3)])
    print("\nGrafo NetworkX (dirigido):")
    print(list(D.edges()))

    # Operaciones básicas
    print(f"\nVecinos de 0 en G: {list(G.neighbors(0))}")
    print(f"Existe arista (0,1) en G: {G.has_edge(0, 1)}")
    print(f"Peso de arista (0,2) en G: {G[0][2]['weight']}")
```

Entender las representaciones manuales es clave para comprender cómo funcionan las librerías internamente, para depurar problemas de rendimiento, y para implementar algoritmos personalizados o variantes no cubiertas por las librerías estándar.

---
