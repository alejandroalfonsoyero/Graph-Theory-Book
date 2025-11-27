# Introducción a la Complejidad y Técnicas Avanzadas

Hasta ahora, hemos cubierto algoritmos que resuelven problemas de manera eficiente (en tiempo polinomial). Sin embargo, no todos los problemas de grafos son tan "amigables". En este capítulo, nos adentraremos en el fascinante mundo de la complejidad computacional y exploraremos técnicas avanzadas para abordar problemas difíciles.

---

## Clases de Complejidad: P, NP y NP-Completo

Entender qué hace que un problema sea "difícil" es crucial para no perder tiempo buscando algoritmos eficientes que probablemente no existan.

### Definiciones Básicas

*   **P (Polinomial):** La clase de problemas de decisión que pueden ser *resueltos* por un algoritmo determinista en tiempo polinomial ($O(V^k)$ para alguna constante $k$). Ejemplos: Camino más corto (Dijkstra), MST (Kruskal), Flujo Máximo.
*   **NP (No-determinista Polinomial):** La clase de problemas cuya *solución* (si se nos da una propuesta) puede ser *verificada* en tiempo polinomial. Todo problema en P está también en NP.
*   **NP-Completo:** Son los problemas "más difíciles" dentro de NP. Si pudieras resolver cualquier problema NP-Completo en tiempo polinomial, podrías resolver *todos* los problemas de NP en tiempo polinomial (demostrando que $P = NP$, uno de los mayores problemas abiertos en matemáticas).

### Problemas NP-Completos Famosos en Grafos

1.  **Problema del Viajante de Comercio (TSP):** Dado un conjunto de ciudades y distancias, encontrar la ruta más corta que visite cada ciudad exactamente una vez y regrese al inicio.
2.  **Coloración de Grafos ($k$-Coloreado):** ¿Es posible asignar uno de $k$ colores a cada vértice tal que ningún par de vértices adyacentes tenga el mismo color? (Para $k \ge 3$).
3.  **Clique Máximo:** Encontrar el subgrafo completo más grande dentro de un grafo.
4.  **Cobertura de Vértices (Vertex Cover):** Encontrar el subconjunto más pequeño de vértices tal que cada arista del grafo incida en al menos un vértice de ese subconjunto.

### ¿Qué hacer ante un problema NP-Completo?

Si te enfrentas a uno de estos problemas en la vida real, tienes tres opciones principales:
1.  **Algoritmos de Fuerza Bruta (Backtracking):** Solo viables para grafos muy pequeños.
2.  **Heurísticas y Algoritmos de Aproximación:** Encontrar una solución "suficientemente buena" (cerca del óptimo) en un tiempo razonable.
3.  **Casos Especiales:** Verificar si tu grafo tiene propiedades especiales (como ser un árbol o un grafo bipartito) que permitan soluciones eficientes.

---

## 2-Satisfiability (2-SAT)

El problema de satisfacibilidad booleana (SAT) es el problema NP-Completo por excelencia. Sin embargo, una variante restringida llamada **2-SAT** puede resolverse en tiempo lineal usando grafos.

### Formulación

Dada una fórmula lógica en forma normal conjuntiva (CNF) donde cada cláusula tiene exactamente dos literales, por ejemplo:
$$(x_1 \lor \neg x_2) \land (\neg x_1 \lor x_3) \land (x_2 \lor \neg x_3)$$
¿Existe una asignación de valores de verdad (V/F) para las variables tal que la fórmula sea verdadera?

La clave es observar que la cláusula $(A \lor B)$ es lógicamente equivalente a las implicaciones $(\neg A \implies B)$ y $(\neg B \implies A)$.

### Construcción del Grafo de Implicación

Construimos un grafo dirigido donde:
*   Los nodos son los literales (para cada variable $x_i$, tenemos nodos $x_i$ y $\neg x_i$).
*   Las aristas representan las implicaciones. Para cada cláusula $(A \lor B)$, añadimos aristas dirigidas $(\neg A, B)$ y $(\neg B, A)$.

### Solución con Componentes Fuertemente Conexas (SCC)

**Teorema:** Una instancia de 2-SAT es satisfacible si y solo si ninguna variable $x$ y su negación $\neg x$ pertenecen a la misma Componente Fuertemente Conexa (SCC).

Si $x$ y $\neg x$ están en la misma SCC, significa que $x \implies \dots \implies \neg x$ y $\neg x \implies \dots \implies x$, lo cual es una contradicción ($x \iff \neg x$).

**Algoritmo:**
1.  Construir el grafo de implicación.
2.  Encontrar las SCCs (usando Tarjan o Kosaraju).
3.  Para cada variable $x$, verificar si `SCC(x) == SCC(not x)`. Si ocurre para alguna, es insatisfacible.
4.  Si es satisfacible, una asignación válida se obtiene asignando `Verdadero` a las componentes que aparecen "más tarde" en el orden topológico inverso de las SCCs.

#### Implementación en Python

```python
def resolver_2sat(n_vars: int, clausulas: list[tuple[int, int]]) -> bool:
    """
    Resuelve una instancia de 2-SAT.
    :param n_vars: Número de variables (x1 ... xn).
    :param clausulas: Lista de tuplas (u, v).
                      Si u > 0 representa x_u, si u < 0 representa not x_|u|.
    :return: True si es satisfacible, False si no.
    """
    # Mapeo de literales a nodos:
    # x_i -> 2*(i-1), not x_i -> 2*(i-1) + 1
    # Ejemplo: x_1 -> 0, not x_1 -> 1, x_2 -> 2, not x_2 -> 3...
    
    def literal_a_nodo(lit):
        idx = abs(lit) - 1
        return 2 * idx + (1 if lit < 0 else 0)

    def nodo_a_negacion(nodo):
        return nodo ^ 1 # 0->1, 1->0, 2->3, 3->2...

    total_nodos = 2 * n_vars
    adj = [[] for _ in range(total_nodos)]

    for u_lit, v_lit in clausulas:
        # (A or B) equiv a (not A -> B) y (not B -> A)
        u = literal_a_nodo(u_lit)
        v = literal_a_nodo(v_lit)
        not_u = nodo_a_negacion(u)
        not_v = nodo_a_negacion(v)
        
        adj[not_u].append(v)
        adj[not_v].append(u)

    # Algoritmo de Kosaraju o Tarjan para SCCs (simplificado aquí)
    # ... (implementación de SCC omitida por brevedad, ver Cap 6)
    # Suponemos una función get_sccs(adj) que retorna una lista `scc_id`
    # donde scc_id[u] es el ID del componente de u.
    
    # scc_id = get_sccs(adj) # Placeholder
    
    # Verificación:
    # for i in range(n_vars):
    #     nodo_x = 2 * i
    #     nodo_not_x = 2 * i + 1
    #     if scc_id[nodo_x] == scc_id[nodo_not_x]:
    #         return False
            
    return True # Si pasa todas las verificaciones
```

---

## Heavy-Light Decomposition (HLD)

HLD es una técnica avanzada para descomponer un árbol en un conjunto de caminos (cadenas) disjuntos. Esto permite realizar consultas y actualizaciones en el camino entre dos nodos cualesquiera del árbol de manera muy eficiente: en tiempo $O(\log^2 V)$.

### Concepto

Para cada nodo $u$, clasificamos sus aristas hacia los hijos en dos tipos:
*   **Arista Pesada (Heavy Edge):** Conecta $u$ con su hijo que tiene el subárbol más grande (mayor número de nodos).
*   **Arista Ligera (Light Edge):** Conecta $u$ con cualquier otro hijo.

**Propiedad Clave:** Cualquier camino desde la raíz a una hoja en el árbol pasará por a lo sumo $O(\log V)$ aristas ligeras. Las aristas pesadas forman cadenas continuas.

### Aplicaciones

Al linealizar el árbol en cadenas, podemos aplicar estructuras de datos eficientes como **Segment Trees** o **Fenwick Trees** sobre cada cadena (o sobre una linealización global que respete las cadenas).

Esto nos permite resolver problemas como:
*   **Consulta de Máximo/Suma en Camino:** ¿Cuál es la arista de mayor peso en el camino entre el nodo $u$ y el nodo $v$?
*   **Actualización de Camino:** Sumar un valor $k$ a todas las aristas en el camino entre $u$ y $v$.
*   **Lowest Common Ancestor (LCA):** HLD proporciona una forma de calcular el LCA.

Esta técnica es fundamental en programación competitiva y en sistemas que requieren análisis estructural rápido sobre árboles dinámicos o estáticos con consultas complejas.

---

## Grafos Aleatorios y Redes de Pequeño Mundo

Finalmente, una breve mención a modelos de grafos que describen redes reales:

*   **Grafos Aleatorios (Erdős-Rényi):** Cada par de nodos se conecta con una probabilidad $p$. Útil como modelo base, pero no captura la estructura de redes sociales reales.
*   **Redes de Pequeño Mundo (Watts-Strogatz):** Modelan el fenómeno de "seis grados de separación". Tienen alto coeficiente de agrupamiento (mis amigos son amigos entre sí) y caminos cortos promedios.
*   **Redes Libres de Escala (Barabási-Albert):** Algunos nodos ("hubs") tienen muchísimas conexiones, siguiendo una ley de potencia. Modelan Internet, citas académicas y redes sociales mejor que los grafos aleatorios puros.