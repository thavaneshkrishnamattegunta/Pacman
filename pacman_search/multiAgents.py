# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        foodList = newFood.asList()
        foodDistance = min((manhattanDistance(newPos, food) for food in foodList), default=0)
        score = successorGameState.getScore() + 10.0 / (foodDistance + 1)
        for ghost, scaredTime in zip(newGhostStates, newScaredTimes):
          distance = manhattanDistance(newPos, ghost.getPosition())
          if scaredTime > 0:
            score += 20.0 / (distance + 1)
          elif distance <= 1:
            score -= 1000
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        def minimax(state, depth, agentIndex):
          if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
          actions = state.getLegalActions(agentIndex)
          if not actions:
            return self.evaluationFunction(state)
          nextAgent = (agentIndex + 1) % state.getNumAgents()
          nextDepth = depth + 1 if nextAgent == 0 else depth
          values = [minimax(state.generateSuccessor(agentIndex, action), nextDepth, nextAgent)
                for action in actions]
          return max(values) if agentIndex == 0 else min(values)

        actions = gameState.getLegalActions(0)
        if not actions:
          return Directions.STOP
        return max(actions, key=lambda action: minimax(
          gameState.generateSuccessor(0, action), 0, 1 % gameState.getNumAgents()))

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        def alphabeta(state, depth, agentIndex, alpha, beta):
          if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
          actions = state.getLegalActions(agentIndex)
          if not actions:
            return self.evaluationFunction(state)
          nextAgent = (agentIndex + 1) % state.getNumAgents()
          nextDepth = depth + 1 if nextAgent == 0 else depth
          if agentIndex == 0:
            value = float('-inf')
            for action in actions:
              value = max(value, alphabeta(
                state.generateSuccessor(agentIndex, action), nextDepth,
                nextAgent, alpha, beta))
              if value > beta:
                break
              alpha = max(alpha, value)
            return value
          value = float('inf')
          for action in actions:
            value = min(value, alphabeta(
              state.generateSuccessor(agentIndex, action), nextDepth,
              nextAgent, alpha, beta))
            if value < alpha:
              break
            beta = min(beta, value)
          return value

        actions = gameState.getLegalActions(0)
        if not actions:
          return Directions.STOP
        alpha = float('-inf')
        beta = float('inf')
        bestAction = actions[0]
        bestValue = float('-inf')
        for action in actions:
          value = alphabeta(gameState.generateSuccessor(0, action), 0,
                    1 % gameState.getNumAgents(), alpha, beta)
          if value > bestValue:
            bestValue, bestAction = value, action
          alpha = max(alpha, bestValue)
        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        def expectimax(state, depth, agentIndex):
          if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
          actions = state.getLegalActions(agentIndex)
          if not actions:
            return self.evaluationFunction(state)
          nextAgent = (agentIndex + 1) % state.getNumAgents()
          nextDepth = depth + 1 if nextAgent == 0 else depth
          values = [expectimax(state.generateSuccessor(agentIndex, action), nextDepth, nextAgent)
                for action in actions]
          if agentIndex == 0:
            return max(values)
          return sum(values) / len(values)

        actions = gameState.getLegalActions(0)
        if not actions:
          return Directions.STOP
        return max(actions, key=lambda action: expectimax(
          gameState.generateSuccessor(0, action), 0, 1 % gameState.getNumAgents()))

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    position = currentGameState.getPacmanPosition()
    food = currentGameState.getFood().asList()
    ghosts = currentGameState.getGhostStates()
    score = currentGameState.getScore() - 8 * len(food)
    if food:
      score += 15.0 / (min(manhattanDistance(position, item) for item in food) + 1)
    score -= 15 * len(currentGameState.getCapsules())
    for ghost in ghosts:
      distance = manhattanDistance(position, ghost.getPosition())
      if ghost.scaredTimer:
        score += 50.0 / (distance + 1)
      elif distance <= 1:
        score -= 1000
      elif distance <= 2:
        score -= 200
      else:
        score += 0.2 * distance
    return score

# Abbreviation
better = betterEvaluationFunction
