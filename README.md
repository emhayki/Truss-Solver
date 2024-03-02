
## Description

The 2D Truss Problem Solver is a Python-based graphical user interface (GUI) application designed to simplify the analysis of 2D truss structures. It provides an intuitive platform for inputting truss configurations and loads, conducting calculations, and visualising the resulting forces and deformations.

## Features

- Interactive GUI for straightforward input and modification of truss configurations
- Visualisation of truss structures and results
- Calculation of nodal displacements and member forces
- Results presented in a clear, tabular format

## Installation

To run the 2D Truss Problem Solver, Python must be installed on your system, along with several dependencies.

### Prerequisites

- Python 3.x
- `numpy`
- `matplotlib`
- `tkinter` (should be included with Python)

### Usage
- Input the geometry of the truss structure, including nodes and members.
- Specify loads and boundary conditions.
- Run the analysis to calculate nodal displacements and member forces.
- View the resulting analysis.

## Example Usage

The example below demonstrates how to analyse a truss with the 2D Truss Problem Solver.

**Step 1: Configure Truss Geometry**
Enter the total number of nodes and elements. For each element, input the start node (S.N), end node (E.N), modulus of elasticity (E), and cross-sectional area (A). For nodes, provide their coordinates on the X and Y axes.

**Step 2: Apply Loads and Constraints**
Define nodes that have prescribed displacements with values along the X and Y axes. For point loads, specify the node number and the load magnitude on the X and Y axes.

<img width="1072" alt="t1" src="https://github.com/emhayki/Truss-Solver/assets/135982304/89d0342a-77e6-4b34-ac09-fc6d414b4254">

**Step 3: Perform Analysis**
Move to the 'Calculation' tab to calculate the global stiffness matrix, displacements, reactions, and element stresses.

<img width="1028" alt="t2" src="https://github.com/emhayki/Truss-Solver/assets/135982304/1a200659-8e25-42c3-b020-266746e9a9a8">

**Step 4: Visualise Truss**
Navigate to the 'Figure' tab to view the structure. It displays nodes, elements, applied displacements, and point loads.
<img width="1072" alt="t3" src="https://github.com/emhayki/Truss-Solver/assets/135982304/5b96dc53-6685-48f2-9593-126dd4bb34bb">

