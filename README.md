# Pacman AI Projects

This repository contains a playable Pacman game plus implementations and tests
for search, multi-agent, and reinforcement-learning algorithms.

## Requirements

- Python 3.11 or later
- No external packages are required for the Pacman projects

## Run the Game

Open PowerShell in the repository root:

```powershell
cd C:\Users\mthav\Downloads\Pacman
python pacman.py
```

The game starts with keyboard control, ghosts, food, and a randomly selected
classic map. Run the command again to select another map.

Useful gameplay options:

```powershell
# Play several random classic maps
python pacman.py --randomMaps -n 5

# Play a specific classic map
python pacman.py -l mediumClassic

# Use text-only graphics
python pacman.py -l smallClassic -t

# Show all available options
python pacman.py -h
```

Use the arrow keys to move Pacman. The classic maps include food, capsules,
and ghosts. Available examples include `smallClassic`, `mediumClassic`,
`originalClassic`, `powerClassic`, `trickyClassic`, and `contestClassic`.

## Check Search Algorithms

Search checks use explicit maze layouts so algorithm results are reproducible:

```powershell
# Breadth-first search
python pacman.py -l mediumMaze -p SearchAgent -a fn=breadthFirstSearch

# Depth-first search
python pacman.py -l mediumMaze -p SearchAgent -a fn=depthFirstSearch

# Uniform-cost search
python pacman.py -l mediumMaze -p SearchAgent -a fn=uniformCostSearch

# A* with the Manhattan-distance heuristic
python pacman.py -l mediumMaze -p SearchAgent -a fn=aStarSearch,heuristic=manhattanHeuristic
```

Other search maps include `smallMaze`, `bigMaze`, `tinyMaze`, and
`trickySearch`. Add `-t` for text graphics or `-q` for minimal output.

Run the complete search autograder:

```powershell
cd pacman_search
python autograder.py --no-graphics
cd ..
```

## Project Folders

### `pacman_search`

Classic search algorithms, search problems, heuristics, and the search
autograder. This is also the implementation used by the root `pacman.py`
launcher.

### `pacman_multiagents`

Reflex, minimax, alpha-beta, expectimax, and improved evaluation agents.

```powershell
cd pacman_multiagents
python autograder.py --no-graphics
```

### `pacman_reinforcement_learning`

Value iteration, Q-learning, approximate Q-learning, feature extractors, and
Gridworld/Pacman reinforcement-learning tests.

```powershell
cd pacman_reinforcement_learning
python autograder.py --no-graphics
```

## Neural Network Template

`feed_forward_network_template.py` contains a NumPy feed-forward neural
network with sigmoid activation, backpropagation training, and inference.
It expects MNIST CSV files in the same directory when run as a standalone
script.

## Repository Layout

```text
Pacman/
|-- pacman.py
|-- pacman_search/
|-- pacman_multiagents/
|-- pacman_reinforcement_learning/
|-- .gitignore
`-- README.md
```
