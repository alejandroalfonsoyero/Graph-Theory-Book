# Grafos Especiales y sus Algoritmos

No todos los grafos son iguales. Existen clases específicas de grafos que poseen estructuras y propiedades únicas. Reconocer que un problema se puede modelar con uno de estos grafos especiales es a menudo la clave para desbloquear soluciones mucho más eficientes que las disponibles para grafos generales.

En este capítulo, exploraremos tres tipos fundamentales: Árboles, Grafos Bipartitos y Grafos Planos.

---

## Árboles

Los árboles son quizás la estructura de datos más fundamental después de los arrays y las listas enlazadas. En teoría de grafos, un árbol es un grafo no dirigido que es **conexo** y **acíclico**.

### Propiedades Definitorias

Un grafo $G$ con $V$ vértices es un árbol si cumple cualquiera de las siguientes condiciones equivalentes:

*   Es conexo y tiene $V-1$ aristas.
*   Es acíclico y tiene $V-1$ aristas.
*   Existe un único camino simple entre cualquier par de vértices.
*   Si se añade cualquier arista, se crea exactamente un ciclo.
*   Si se elimina cualquier arista, el grafo deja de ser conexo (la arista es un puente).

### Terminología de Árboles Enraizados

Aunque los árboles en teoría de grafos no tienen dirección, en informática a menudo elegimos un nodo como **raíz** (root), lo que induce una jerarquía:

*   **Raíz:** El nodo superior.
*   **Padre/Hijo:** Si $u$ está conectado a $v$ y $u$ está más cerca de la raíz, $u$ es el padre de $v$.
*   **Hoja (Leaf):** Un nodo sin hijos (grado 1, excepto si es la raíz única).
*   **Altura:** La longitud del camino más largo desde la raíz hasta una hoja.
*   **Profundidad:** La longitud del camino desde la raíz hasta un nodo específico.

### Recorridos en Árboles (Tree Traversals)

A diferencia de los grafos generales donde usamos BFS/DFS genéricos, en árboles (especialmente binarios) definimos órdenes de visita específicos que son variantes de DFS.

*   **Pre-orden (Pre-order):** Raíz $\to$ Izquierda $\to$ Derecha. Útil para copiar árboles.
*   **In-orden (In-order):** Izquierda $\to$ Raíz $\to$ Derecha. En árboles de búsqueda binaria (BST), visita los nodos en orden ascendente.
*   **Post-orden (Post-order):** Izquierda $\to$ Derecha $\to$ Raíz. Útil para eliminar árboles o evaluar expresiones matemáticas.

#### Implementación en Python (Árbol N-ario)

```python
class TreeNode:
    def __init__(self, valor: int):
        self.valor = valor
        self.hijos: list['TreeNode'] = []

    def agregar_hijo(self, nodo_hijo: 'TreeNode'):
        self.hijos.append(nodo_hijo)

def recorrido_preorden(raiz: TreeNode, resultado: list[int]):
    if raiz is None:
        return
    # Procesar raíz
    resultado.append(raiz.valor)
    # Procesar hijos recursivamente
    for hijo in raiz.hijos:
        recorrido_preorden(hijo, resultado)

def recorrido_postorden(raiz: TreeNode, resultado: list[int]):
    if raiz is None:
        return
    for hijo in raiz.hijos:
        recorrido_postorden(hijo, resultado)
    resultado.append(raiz.valor)

# Ejemplo
#       1
#     /   \
#    2     3
#   / \
#  4   5
# raiz = TreeNode(1)
# n2 = TreeNode(2); n3 = TreeNode(3)
# raiz.agregar_hijo(n2); raiz.agregar_hijo(n3)
# n2.agregar_hijo(TreeNode(4)); n2.agregar_hijo(TreeNode(5))
# res = []
# recorrido_preorden(raiz, res)
# print(f"Pre-orden: {res}") # [1, 2, 4, 5, 3]
```

### Centro y Diámetro de un Árbol

*   **Diámetro:** El camino simple más largo entre dos nodos cualesquiera del árbol. Se puede encontrar con dos BFS:
    1.  BFS desde un nodo arbitrario $u$ para encontrar el nodo más lejano $v$.
    2.  BFS desde $v$ para encontrar el nodo más lejano $w$.
    3.  La distancia entre $v$ y $w$ es el diámetro.
*   **Centro:** El vértice (o dos vértices adyacentes) que minimiza la distancia máxima a cualquier otro nodo. Es el punto medio del diámetro.

---

## Grafos Bipartitos

Un grafo es **bipartito** si sus vértices se pueden dividir en dos conjuntos disjuntos, $U$ y $V$, de tal manera que cada arista conecte un vértice en $U$ con uno en $V$. No existen aristas que conecten dos vértices dentro del mismo conjunto.

### Caracterización

**Teorema:** Un grafo es bipartito si y solo si **no contiene ciclos de longitud impar**.

### Detección de Bipartición (2-Coloreado)

Podemos verificar si un grafo es bipartito intentando colorearlo con dos colores (0 y 1) usando BFS o DFS.

1.  Asignar al vértice inicial el color 0.
2.  Para cada vecino:
    *   Si no tiene color, asignarle el color opuesto al actual (1 - color_actual).
    *   Si ya tiene color y es el mismo que el actual, **el grafo no es bipartito**.

#### Implementación en Python

```python
from collections import deque

def es_bipartito(grafo) -> bool:
    """
    Determina si un grafo es bipartito usando 2-coloreado (BFS).
    :param grafo: Instancia de GrafoListaAdyacencia.
    """
    colores = {} # Mapa: vertice_id -> color (0 o 1)

    # Iterar sobre todos los nodos para manejar grafos no conexos
    for i in range(grafo.n):
        if i in colores:
            continue

        colores[i] = 0
        cola = deque([i])

        while cola:
            u = cola.popleft()
            color_u = colores[u]

            for v, _ in grafo.obtener_vecinos(u):
                if v not in colores:
                    colores[v] = 1 - color_u
                    cola.append(v)
                elif colores[v] == color_u:
                    # Conflicto: vecino tiene el mismo color
                    return False
    return True
```

---

## Grafos Planos

Un **grafo plano** es aquel que puede ser dibujado en el plano (una hoja de papel) de tal manera que **ninguna de sus aristas se cruce**.

### Fórmula de Euler

Para cualquier grafo plano conexo dibujado sin cruces, se cumple la relación:

$$ V - E + F = 2 $$

Donde:
*   $V$: Número de vértices.
*   $E$: Número de aristas.
*   $F$: Número de caras (regiones delimitadas por aristas, incluyendo la región exterior infinita).

### Teorema de Kuratowski

¿Cómo sabemos si un grafo *no* es plano? El teorema de Kuratowski establece que un grafo es plano si y solo si no contiene un subgrafo que sea una subdivisión de:
1.  **$K_5$:** El grafo completo de 5 vértices.
2.  **$K_{3,3}$:** El grafo bipartito completo con 3 vértices en cada conjunto.

### Teorema de los 4 Colores

Este famoso teorema establece que cualquier grafo plano puede ser coloreado con a lo sumo **4 colores** de tal manera que no haya dos vértices adyacentes con el mismo color. Esto tiene aplicaciones directas en la cartografía (colorear mapas de países/regiones).

### Aplicaciones

*   **Diseño de Circuitos (VLSI):** Es crucial diseñar circuitos impresos donde las pistas de cobre no se crucen para evitar cortocircuitos. Se busca que el grafo del circuito sea plano o tenga el mínimo número de cruces.
*   **Redes de Carreteras:** A gran escala, las redes de carreteras son casi planas (excepto por puentes y túneles). Esto permite algoritmos de navegación especializados y más rápidos que los generales.