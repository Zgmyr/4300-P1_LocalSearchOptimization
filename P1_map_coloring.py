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
def draw_graph(nxgraph, color_assignment, objective_val, graph_title=""):

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
        display_color_map[color_assignment[node]]
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

    # display subtitle describing graph structure
    ax.text(
        0.5, 1.02,
        "26 Nodes (A-Z), 43 Edges",
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        color="#d0d0d0",
        fontsize=10
    )

    # display objective function value at bottom of graph
    ax.text(
        0.5, -0.05,
        f"f(state): {objective_val} conflicting edges",
        transform=ax.transAxes,
        ha="center",
        va="top",
        color="white",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_facecolor("#1f1f1f")
    fig.set_facecolor("#1f1f1f")

    plt.show()

# get_objective_value
# Given a NetworkX graph & color assignments dictionary for each node A-Z,
# counts number of coloring conflicts between endpoint nodes for each and every edge
# Returns the number of edge conflicts counted
def get_objective_value(nxgraph, color_assignments):
    edge_conflicts = 0

    # count the number of conflicting edges for same-color assignment
    for endpt1, endpt2 in nxgraph.edges:
        if (color_assignments[endpt1] == color_assignments[endpt2]):
            edge_conflicts += 1

    return edge_conflicts

def find_steepest_neighbor(nxgraph, color_assignments, cur_objval):

    # best assignment (node, color) + objective function value among neighboring states
    steepest_assignment = None
    steepest_objval = cur_objval
    
    allowed_colors = {"red", "blue", "green"}
    
    # consider each and every possible node recoloring (neighboring states)
    for node in nxgraph.nodes:

        # determine what other colors the node may be assigned
        choice_colors = allowed_colors.difference({color_assignments[node]})
        
        # get nodes adjacent to this node
        neighboring_nodes = tuple(nxgraph.neighbors(node))

        # count current edge conflicts incident to this node
        old_node_edge_conflicts = 0
        for neighbor_node in neighboring_nodes:
            if color_assignments[node] == color_assignments[neighbor_node]:
                old_node_edge_conflicts += 1

        # consider each other color assignment for this node
        for new_color in choice_colors:

            # count incident edge conflicts if this node is assigned the candidate color
            new_node_edge_conflicts = 0
            for neighbor_node in neighboring_nodes:
                if new_color == color_assignments[neighbor_node]:
                    new_node_edge_conflicts += 1

            # compute objective value of the candidate neighboring state
            delta_node_conflicts = old_node_edge_conflicts - new_node_edge_conflicts
            candidate_objval = cur_objval - delta_node_conflicts

            # store best-so-far objective function value
            if candidate_objval < steepest_objval:
                steepest_assignment = (node, new_color)
                steepest_objval = candidate_objval
                
                # stop early if a goal state with 0 conflicting edges is found
                if steepest_objval == 0:
                    return steepest_assignment, steepest_objval

    # return steepest improving neighboring assignment + objective value
    return steepest_assignment, steepest_objval

def steepest_hill_climbing(nxgraph, init_color_assignments, init_objval):
    # create a copy of initial state {node:color} assignments
    current_assignments = init_color_assignments.copy()
    current_objval = init_objval

    # transition to neighboring states until no further improvement in objective value
    is_still_climbing = True
    
    while is_still_climbing:
        # find the steepest improving neighboring assignment, if one exists (node:color assignment, new objective value)
        neighbor_node_assignment, current_objval = find_steepest_neighbor(nxgraph, current_assignments, current_objval)

        # check if better neighboring state was found
        if neighbor_node_assignment is not None:

            # apply move to neighboring state
            reassigned_node, reassigned_color = neighbor_node_assignment
            current_assignments[reassigned_node] = reassigned_color

            # stop if goal state (0 edge conflicts) is reached
            if current_objval == 0:
                is_still_climbing = False
        else:
            # stop if no strictly improving neighboring state can be found
            is_still_climbing = False

    # return final color assignments + objective value after hill climbing terminates
    return current_assignments, current_objval

    

            

#//////////////////////#
# MAIN DRIVER
#\\\\\\\\\\\\\\\\\\\\\\#

def main():

    # create NetworkX graph with random color assignments
    nxgraph, color_assignments = build_graph()

    # get initial objective function value
    init_objval = get_objective_value(nxgraph, color_assignments)
    print(f"f(initial)={init_objval}")
    
    # draw the initial randomized state
    draw_graph(nxgraph, color_assignments, init_objval,"Randomized Initial State")

    # run steepest hill climbing
    steep_hill_assignments, steep_objval = steepest_hill_climbing(nxgraph, color_assignments, init_objval)
    print(f"f(hill)={steep_objval}")
    print(f"DEBUG f(hill)={get_objective_value(nxgraph,steep_hill_assignments)}")

    # draw the steepest hill climbing result
    draw_graph(nxgraph, steep_hill_assignments, steep_objval, "Steepest Hill Climbing Result")

    return




# main guard: run main() function as driver
if __name__ == "__main__":
    main()
