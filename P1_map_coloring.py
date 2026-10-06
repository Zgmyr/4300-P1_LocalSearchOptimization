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
import math
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

# colors allowed for assignment as used by local search algorithms
ALLOWED_COLORS = (
    "red",
    "blue",
    "green"
)




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


# _draw_graph_state:
# Internal helper used by draw_graph() to render one graph-coloring state
# onto a supplied Matplotlib axis. Uses the globally defined GRAPH_POSITIONS
# and DISPLAY_COLOR_MAP values and displays the graph title, structure,
# and objective-function value.
def _draw_graph_state(ax, nxgraph, color_assignments, objective_val, graph_title):

    # convert logical color assignments to display colors in NetworkX node order
    node_colors = [
        DISPLAY_COLOR_MAP[color_assignments[node]]
        for node in nxgraph.nodes
    ]

    # draw NetworkX graph onto supplied axis
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

    # display graph title
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

    # display objective-function value below graph
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

    # set graph background
    ax.set_facecolor("#1f1f1f")


# draw_graph:
# Displays either a single graph-coloring state or a side-by-side comparison
# between an initial state and an algorithm-result state.
# If result_assignments is not supplied, draws only the initial state using
# the provided objective value and graph title.
# If result_assignments is supplied, metadata provides the initial/final
# objective values and runtime for the comparison display.
def draw_graph(nxgraph, initial_assignments, objective_val=None,
               result_assignments=None, metadata=None, graph_title=""):

    # single-state display
    if result_assignments is None:

        fig, ax = plt.subplots(figsize=(8, 5))

        _draw_graph_state(
            ax,
            nxgraph,
            initial_assignments,
            objective_val,
            graph_title
        )

        fig.set_facecolor("#1f1f1f")

        # provide room for title and objective-value label
        fig.subplots_adjust(
            bottom=0.14,
            top=0.88
        )

    # initial vs. algorithm-result comparison
    else:

        # comparison requires search metadata
        if metadata is None:
            raise ValueError(
                "metadata must be provided when drawing a result comparison"
            )

        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        # draw randomized initial state
        _draw_graph_state(
            axes[0],
            nxgraph,
            initial_assignments,
            metadata["init_objval"],
            "Randomized Initial State"
        )

        # draw algorithm result
        _draw_graph_state(
            axes[1],
            nxgraph,
            result_assignments,
            metadata["final_objval"],
            graph_title
        )

        # display algorithm runtime below result objective value
        axes[1].text(
            0.5, -0.11,
            f"Runtime: {metadata['runtime'] * 1000:.3f} ms",
            transform=axes[1].transAxes,
            ha="center",
            va="top",
            color="#d0d0d0",
            fontsize=10
        )

        fig.set_facecolor("#1f1f1f")

        # provide room for titles, objective values, and runtime
        fig.subplots_adjust(
            bottom=0.18,
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


# _evaluate_recolor
# Evaluates one candidate node recoloring using the change in conflicts on
# edges incident to that node rather than recounting all graph edges.
# Returns the neighboring state's objective value.
def _evaluate_recolor(nxgraph, current_assignments, cur_objval, candidate_node, candidate_color):

    old_node_edge_conflicts = 0
    new_node_edge_conflicts = 0

    # check the nodes incident to candidate node
    for neighbor_node in nxgraph.neighbors(candidate_node):

        # count edge conflicts for candidate node with current color assignment
        if current_assignments[candidate_node] == current_assignments[neighbor_node]:
            old_node_edge_conflicts += 1
        
        # count edge conflicts if candidate node is assigned the candidate color
        if candidate_color == current_assignments[neighbor_node]:
            new_node_edge_conflicts += 1

    # compute objective value of neighboring state with candidate node recoloring
    delta_recolor_conflicts = old_node_edge_conflicts - new_node_edge_conflicts
    neighbor_objval = cur_objval - delta_recolor_conflicts

    return neighbor_objval


# _find_steepest_neighbor
# Evaluates every one-node recoloring and finds the lowest objective value
# among strictly improving neighbors. Ties at the steepest objective are
# broken randomly. Returns the selected (node, new_color), resulting objective
# value, and number of candidates evaluated; returns None if no improvement exists.
def _find_steepest_neighbor(nxgraph, current_assignments, cur_objval):

    # track all recolorings tied for the steepest improving objective value
    steepest_candidates = []
    steepest_objval = cur_objval

    # count how many neighboring candidate states are evaluated
    candidates_considered = 0
    
    # examine every possible one-node recoloring
    for node in nxgraph.nodes:

        # determine the two alternative colors available for this node
        choice_colors = [color for color in ALLOWED_COLORS
                         if color != current_assignments[node]]

        # evaluate each possible recoloring of this node
        for new_color in choice_colors:

            # compute objective value produced by this candidate recoloring
            candidate_objval = _evaluate_recolor(
                nxgraph,
                current_assignments,
                cur_objval,
                node,
                new_color
            )

            # increment number of candidate neighboring states evaluated
            candidates_considered += 1

            # check if candidate value is better than steepest-so-far
            if candidate_objval < steepest_objval:
                # discard previous steepest candidates and store new steepest candidate
                steepest_candidates.clear()
                steepest_candidates.append((node, new_color))
                steepest_objval = candidate_objval

            # check if candidate ties with steepest-so-far
            elif candidate_objval == steepest_objval and candidate_objval < cur_objval:
                # record equally steep improving candidates for random tie-breaking
                steepest_candidates.append((node,new_color))

    # return either a steepest improving candidate, or None if one does not exist
    if steepest_candidates:
        # randomly choose among equally steep improving neighbors
        return random.choice(steepest_candidates), steepest_objval, candidates_considered
    else:
        # no strictly improving neighboring state exists
        return None, cur_objval, candidates_considered


# steepest_hill_climbing
# Repeatedly applies a steepest strictly improving recoloring from the
# provided initial state, with random tie-breaking among equally steep moves.
# Stops at a goal state or when no strictly improving neighbor exists.
# Returns the final assignments and search metadata.
def steepest_hill_climbing(nxgraph, init_color_assignments, init_objval):

    # initialize search metadata
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

    # create a copy of the initial state and objective value
    current_assignments = init_color_assignments.copy()
    current_objval = init_objval

    # return immediately if the initial state is already a goal 
    if init_objval == 0:
        metadata["goal_reached"] = True
        metadata["runtime"] = time.perf_counter() - start_time
        return current_assignments, metadata

    # continue until a goal is reached or no improving neighboring move exists
    is_still_climbing = True
    
    while is_still_climbing:
        # find the steepest improving neighboring assignment, if one exists
        neighbor_assignment, current_objval, candidates_evaluated = _find_steepest_neighbor(
            nxgraph,
            current_assignments,
            current_objval
        )

        # accumulate candidate states evaluated
        metadata["candidate_states_evaluated"] += candidates_evaluated

        # process the returned neighboring move, if one exists
        if neighbor_assignment is not None:

            # apply the selected recoloring
            reassigned_node, reassigned_color = neighbor_assignment
            current_assignments[reassigned_node] = reassigned_color

            # record the state transition
            metadata["transitions"] += 1

            # stop if a goal state is reached
            if current_objval == 0:
                is_still_climbing = False
                metadata["goal_reached"] = True

        # stop if no strictly improving neighboring state can be found
        else:
            is_still_climbing = False

    # record final objective value and runtime
    metadata["final_objval"] = current_objval
    metadata["runtime"] = time.perf_counter() - start_time

    # return final state and search metadata
    return current_assignments, metadata


# _find_sideways_neighbor
# Finds a steepest improving recoloring, randomly breaking ties.
# If no improvement exists and sideways movement is permitted, randomly
# selects an equal-objective neighbor. Returns the move, objective value,
# and number of candidate states evaluated, or None if no valid move exists.
def _find_sideways_neighbor(nxgraph, current_assignments, cur_objval, is_sideways_valid):

    # track all recolorings tied for the steepest improving objective value
    steepest_candidates = []
    steepest_objval = cur_objval

    # track equal-objective recolorings available for sideways movement
    sideways_candidates = []

    # count how many neighboring candidate states are evaluated
    candidates_considered = 0

    # examine every possible one-node recoloring
    for node in nxgraph.nodes:

        # determine the two alternative colors available for this node
        choice_colors = [color for color in ALLOWED_COLORS
                        if color != current_assignments[node]]

        # evaluate each possible recoloring of this node
        for new_color in choice_colors:

            # compute objective value produced by this candidate recoloring
            candidate_objval = _evaluate_recolor(
                nxgraph,
                current_assignments,
                cur_objval,
                node,
                new_color
            )

            # increment number of candidate neighboring states evaluated
            candidates_considered += 1

            # check if candidate value is better than steepest-so-far
            if candidate_objval < steepest_objval:
                # discard previous candidates and store new steepest candidate
                steepest_candidates.clear()
                steepest_candidates.append((node,new_color))
                steepest_objval = candidate_objval

                # discard sideways candidates after an improving move is found
                sideways_candidates.clear()
                is_sideways_valid = False

            # check if candidate ties with steepest-so-far
            elif candidate_objval == steepest_objval and candidate_objval < cur_objval:
                # record equally steep improving candidates for random tie-breaking
                steepest_candidates.append((node,new_color))

            # check if candidate is a sideways move for the current state
            elif is_sideways_valid and candidate_objval == cur_objval:
                # record equal-objective candidate for possible sideways movement
                sideways_candidates.append((node,new_color))
                
    # prefer a steepest improving neighbor
    if steepest_candidates:
        # randomly choose among equally steep improving neighbors
        return random.choice(steepest_candidates), steepest_objval, candidates_considered
    
    # otherwise return a sideways move if available
    elif sideways_candidates:
        # randomly choose among sideways neighbors
        return random.choice(sideways_candidates), cur_objval, candidates_considered

    # no improving or permitted sideways neighbor exists
    else:
        return None, cur_objval, candidates_considered


# sideways_hill_climbing
# Performs steepest hill climbing while permitting a limited number of
# consecutive sideways moves. Improving moves reset the sideways allowance.
# Stops at a goal state or when no permitted move exists, and returns the
# final assignments with search metadata.
def sideways_hill_climbing(nxgraph, init_color_assignments, init_objval, consecutive_sideways_limit):

    # initialize search metadata
    metadata = {
        "init_objval": init_objval,
        "final_objval": init_objval,
        "transitions": 0,
        "candidate_states_evaluated": 0,
        "goal_reached": False,
        "runtime": 0.0,
        "consecutive_sideways_limit": consecutive_sideways_limit,
        "sideways_moves": 0
    }

    # start runtime counter
    start_time = time.perf_counter()

    # create a copy of the initial state and objective value
    current_assignments = init_color_assignments.copy()
    current_objval = init_objval

    # initialize remaining consecutive sideways moves
    sideways_remaining = consecutive_sideways_limit

    # return immediately if the initial state is already a goal
    if init_objval == 0:
        metadata["goal_reached"] = True
        metadata["runtime"] = time.perf_counter() - start_time
        return current_assignments, metadata

    # continue until a goal is reached or no permitted neighboring move exists
    is_still_climbing = True
    
    while is_still_climbing:

        # allow sideways movement while consecutive moves remain
        is_sideways_valid = sideways_remaining > 0

        # find a steepest improving neighbor or permitted sideways neighbor
        neighbor_assignment, new_objval, candidates_evaluated = _find_sideways_neighbor(
            nxgraph,
            current_assignments,
            current_objval,
            is_sideways_valid
        )

        # accumulate candidate states evaluated
        metadata["candidate_states_evaluated"] += candidates_evaluated

        # process the returned neighboring move, if one exists
        if neighbor_assignment is not None:

            # handle an equal-objective sideways move
            if new_objval == current_objval:
                
                # record sideways move and consume one consecutive allowance
                metadata["sideways_moves"] += 1
                sideways_remaining -= 1

            # handle a strictly improving move
            elif new_objval < current_objval:

                # update objective value and reset consecutive sideways allowance
                current_objval = new_objval
                sideways_remaining = consecutive_sideways_limit

            # apply the selected recoloring
            reassigned_node, reassigned_color = neighbor_assignment
            current_assignments[reassigned_node] = reassigned_color

            # record the state transition
            metadata["transitions"] += 1

            # stop if a goal state is reached
            if current_objval == 0:
                is_still_climbing = False
                metadata["goal_reached"] = True

        # stop when no improving or permitted sideways neighbor exists
        else:
            is_still_climbing = False

    # record final objective value and runtime
    metadata["final_objval"] = current_objval
    metadata["runtime"] = time.perf_counter() - start_time

    # return final state and search metadata
    return current_assignments, metadata

# _cooling_schedule
# Computes the simulated-annealing temperature for a given iteration using
# either a linear or geometric cooling schedule. Returns 0 once the scheduled
# temperature reaches the fixed minimum cutoff of 0.1.
def _cooling_schedule(iteration, cooling_strategy, init_temp, cooling_rate):

    # initialize temperature and minimum temperature cutoff
    temperature = 0.0
    cutoff_temp = 0.1

    # LINEAR cooling schedule: T(t)=T0-(rate * t)
    if cooling_strategy == "linear":
        temperature = init_temp - (cooling_rate * iteration)

    # GEOMETRIC cooling schedule: T(t)=T0*(rate)^t
    elif cooling_strategy == "geometric":
        temperature = init_temp * (cooling_rate ** iteration)

    # return 0 when the scheduled temperature reaches the cutoff
    if temperature <= cutoff_temp:
        temperature = 0

    return temperature

# simulated_annealing
# Repeatedly samples one random neighboring recoloring and accepts improving
# or equal moves, while worse moves may be accepted based on temperature.
# Stops at a goal state or when the cooling schedule terminates, and returns
# the final assignments with search metadata.
def simulated_annealing(nxgraph, init_color_assignments, init_objval, cooling_strategy, init_temp, cooling_rate):

    # initialize search metadata
    metadata = {
        "init_objval": init_objval,
        "final_objval": init_objval,
        "transitions": 0,
        "candidate_states_evaluated": 0,
        "goal_reached": False,
        "runtime": 0.0,
        "cooling_strategy": cooling_strategy,
        "initial_temp": init_temp,
        "cooling_rate": cooling_rate,
        "worse_moves_considered": 0,
        "worse_moves_accepted": 0
    }

    # start runtime counter
    start_time = time.perf_counter()

    # create a copy of the initial state and objective value
    current_assignments = init_color_assignments.copy()
    current_objval = init_objval

    # initialize current temperature to initial temperature
    current_temp = init_temp

    # return immediately if the initial state is already a goal
    if init_objval == 0:
        metadata["goal_reached"] = True
        metadata["runtime"] = time.perf_counter() - start_time
        return current_assignments, metadata
    
    # continue until a goal is reached or the cooling schedule terminates
    current_iteration = 0

    while True:

        # compute temperature for the current iteration
        current_temp = _cooling_schedule(
            current_iteration,
            cooling_strategy,
            init_temp,
            cooling_rate
        )

        # stop when the cooling schedule returns 0
        if current_temp == 0:
            break

        # randomly choose one candidate neighboring state
        candidate_node = random.choice(list(nxgraph.nodes))
        choice_colors = [color for color in ALLOWED_COLORS
                         if color != current_assignments[candidate_node]]
        candidate_color = random.choice(choice_colors)

        # compute objective value produced by this random candidate recoloring
        candidate_objval = _evaluate_recolor(
            nxgraph,
            current_assignments,
            current_objval,
            candidate_node,
            candidate_color
        )

        # accumulate candidate states evaluated
        metadata["candidate_states_evaluated"] += 1

        # compute objective difference; positive is improving, zero is equal, negative is worse
        delta_objval = current_objval - candidate_objval

        # determine if the move is accepted
        is_move_accepted = False

        # always accept strictly improving moves
        if delta_objval > 0:
            is_move_accepted = True

        # always accept equal-objective moves
        elif delta_objval == 0:
            is_move_accepted = True
        
        # consider worse moves using temperature-dependent acceptance probability
        else:
            # record worse candidate considered
            metadata["worse_moves_considered"] += 1

            # compute probability of accepting the worse move
            probability_accept_move = math.e ** (delta_objval / current_temp)

            if random.random() <= probability_accept_move:
                # permit worse move and record its acceptance
                is_move_accepted = True
                metadata["worse_moves_accepted"] += 1

        # apply the candidate move if accepted
        if is_move_accepted:
            
            # apply the selected recoloring and update objective value
            current_assignments[candidate_node] = candidate_color
            current_objval = candidate_objval
            
            # record the state transition
            metadata["transitions"] += 1

            # stop if a goal state is reached
            if current_objval == 0:
                metadata["goal_reached"] = True
                break

        # increment iteration and continue
        current_iteration += 1

    # record final objective value and runtime
    metadata["final_objval"] = current_objval
    metadata["runtime"] = time.perf_counter() - start_time

    # return final state and search metadata
    return current_assignments, metadata




#////////////////////////////////////////////////////////////////////////////////////////////////////#
#                            MAIN DRIVER + HELPERS
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\#


def debug_display_search_metadata(search_name, metadata):
    print(f"[{search_name}]:")

    for key in metadata:
        if key != "runtime":
            print(f"  {key} = {metadata[key]}")
        else:
            print(f"  {key} = {metadata[key] * 1000:.6f} ms")


def get_simulated_annealing_parameters():

    print("""Cooling Schedules:
 1. Linear: T(t)=T0-(R * t)
 2. Geometric: T(t)=T0*(R^t)
""")

    # get cooling schedule
    cooling_sched = int(input("Select cooling schedule (1 or 2): "))
    while cooling_sched != 1 and cooling_sched != 2:
        print("Invalid cooling schedule selected")
        cooling_sched = int(input("Select cooling schedule (1 or 2): "))

    if cooling_sched == 1:
        cooling_sched = "linear"
    else:
        cooling_sched = "geometric"

    # get initial temperature
    init_temp = float(input("Enter initial temperature (> 0.1): "))
    while init_temp <= 0.1:
        print("Invalid initial temperature entered")
        init_temp = float(input("Enter initial temperature (> 0.1): "))

    # get cooling rate/factor
    if cooling_sched == "linear":
        print("NOTE: Smaller values cool more slowly and allow more iterations.")
        print("      Larger values cool more quickly.")
        cooling_rate = float(input("Enter cooling rate (R > 0): "))

        while cooling_rate <= 0:
            print("Invalid cooling rate entered")
            cooling_rate = float(input("Enter cooling rate (R > 0): "))

    else:
        print("NOTE: Values closer to 1 cool more slowly and allow more iterations.")
        print("      Smaller values cool more quickly and reduce acceptance of worse moves sooner.")
        cooling_rate = float(input("Enter cooling factor (0 < R < 1): "))

        while cooling_rate <= 0 or cooling_rate >= 1:
            print("Invalid cooling factor entered")
            cooling_rate = float(input("Enter cooling factor (0 < R < 1): "))

    return cooling_sched, init_temp, cooling_rate

def main():

    # TESTING SIMULATED ANNEALING

    results_titles = [
        "Steepest Hill Climbing Result",
        "Sideways Hill Climbing Result",
        "Simulated Annealing Result"
    ]


    # create NetworkX graph with random color assignments & get initial objective value
    nxgraph, init_assignments = build_graph()
    init_objval = get_objective_value(nxgraph, init_assignments)

    is_still_debugging = True

    while is_still_debugging:
        print("""
Search Algorithms Menu:
1. Steepest Hill Climbing
2. Sideways Hill Climbing
3. Simulated Annealing
4. Generate initial state
5. Exit""")
        search_choice = int(input(f"\nEnter option: "))

        if search_choice == 1:
            # run steepest hill climbing, print metadata, and draw results
            shc_assignments, shc_metadata = steepest_hill_climbing(
                nxgraph,
                init_assignments,
                init_objval
            )

            debug_display_search_metadata(results_titles[0], shc_metadata)

            draw_graph(
                nxgraph,
                init_assignments,
                result_assignments=shc_assignments,
                metadata=shc_metadata,
                graph_title=results_titles[0]
            )
        elif search_choice == 2:
            # NOTE TO SELF: turn this prompt into a helper function w/ validation later on
            # run sideways hill climbing, print metadata, and draw results
            sideways_moves = int(input(f"How many consecutive sideways moves?: "))
            print()

            swhc_assignments, swhc_metadata = sideways_hill_climbing(
                nxgraph,
                init_assignments,
                init_objval,
                sideways_moves
            )

            debug_display_search_metadata(results_titles[1], swhc_metadata)

            draw_graph(
                nxgraph,
                init_assignments,
                result_assignments=swhc_assignments,
                metadata=swhc_metadata,
                graph_title=results_titles[1]
            )
        elif search_choice == 3:

            # get parameters for simulated annealing search
            cooling_sched, init_temp, cooling_rate = get_simulated_annealing_parameters()
            
            # run simulated annealing, print metadata, and draw results
            sa_assignments, sa_metadata = simulated_annealing(
                nxgraph,
                init_assignments,
                init_objval,
                cooling_sched,
                init_temp,
                cooling_rate
            )

            debug_display_search_metadata(results_titles[2], sa_metadata)

            draw_graph(
                nxgraph,
                init_assignments,
                result_assignments=sa_assignments,
                metadata=sa_metadata,
                graph_title=results_titles[2]
            )

        elif search_choice == 4:
            # create NetworkX graph with random color assignments & get initial objective value
            nxgraph, init_assignments = build_graph()
            init_objval = get_objective_value(nxgraph, init_assignments)
        elif search_choice == 5:
            is_still_debugging = False
        else:
            print("invalid option")

    return




# main guard: run main() function as driver
if __name__ == "__main__":
    main()
