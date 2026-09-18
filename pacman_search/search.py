# search.py
# ---------

import util
from game import Directions
from typing import List
import searchProblems
import searchHeuristics


def tinyMazeSearch(problem: searchProblems.SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: searchProblems.SearchProblem) -> List[Directions]:
    
    s = util.Stack()
    visited = set()
    startState = problem.getStartState()
    s.push((startState, []))

    while not s.isEmpty():
        current, actions = s.pop()

        if problem.isGoalState(current):
            return actions
        if current not in visited:
            visited.add(current)
            successors = problem.getSuccessors(current)
            for successor, action, cost in successors:
                newActions = actions + [action]
                s.push((successor, newActions))



def breadthFirstSearch(problem: searchProblems.SearchProblem) -> List[Directions]:
    
    q = util.Queue()
    visited = set()
    startState = problem.getStartState()
    q.push((startState, []))

    while not q.isEmpty():
        current, actions = q.pop()

        if problem.isGoalState(current):
            return actions
        if current not in visited:
            visited.add(current)
            successors = problem.getSuccessors(current)
            for successor, action, cost in successors:
                newActions = actions + [action]
                q.push((successor, newActions))


def uniformCostSearch(problem: searchProblems.SearchProblem) -> List[Directions]:
    
    pq = util.PriorityQueue()
    visited = set()
    startState = problem.getStartState()
    pq.push((startState, [], 0), 0)

    while not pq.isEmpty():
        current, actions, cost = pq.pop()

        if problem.isGoalState(current):
            return actions
        if current not in visited:
            visited.add(current)
            successors = problem.getSuccessors(current)
            for successor, action, stepCost in successors:
                newActions = actions + [action]
                newCost = cost + stepCost
                pq.push((successor, newActions, newCost), newCost)

def aStarSearch(problem, heuristic=searchHeuristics.nullHeuristic):

    open_list = util.PriorityQueue()
    closed_list = {}

    start_state = problem.getStartState()

    open_list.push((start_state, [], 0), 0)

    while not open_list.isEmpty():

        current, actions, cost = open_list.pop()

        if problem.isGoalState(current):
            return actions

        if current in closed_list and closed_list[current] <= cost:
            continue

        closed_list[current] = cost

        successors = problem.getSuccessors(current)

        for successor, action, stepCost in successors:

            newActions = actions + [action]

            g = problem.getCostOfActions(newActions)
            h = heuristic(successor, problem)

            f = g + h

            open_list.push(
                (successor, newActions, g),
                f
            )

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch