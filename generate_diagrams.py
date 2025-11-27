#!/usr/bin/env python3
import os

import matplotlib.pyplot as plt
import networkx as nx

# Configuración de estilo
plt.style.use("seaborn-v0_8-whitegrid")
NODE_COLOR = "#89CFF0"  # Baby Blue
EDGE_COLOR = "#808080"  # Gris
HIGHLIGHT_COLOR = "#FF6B6B"  # Rojo suave
NODE_SIZE = 700
FONT_SIZE = 10
IMAGES_DIR = "images"


def save_plot(filename, title=None):
    if title:
        plt.title(title)
    plt.axis("off")
    path = os.path.join(IMAGES_DIR, filename)
    plt.savefig(path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Generado: {path}")


def generate_graph_types():
    # 1. Grafo No Dirigido
    G = nx.Graph()
    G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4)])
    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(4, 4))
    nx.draw_networkx(
        G,
        pos,
        node_color=NODE_COLOR,
        node_size=NODE_SIZE,
        edge_color=EDGE_COLOR,
        font_size=FONT_SIZE,
    )
    save_plot("01_undirected.png", "Grafo No Dirigido")

    # 2. Grafo Dirigido
    D = nx.DiGraph()
    D.add_edges_from([(1, 2), (2, 3), (3, 1), (1, 4)])

    plt.figure(figsize=(4, 4))
    nx.draw_networkx(
        D,
        pos,
        node_color=NODE_COLOR,
        node_size=NODE_SIZE,
        edge_color=EDGE_COLOR,
        font_size=FONT_SIZE,
        arrowsize=20,
    )
    save_plot("01_directed.png", "Grafo Dirigido")

    # 3. Grafo Ponderado
    W = nx.Graph()
    W.add_edge(1, 2, weight=4.5)
    W.add_edge(2, 3, weight=1.2)
    W.add_edge(3, 1, weight=3.0)

    plt.figure(figsize=(4, 4))
    pos_w = nx.spring_layout(W, seed=42)
    nx.draw_networkx(
        W,
        pos_w,
        node_color=NODE_COLOR,
        node_size=NODE_SIZE,
        edge_color=EDGE_COLOR,
        font_size=FONT_SIZE,
    )
    labels = nx.get_edge_attributes(W, "weight")
    nx.draw_networkx_edge_labels(W, pos_w, edge_labels=labels)
    save_plot("01_weighted.png", "Grafo Ponderado")


def generate_bfs_dfs():
    # Árbol para recorridos
    T = nx.balanced_tree(r=2, h=3)
    pos = nx.spring_layout(T, seed=42)

    # BFS: Niveles
    # Colorear por distancia desde la raíz (0)
    layers = dict(nx.bfs_predecessors(T, 0))
    # Simulación simple de capas
    colors = []
    for node in T.nodes():
        dist = nx.shortest_path_length(T, 0, node)
        if dist == 0:
            colors.append("#FF9999")  # Rojo
        elif dist == 1:
            colors.append("#99FF99")  # Verde
        elif dist == 2:
            colors.append("#9999FF")  # Azul
        else:
            colors.append("#FFFF99")  # Amarillo

    plt.figure(figsize=(6, 4))
    nx.draw_networkx(T, pos, node_color=colors, node_size=500, with_labels=True)
    save_plot("02_bfs_layers.png", "BFS: Exploración por Niveles")


def generate_mst_example():
    G = nx.Graph()
    edges = [
        (0, 1, 2),
        (0, 3, 6),
        (1, 2, 3),
        (1, 3, 8),
        (1, 4, 5),
        (2, 4, 7),
        (3, 4, 9),
    ]
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    pos = nx.spring_layout(G, seed=42)

    # MST Edges (kruskal/prim result)
    mst_edges = [(0, 1), (1, 2), (1, 4), (0, 3)]

    plt.figure(figsize=(5, 5))

    # Dibujar todo el grafo en gris
    nx.draw_networkx_edges(G, pos, edge_color="#DDDDDD", width=1)
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=nx.get_edge_attributes(G, "weight")
    )

    # Dibujar MST resaltado
    nx.draw_networkx_edges(
        G, pos, edgelist=mst_edges, edge_color=HIGHLIGHT_COLOR, width=3
    )

    nx.draw_networkx_nodes(G, pos, node_color=NODE_COLOR, node_size=NODE_SIZE)
    nx.draw_networkx_labels(G, pos)

    save_plot("04_mst.png", "Árbol de Expansión Mínima (MST)")


def generate_flow_network():
    G = nx.DiGraph()
    G.add_edge("s", "a", capacity=3)
    G.add_edge("s", "b", capacity=2)
    G.add_edge("a", "b", capacity=1)
    G.add_edge("a", "t", capacity=2)
    G.add_edge("b", "t", capacity=3)

    pos = {"s": (0, 1), "a": (1, 2), "b": (1, 0), "t": (2, 1)}

    plt.figure(figsize=(6, 3))

    nx.draw_networkx_nodes(G, pos, node_color=NODE_COLOR, node_size=NODE_SIZE)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edge_color=EDGE_COLOR, arrowsize=20)

    labels = nx.get_edge_attributes(G, "capacity")
    # Formato "cap: X"
    labels = {k: f"{v}" for k, v in labels.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, label_pos=0.5)

    save_plot("07_flow_network.png", "Red de Flujo (Capacidades)")


if __name__ == "__main__":
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)

    print("Generando diagramas...")
    try:
        generate_graph_types()
        generate_bfs_dfs()
        generate_mst_example()
        generate_flow_network()
        print("¡Listo! Diagramas guardados en 'images/'.")
    except Exception as e:
        print(f"Error generando diagramas: {e}")
