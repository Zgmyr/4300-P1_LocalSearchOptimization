# Zachary Gmyr
# 10.02.2026
#
# Built using Python v3.12 (IDE: VSCode)
# Required Packages: networkx, matplotlib, random
# run as needed: python -m pip install networkx matplotlib random
#
# CMP SCI 4300 - Intro to AI
# Main driver for project 1: Local search & optimization for a graph coloring problem
#
# This project uses a hand drawn graph (Fig 1.1) shown in the Introduction section of my lab report.
# In this driver the graph is created then drawn to a new window, and each color conflict is printed
# to the terminal.

import networkx as nx
import matplotlib.pyplot as plt
import random

#//////////////////////#
# HELPER FUNCTIONS
#\\\\\\\\\\\\\\\\\\\\\\#

# build_graph:
# initializes a NetworkX graph with connected edges modeled after Fig 1.1, as shown
# in the Introduction section of the lab report. Also produces a random assignment of
# colors for each node in the graph, as a dictionary.
# returns both the NetworkX graph and the dictionary of color assignments.
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
# takes a NetworkX graph and a dictionary of color assignments for each labeled
# node A-Z, and assigns positions for each node according to Fig 1.1.
# draws the graph in a separate window.
def draw_graph(nxgraph, color_dictionary):

    # hardcoded/fixed positions for all 26 nodes, modeled from Fig 1.1
    positions = {
        "A": (14, 0), "B": (2, 6), "C": (0, 4), "D": (4, 4), "E": (4, 2),
        "F": (9, -2), "G": (6, 6), "H": (2, 0), "I": (6, 2), "J": (10, 4),
        "K": (8, 0), "L": (4, 6), "M": (11, -2), "N": (12, 6), "O": (14, -2),
        "P": (14, 4), "Q": (10, 6), "R": (0, 0), "S": (4, 0), "T": (10, 0),
        "U": (10, 2), "V": (8, 4), "W": (6, -2), "X": (12, 2), "Y": (2, 2),
        "Z": (0, 2)
    }

    # build list of colors from dictionary, mapped to each node in NetworkX graph
    node_colors = [color_dictionary[node] for node in nxgraph.nodes]

    nx.draw(
        nxgraph,
        pos=positions,
        with_labels=True,
        font_color="white",
        node_color=node_colors
    )

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
    draw_graph(nxgraph, color_assignments)

    return




# main guard: run main() function as driver
if __name__ == "__main__":
    main()
