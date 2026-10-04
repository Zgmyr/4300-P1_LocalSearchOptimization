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
# This project uses a fixed hand-drawn graph (Fig 1.1) from the lab report as a graph-coloring
# optimization problem. The program generates randomized initial color assignments, evaluates
# states using the number of conflicting edges, applies local-search algorithms, and visualizes
# initial/result states using NetworkX and Matplotlib.
#
# Generative AI disclosure:
# ChatGPT was used as a learning/debugging aid for Python syntax, NetworkX/Matplotlib visualization,
# code organization & troubleshooting. Any AI-assisted suggestions integrated into my code were
# reviewed and modified by me before inclusion.

import networkx as nx
import matplotlib.pyplot as plt
import random
import time




#////////////////////////////////////////////////////////////////////////////////////////////////////#
#                            GRAPH CONSTRUCTION GLOBAL VARIABLES
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\#

# graph positions & edges are hardcoded, modeled after Fig 1.1 from the lab report
GRAPH_POSITIONS = {
    "A": (14, 0), "B": (2, 6), "C": (0, 4), "D": (4, 4), "E": (4, 2),
    "F": (9, -2), "G": (6, 6), "H": (2, 0), "I": (6, 2), "J": (10, 4),
    "K": (8, 0), "L": (4, 6), "M": (11, -2), "N": (12, 6), "O": (14, -2),
    "P": (14, 4), "Q": (10, 6), "R": (0, 0), "S": (4, 0), "T": (10, 0),
    "U": (10, 2), "V": (8, 4), "W": (6, -2), "X": (12, 2), "Y": (2, 2),
    "Z": (0, 2)
}

GRAPH_EDGES = [
    ("A","O"), ("A","X"), ("B","C"), ("B","D"), ("B","L"), ("C","Y"),
    ("C","Z"), ("D","E"), ("D","G"), ("D","I"), ("D","Y"), ("E","I"),
    ("E","S"), ("E","Y"), ("F","K"), ("F","M"), ("F","T"), ("F","W"),
    ("G","L"), ("G","Q"), ("H","R"), ("H","S"), ("H","Y"), ("I","K"),
    ("I","S"), ("I","V"), ("J","Q"), ("J","U"), ("J","V"), ("K","T"),
    ("K","U"), ("K","W"), ("M","O"), ("M","T"), ("N","P"), ("N","Q"),
    ("P","X"), ("R","Y"), ("R","Z"), ("S","W"), ("T","U"), ("T","X"),
    ("U","X")
]

# display colors used for red/blue/green (better contrast for red-green accessibility)
DISPLAY_COLOR_MAP = {
    "red": "#D55E00",
    "green": "#009E73",
    "blue": "#0072B2"
}




#////////////////////////////////////////////////////////////////////////////////////////////////////#
#                            GRAPHING FUNCTIONS
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\#


# build_graph:
# Initializes and returns the fixed NetworkX graph used for the project.
# Node labels A-Z are added to the graph, and the hardcoded edge list is
# loaded from the global GRAPH_EDGES definition modeled after Fig 1.1.
# Also generates and returns a randomized red/green/blue color assignment
# dictionary for all 26 nodes.
def build_graph():
    # construct a NetworkX undirected graph with nodes A-Z
    G = nx.Graph()
    G.add_nodes_from("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    # 43 total hardcoded edges, defined globally
    G.add_edges_from(GRAPH_EDGES)

    # generate random colors for each node
    available_colors = ("red","green","blue")
    color_dictionary = {}
    for node in G.nodes:
         color_dictionary[node] = random.choice(available_colors)

    return G, color_dictionary

# draw_graph:
# Displays a single graph-coloring state in a separate Matplotlib window.
# Uses the globally defined GRAPH_POSITIONS and DISPLAY_COLOR_MAP values
# to draw the fixed graph layout and accessible display colors.
# Displays the provided graph title, graph metadata, and objective-function value
def draw_graph(nxgraph, color_assignment, objective_val, graph_title=""):

    # convert logical color assignments to display colors in NetworkX node order
    node_colors = [
        DISPLAY_COLOR_MAP[color_assignment[node]]
        for node in nxgraph.nodes
    ]

    # create Matplotlib figure & axes for the NetworkX graph
    fig, ax = plt.subplots(figsize=(8,5))

    # draw NetworkX graph onto axis, using positions defined globally
    nx.draw(
        nxgraph,
        pos=GRAPH_POSITIONS,
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

# draw_graph_comparison
# Displays a randomized initial coloring and an algorithm-result coloring
# side-by-side in the same Matplotlib window for direct comparison.
# Uses the globally defined GRAPH_POSITIONS and DISPLAY_COLOR_MAP values.
# Accepts the algorithm's resulting metadata dictionary to obtain the initial
# and final objective-function values and support display of search statistics.
# Displays a configurable title for the algorithm result.
def draw_graph_comparison(nxgraph, initial_assignments,
                          result_assignments, metadata, result_title):
    
    # convert logical color assignments to display colors in NetworkX node order
    initial_node_colors = [
        DISPLAY_COLOR_MAP[initial_assignments[node]]
        for node in nxgraph.nodes
    ]

    result_node_colors = [
        DISPLAY_COLOR_MAP[result_assignments[node]]
        for node in nxgraph.nodes
    ]

    # create side-by-side Matplotlib axes
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # draw randomized initial state
    nx.draw(
        nxgraph,
        pos=GRAPH_POSITIONS,
        with_labels=True,
        font_color="white",
        font_size=10,
        font_weight="bold",
        node_color=initial_node_colors,
        node_size=500,
        edgecolors="white",
        edge_color="white",
        width=2,
        ax=axes[0]
    )

    # draw algorithm result
    nx.draw(
        nxgraph,
        pos=GRAPH_POSITIONS,
        with_labels=True,
        font_color="white",
        font_size=10,
        font_weight="bold",
        node_color=result_node_colors,
        node_size=500,
        edgecolors="white",
        edge_color="white",
        width=2,
        ax=axes[1]
    )

    # data used to customize each side of the comparison
    graph_data = [
        (axes[0], "Randomized Initial State", metadata["init_objval"]),
        (axes[1], result_title, metadata["final_objval"])
    ]

    # apply titles, graph information, objective values, and appearance
    for ax, graph_title, objective_val in graph_data:

        ax.set_title(
            graph_title,
            fontsize=16,
            color="white",
            fontweight="bold",
            pad=22
        )

        # display graph structure below title
        ax.text(
            0.5, 1.02,
            "26 Nodes (A-Z), 43 Edges",
            transform=ax.transAxes,
            ha="center",
            va="bottom",
            color="#d0d0d0",
            fontsize=10
        )

        # display objective function value below graph
        ax.text(
            0.5, -0.05,
            f"f(state) = {objective_val} conflicting edges",
            transform=ax.transAxes,
            ha="center",
            va="top",
            color="white",
            fontsize=14,
            fontweight="bold"
        )

        # display runtime below the result objective value
        axes[1].text(
            0.5, -0.11,
            f"Runtime: {metadata['runtime'] * 1000:.3f} ms",
            transform=axes[1].transAxes,
            ha="center",
            va="top",
            color="#d0d0d0",
            fontsize=10
        )

        ax.set_facecolor("#1f1f1f")

    # customize overall figure appearance
    fig.set_facecolor("#1f1f1f")

    # provide room for titles and objective-value labels
    fig.subplots_adjust(
        bottom=0.14,
        top=0.88,
        wspace=0.12
    )

    plt.show()




#////////////////////////////////////////////////////////////////////////////////////////////////////#
#                            LOCAL SEARCH ALGORITHMS
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\#


# get_objective_value
# Given a NetworkX graph & a complete color-assignment dictionary (node:color for nodes A-Z),
# evaluates the state globally by checking every graph edge for same-color endpoints.
# Returns the total number of conflicting edges as the objective-function value.
def get_objective_value(nxgraph, color_assignments):
    edge_conflicts = 0

    # count the number of conflicting edges for same-color assignment
    for endpt1, endpt2 in nxgraph.edges:
        if (color_assignments[endpt1] == color_assignments[endpt2]):
            edge_conflicts += 1

    return edge_conflicts

# find_steepest_neighbor
# Examines every possible one-node recoloring from the current state and
# returns the strictly improving neighboring move with the lowest objective value.
# Candidate objective values are calculated locally using the change in conflicts
# on edges incident to the recolored node rather than recounting all graph edges.
# Also counts how many candidate neighboring states are evaluated during the search.
# Returns (node, new_color), the resulting objective value, and the number of
# candidate states evaluated. If no strictly improving neighbor exists, returns
# None, the current objective value, and the number of candidates evaluated.
def find_steepest_neighbor(nxgraph, color_assignments, cur_objval):

    # best assignment (node, color) + objective function value among neighboring states
    steepest_assignment = None
    steepest_objval = cur_objval

    candidates_considered = 0
    
    allowed_colors = ("red", "blue", "green")

    
    # consider each and every possible node recoloring (neighboring states)
    for node in nxgraph.nodes:

        # get nodes adjacent to this node
        neighboring_nodes = tuple(nxgraph.neighbors(node))

        # count current edge conflicts incident to this node
        old_node_edge_conflicts = 0
        for neighbor_node in neighboring_nodes:
            if color_assignments[node] == color_assignments[neighbor_node]:
                old_node_edge_conflicts += 1

        # determine what other colors the node may be assigned
        choice_colors = []
        for new_color in allowed_colors:
            if new_color == color_assignments[node]:
                continue
            choice_colors.append(new_color)

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

            # increment candidate states considered
            candidates_considered += 1

            # store best-so-far objective function value
            if candidate_objval < steepest_objval:
                steepest_assignment = (node, new_color)
                steepest_objval = candidate_objval
                
                # stop early if a goal state with 0 conflicting edges is found
                if steepest_objval == 0:
                    return steepest_assignment, steepest_objval, candidates_considered

    # return steepest improving neighboring assignment + objective value
    return steepest_assignment, steepest_objval, candidates_considered

# steepest_hill_climbing
# Performs steepest hill climbing from the provided randomized initial state.
# A copy of the initial color assignments is repeatedly updated by applying
# the best strictly improving move returned by find_steepest_neighbor().
# Search terminates when a goal state with 0 conflicts is reached or when
# no strictly improving neighboring state exists.
# Collects metadata including initial/final objective values, number of state
# transitions, total candidate states evaluated, whether the goal was reached,
# and total algorithm runtime.
# Returns the final color assignments and the metadata dictionary.
def steepest_hill_climbing(nxgraph, init_color_assignments, init_objval):
    # container to store resulting metadata for steepest hill climbing
    metadata = {
        "init_objval": init_objval,
        "final_objval": init_objval,
        "transitions": 0,
        "candidate_states_evaluated": 0,
        "goal_reached": False,
        "runtime": 0.0
    }

    # start runtime counter
    start_time = time.perf_counter()

    # create a copy of initial state {node:color} assignments
    current_assignments = init_color_assignments.copy()
    current_objval = init_objval

    # early check if initial state == goal state (0 conflicting edges)    
    if init_objval == 0:
        metadata["goal_reached"] = True
        metadata["runtime"] = time.perf_counter() - start_time
        return current_assignments, metadata

    # transition to neighboring states until no further improvement in objective value
    is_still_climbing = True
    
    while is_still_climbing:
        # find the steepest improving neighboring assignment, if one exists
        neighbor_node_assignment, current_objval, candidates_evaluated = find_steepest_neighbor(
            nxgraph,
            current_assignments,
            current_objval)

        # update metadata with candidates considered
        metadata["candidate_states_evaluated"] += candidates_evaluated

        # check if better neighboring state was found
        if neighbor_node_assignment is not None:

            # apply move to neighboring state
            reassigned_node, reassigned_color = neighbor_node_assignment
            current_assignments[reassigned_node] = reassigned_color

            # increment transition in metadata after applying move
            metadata["transitions"] += 1

            # stop if goal state (0 edge conflicts) is reached
            if current_objval == 0:
                is_still_climbing = False
                metadata["goal_reached"] = True
        else:
            # stop if no strictly improving neighboring state can be found
            is_still_climbing = False

    # end runtime counter and update metadata
    metadata["final_objval"] = current_objval
    metadata["runtime"] = time.perf_counter() - start_time

    # return final color assignments + resulting search metadata
    return current_assignments, metadata

    

#////////////////////////////////////////////////////////////////////////////////////////////////////#
#                            MAIN DRIVER
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\#

def main():

    # create NetworkX graph with random color assignments
    nxgraph, init_assignments = build_graph()

    # get initial objective function value
    init_objval = get_objective_value(nxgraph, init_assignments)
    print(f"f(initial)={init_objval}")
    
    # draw the initial randomized state
    draw_graph(nxgraph, init_assignments, init_objval,"Randomized Initial State")

    # run steepest hill climbing
    shc_assignments, shc_metadata = steepest_hill_climbing(nxgraph, init_assignments, init_objval)
    print(f"f(hill)={shc_metadata["final_objval"]}")
    print(f"Hill climbing runtime: {shc_metadata["runtime"] * 1000:.3f} ms")

    # draw the steepest hill climbing result as comparison
    draw_graph_comparison(nxgraph, init_assignments,
                          shc_assignments, shc_metadata,
                          "Steepest Hill Climbing Result")

    return




# main guard: run main() function as driver
if __name__ == "__main__":
    main()
