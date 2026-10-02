# Zachary Gmyr
# 10.02.2026
#
# Built using Python v3.12 (IDE: VSCode)
# Required Packages: networkx, matplotlib
# run as needed: python -m pip install networkx matplotlib
#
# CMP SCI 4300 - Intro to AI
# Main driver for project 1: Local search & optimization for a graph coloring problem
#
# This project uses a hand drawn graph (Fig 1.1) shown in the Introduction section of my lab report.
# In this driver the graph is created then drawn to a new window, and each color conflict is printed
# to the terminal.

import networkx as nx
import matplotlib.pyplot as plt


# build_graph:
# initializes and returns a NetworkX graph with connected edges modeled
# from Fig 1.1, as shown in the Introduction section of the lab report.
def build_graph():
    # construct a NetworkX undirected graph with nodes A-Z
    G = nx.Graph()
    G.add_nodes_from("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    # 43 total hardcoded edges, modeled from Fig 1.1
    G.add_edges_from([
        ("A","O"), ("A","X"), ("B","C"), ("B","D"), ("B","L"), ("C","Y"),
        ("C","Z"), ("D","E"), ("D","G"), ("D","I"), ("D","Y"), ("E","I"),
        ("E","S"), ("E","Y"), ("F","K"), ("F","M"), ("F","T"), ("F","W"),
        ("G","L"), ("G","Q"), ("H","R"), ("H","S"), ("H","Y"), ("I","K"),
        ("I","S"), ("I","V"), ("J","Q"), ("J","U"), ("J","V"), ("K","T"),
        ("K","U"), ("K","W"), ("M","O"), ("M","T"), ("N","P"), ("N","Q"),
        ("P","X"), ("R","Y"), ("R","Z"), ("S","W"), ("T","U"), ("T","X"),
        ("U","X")
    ])

    return G

# draw_graph:
# takes a NetworkX graph and a dictionary of color assignments for each labeled
# node A-Z, and assigns positions for each node according to Fig 1.1.
# draws the graph in a separate window.
def draw_graph(nxgraph, colors):

    # hardcoded/fixed positions for all 26 nodes, modeled from Fig 1.1
    positions = {
        "A": (14, 0), "B": (2, 6), "C": (0, 4), "D": (4, 4), "E": (4, 2),
        "F": (9, -2), "G": (6, 6), "H": (2, 0), "I": (6, 2), "J": (10, 4),
        "K": (8, 0), "L": (4, 6), "M": (11, -2), "N": (12, 6), "O": (14, -2),
        "P": (14, 4), "Q": (10, 6), "R": (0, 0), "S": (4, 0), "T": (10, 0),
        "U": (10, 2), "V": (8, 4), "W": (6, -2), "X": (12, 2), "Y": (2, 2),
        "Z": (0, 2)
    }

    # NetworkX expects the colors in the same order as the graph's nodes
    node_colors = [colors[node] for node in nxgraph.nodes]

    nx.draw(
        nxgraph,
        pos=positions,
        with_labels=True,
        node_color=node_colors
    )

    plt.show()



# DRIVER - testing graph building and node conflicts

graph = build_graph()

# testing color assignment for generated graph
colors = {
    "A": "green",
    "B": "green",
    "C": "green",
    "D": "green",
    "E": "green",
    "F": "green",
    "G": "green",
    "H": "green",
    "I": "green",
    "J": "green",
    "K": "green",
    "L": "green",
    "M": "green",
    "N": "green",
    "O": "green",
    "P": "green",
    "Q": "green",
    "R": "green",
    "S": "green",
    "T": "green",
    "U": "green",
    "V": "green",
    "W": "green",
    "X": "green",
    "Y": "green",
    "Z": "green"
}

draw_graph(graph, colors)

i = 1
# Check for conflict and print each one
for u, v in graph.edges:
    if (colors[u] == colors[v]):
        print(f"[{i}] CONFLICT: {u}={colors[u]} <=> {v}={colors[v]}")
        i+=1