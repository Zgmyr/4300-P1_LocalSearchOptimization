# Zachary Gmyr
# 10.02.2026
# CMP SCI 4300 - Intro to AI
# Main driver for project 1: Local search & optimization for a graph coloring problem
#
# Built using Python v3.12 (IDE: VSCode)
# Required Packages: networkx, matplotlib
# run as needed: python -m pip install networkx matplotlib
#
# Description:
# This project uses a hand drawn graph (Fig 1.1) shown in the Introduction section of my lab report.
# In this driver the graph is created then drawn to a new window, and each color conflict is printed
# to the terminal.
#
# Generative AI disclosure:
# ChatGPT was used as a learning/debugging aid for Python syntax, NetworkX/Matplotlib visualization,
# code organization & troubleshooting. Any AI-assisted suggestions integrated into my code were
# reviewed and modified by me before inclusion.

import networkx as nx
import matplotlib.pyplot as plt
import random

#//////////////////////#
# HELPER FUNCTIONS
#\\\\\\\\\\\\\\\\\\\\\\#

# build_graph:
# Initializes a NetworkX graph with connected edges modeled after Fig 1.1, as shown
# in the Introduction section of the lab report. Also produces a random assignment of
# colors for each node in the graph, as a dictionary.
# Returns both the NetworkX graph and the dictionary of color assignments.
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

    # generate random colors for each node
    available_colors = ("red","green","blue")
    color_dictionary = {}
    for node in G.nodes:
         color_dictionary[node] = random.choice(available_colors)

    return G, color_dictionary

# draw_graph:
# Takes a NetworkX graph and a dictionary of color assignments for each labeled
# node A-Z, and assigns positions for each node according to Fig 1.1.
# Draws the graph in a separate window.
def draw_graph(nxgraph, color_assignments, graph_title=""):

    # hardcoded/fixed positions for all 26 nodes, modeled from Fig 1.1
    positions = {
        "A": (14, 0), "B": (2, 6), "C": (0, 4), "D": (4, 4), "E": (4, 2),
        "F": (9, -2), "G": (6, 6), "H": (2, 0), "I": (6, 2), "J": (10, 4),
        "K": (8, 0), "L": (4, 6), "M": (11, -2), "N": (12, 6), "O": (14, -2),
        "P": (14, 4), "Q": (10, 6), "R": (0, 0), "S": (4, 0), "T": (10, 0),
        "U": (10, 2), "V": (8, 4), "W": (6, -2), "X": (12, 2), "Y": (2, 2),
        "Z": (0, 2)
    }

    # display colors used for red/blue/green (better contrast for red-green accessibility)
    display_color_map = {
        "red": "#D55E00",
        "green": "#009E73",
        "blue": "#0072B2"
    }

    # convert logical color assignments to display colors in NetworkX node order
    node_colors = [
        display_color_map[color_assignments[node]]
        for node in nxgraph.nodes
    ]

    # create Matplotlib figure & axes for the NetworkX graph
    fig, ax = plt.subplots(figsize=(8,5))

    # draw NetworkX graph onto axis
    nx.draw(
        nxgraph,
        pos=positions,
        with_labels=True,
        font_color="white",
        font_size=10,
        font_weight="bold",
        node_color=node_colors,
        node_size=500,
        edgecolors="white",
        edge_color="white",
        width=2,
        ax=ax
    )

    # customize graph title & appearance
    ax.set_title(
        graph_title,
        fontsize=16,
        color="white",
        fontweight="bold",
        pad=22
    )

    # subtitle
    ax.text(
        0.5, 1.02,
        "26 Nodes (A-Z), 43 Edges",
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        color="#d0d0d0",
        fontsize=10
    )

    ax.set_facecolor("#1f1f1f")
    fig.set_facecolor("#1f1f1f")

    plt.show()


#//////////////////////#
# MAIN DRIVER
#\\\\\\\\\\\\\\\\\\\\\\#

def main():

    # create NetworkX graph with random color assignments
    nxgraph, color_assignments = build_graph()

    # print color assignments to terminal
    for node in color_assignments:
         print(f"{node} = {color_assignments[node]}")

    # Check for conflict and print each one
    i = 1
    for u, v in nxgraph.edges:
        if (color_assignments[u] == color_assignments[v]):
            print(f"[{i}] conflict {color_assignments[u].upper()}: {u} <=> {v}")
            i+=1
    
    # print graph
    draw_graph(nxgraph, color_assignments,"Randomized Initial State")

    return




# main guard: run main() function as driver
if __name__ == "__main__":
    main()
