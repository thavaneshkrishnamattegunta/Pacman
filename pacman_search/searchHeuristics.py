from turtle import position

import util
from typing import List, Any, Tuple
import searchProblems

def nullHeuristic(state: Any, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def manhattanHeuristic(position, problem, info={}):
    goal = problem.goal

    return abs(position[0] - goal[0]) + abs(position[1] - goal[1])


def euclideanHeuristic(position: Tuple[int,int], problem: searchProblems.PositionSearchProblem, info={}) -> float:
    "The Euclidean distance heuristic for a PositionSearchProblem"
    x1, y1 = position
    x2, y2 = problem.goal
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def cornersHeuristic(state, problem):

    position, visited_corners = state

    remaining_corners = frozenset(set(problem.corners) - visited_corners)

    if not remaining_corners:
        return 0

    return max(util.manhattanDistance(position, corner)
        for corner in remaining_corners
    )


def foodHeuristic(state, problem):

    position, foodGrid = state
    foodList = foodGrid.asList()

    if len(foodList) == 0:
        return 0

    if len(foodList) == 1:
        return util.manhattanDistance(position, foodList[0])

    max_distance = -1
    f1 = None
    f2 = None

    for i in range(len(foodList)):
        for j in range(len(foodList)):
            if i != j:

                distance = util.manhattanDistance(foodList[i], foodList[j])

                if distance > max_distance:
                    max_distance = distance
                    f1 = foodList[i]
                    f2 = foodList[j]

    distance_to_f1 = util.manhattanDistance(position, f1)
    distance_to_f2 = util.manhattanDistance(position, f2)

    return max_distance + min(distance_to_f1, distance_to_f2)