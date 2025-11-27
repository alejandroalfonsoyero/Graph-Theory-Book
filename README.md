# Teoría de Grafos y Algoritmos Fundamentales

**Autor:** Alejandro  
**Audiencia:** Desarrolladores de software con sólidos conocimientos matemáticos y de programación  
**Nivel:** Avanzado  
**Lenguaje de implementación:** Python 3.10+

---

## Descripción

Este libro es una guía completa sobre teoría de grafos y sus algoritmos más importantes, diseñada para desarrolladores profesionales que desean profundizar en estructuras de datos avanzadas y algoritmos de grafos. Cada concepto se presenta con rigor matemático y se acompaña de implementaciones en Python idiomático y eficiente.

## Estructura del Libro

### [Capítulo 1: Fundamentos de Grafos](capitulos/01_fundamentos.md)
- Definiciones formales
- Tipos de grafos
- Representaciones computacionales
- Análisis de complejidad

### [Capítulo 2: Recorridos y Exploración](capitulos/02_recorridos.md)
- DFS (Depth-First Search)
- BFS (Breadth-First Search)
- Aplicaciones: componentes conectados, detección de ciclos, orden topológico

### [Capítulo 3: Caminos Mínimos](capitulos/03_caminos_minimos.md)
- Single-source: BFS, Dijkstra, Bellman-Ford
- All-pairs: Floyd-Warshall
- Heurísticas: A*, Greedy Best-First

### [Capítulo 4: Árboles y Expansión Mínima](capitulos/04_arboles_expansion.md)
- Árboles de expansión
- MST: Kruskal, Prim
- Union-Find
- LCA (Lowest Common Ancestor)

### [Capítulo 5: Grafos Dirigidos y DAGs](capitulos/05_dags.md)
- Detección de ciclos
- SCC: Kosaraju, Tarjan
- Orden topológico
- DP sobre DAG

### [Capítulo 6: Conectividad Avanzada](capitulos/06_conectividad.md)
- Bridges y Articulation points
- Biconnected components
- Strongly Connected Components

### [Capítulo 7: Flujo y Matching](capitulos/07_flujo_matching.md)
- Máximo flujo: Ford-Fulkerson, Edmonds-Karp, Dinic
- Matching bipartito: Hopcroft-Karp
- Teorema max-flow min-cut

### [Capítulo 8: Grafos Especiales](capitulos/08_grafos_especiales.md)
- Grafos bipartitos
- Caminos Eulerianos (Hierholzer)
- Problemas Hamiltonianos
- Técnicas de optimización

### [Capítulo 9: Técnicas Avanzadas](capitulos/09_tecnicas_avanzadas.md)
- Multi-source BFS/Dijkstra
- 0-1 BFS
- Grafos implícitos
- Optimizaciones avanzadas

### [Capítulo 10: Aplicaciones Prácticas](capitulos/10_aplicaciones.md)
- Redes y sistemas distribuidos
- GIS y routing
- Compiladores y análisis de dependencias
- Graph embeddings y ML

---

## Compilación

Para generar el libro completo en PDF:

```bash
python compile_book.py
```

El PDF generado estará en `output/graph_theory_book.pdf`

### Requisitos de compilación
- Python 3.10+
- Pandoc 2.0+
- LaTeX (TeXLive o MiKTeX)

```bash
# Instalar dependencias en Ubuntu/Debian
sudo apt-get install pandoc texlive-latex-base texlive-latex-extra

# En macOS con Homebrew
brew install pandoc
brew install --cask mactex
```

---

## Código de Ejemplo

Todos los algoritmos están implementados en el directorio `codigo/`. Cada módulo puede importarse independientemente:

```python
from codigo.estructuras.grafo import Grafo
from codigo.caminos.dijkstra import dijkstra
from codigo.arboles.kruskal import kruskal

# Crear grafo
g = Grafo(vertices=5)
g.agregar_arista(0, 1, peso=4)
g.agregar_arista(0, 2, peso=2)

# Ejecutar algoritmo
distancias = dijkstra(g, origen=0)
```

---

## Licencia

© 2025 Alejandro. Todos los derechos reservados.
