## Project 1: Local Search & Optimization — Graph Coloring Problem
Zachary Gmyr<br>
10/02/2026<br>
CMP-SCI 4300<br>

### Project Overview:
This project explores a *map coloring* optimization problem using a graph with 26 vertices (nodes A-Z), 43 edges, and valid color assignments of red, green, or blue. The graph was drawn first (seen in the problem introduction of the lab report) before being reconstructed as a NetworkX undirected graph.

### Python Version / Dependencies:
Python v3.12 was used, along with the `networkx` and `matplotlib` libraries.

### Project Folder Organization:

The project folder is organized as follows:

```text
Gmyr_LocalSearchProject/
├── README.md
├── P1_Local_Search_and_Optimization_Graph_Coloring.pdf
├── src/
│   ├── P1_map_coloring.py
│   └── P1_map_coloring.ipynb
└── results/
    └── [graph-result screenshots used in the report]
```

### Usage:

Two python source files were included:
1. `P1_map_coloring.py` - original development version
2. `P1_map_coloring.ipynb` - Jupyter Notebook version

Both versions contain the same program logic and should run correctly. The `.py` version was the primary version used during development and testing in Visual Studio Code.

To run the `.py` version from a terminal, navigate to the directory containing the file and execute:
```
python P1_map_coloring.py
```
The `.py` version can also be run directly from Visual Studio Code (recommended).

To run the `.ipynb` version, open the notebook in Jupyter Notebook, JupyterLab, or another compatible environment such as Visual Studio Code, then execute the code cell.

### Experiment Reproduction:

The experiments were conducted without seeding, therefore the exact results cannot be reproduced. The algorithms can still be run to see comparable results however. When executing the program a randomly generated initial state is produced. This initial coloring assignment is passed to each of the search algorithms (menu options 1-4) and reused across runs. The randomized initial state can be regenerated using option 5.

A `display_search_metadata()` helper was implemented to display all relevant search data collected per algorithm when the search is invoked from the main driver. All search algorithms track common bookkeeping information such as initial objective value, final objective value, number of transitions, candidate states evaluated, whether a goal was reached, and their runtime. This data is inclusive for `steepest_hill_climbing()`, while the other four search algorithms track additional metadata including any configured parameters passed from the driver during invocation.

All experimental configurations were listed in detail in the lab report, though a brief overview of the tests conducted are listed below.

#### Steps to Reproduce: Steep Hill Climbing

1. Select option 1 for Steepest Hill Climbing and close the results window when finished
2. Select option 5 to generate a new random initial state
3. Repeat steps 1 & 2 until obtaining the remaining 9 trial results

#### Steps to Reproduce: Sideways Hill Climbing

1. For a single trial set, first select option 1 for Steepst Hill Climbing and close the results window when finished
2. Then select option 2 for Sideways Hill Climbing and enter a consecutive sideways move limit of 1 and close the window when finished
3. Repeat step 2 for consecutive sideways limits 5, 10, and 15
4. Select option 5 to generate a new random initial state
5. Repeat steps 1-4 two more times to obtain the two other trial sets

#### Steps to Reproduce: Simulated Annealing

1. Select option 1 for Steepest Hill Climbing and close the results window when finished
2. Select option 3 for Simulated Annealing and enter 1 for a linear cooling schedule. Enter an initial temperature of 10 and a cooling rate of 0.5, then close the results window when finished
3. Repeat step 2 two more times with the same initial temperature of 10, but decrease the cooling rate to 0.2 and then 0.1
4. Repeat step 2 two more times while increasing the initial temperature to 50 and then 100 while keeping the cooling rate 0.1.
5. Select option 3 for Simulated Annealing and enter 2 for geometric cooling schedule. Enter an initial temperature of 10 and a cooling factor of 0.80, then close the results window when finished
6. Repeat step 5 two more times with the same initial temperature of 10, but increase the cooling factor to 0.90 and then 0.99
7. Repeat step 5 two more times while increasing the initial temperature to 50 and then 100 while keeping the cooling factor 0.99
8. Select option 5 to generate a new random initial state
9. Repeat steps 1-8 to obtain the linear and geometric cooling trial sets for the new initial state

#### Steps to Reproduce: Local Beam Search

1. Select option 1 for Steepest Hill Climbing and close the results window when finished
2. Select option 4 for Local Beam Search and then enter a beam size of 1. When prompted for the limit on number of beam iterations enter 50, and then close the results window when finished
3. Repeat step 2 three more times while changing the beam size to 3, then 5, then 10 to obtain the first trial set
4. Repeat steps 1-3 to obtain the remaining two trial sets