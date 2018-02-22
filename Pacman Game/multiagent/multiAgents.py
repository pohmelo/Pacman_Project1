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

        "*** YOUR CODE HERE ***"
        score = 0 # Max score = 100, min score = 0

        if successorGameState.isLose(): #If action leads to losing the game.
            return 0
        elif successorGameState.isWin(): #If action leads to winning the game.
            return 100
        else:
            try: # Clumsy way to check how many ghosts are there. Assumingly four ghosts is the maximum.
                ghostPosition = currentGameState.getGhostPosition(1) # Gets ghost position.
                ghostDistance = util.manhattanDistance(ghostPosition, newPos) # Distance between ghost's position and Pacman's new position.
                if ghostDistance > 2:
                    score += 30 # If distance between ghost and Pacman is greater than 2, we add 30 points to score.
            except IndexError: # Error handling.
                pass

            try: # Same thing repeated here..
                ghostPosition = currentGameState.getGhostPosition(2)
                ghostDistance = util.manhattanDistance(ghostPosition, newPos)
                if ghostDistance > 2:
                    score += 30
            except IndexError:
                pass

            try: # ..and here..
                ghostPosition = currentGameState.getGhostPosition(3)
                ghostDistance = util.manhattanDistance(ghostPosition, newPos)
                if ghostDistance > 2:
                    score += 30
            except IndexError:
                pass

            try: # ..and here.
                ghostPosition = currentGameState.getGhostPosition(4)
                ghostDistance = util.manhattanDistance(ghostPosition, newPos)
                if ghostDistance > 2:
                    score += 30
            except IndexError:
                pass

            currentPos = currentGameState.getPacmanPosition() # Pacman's current position.
            foodDots = currentGameState.getFood() # Food positions.
            minFoodDistance = 1000 # Default minimum food distance.
            for i in foodDots.asList(): # Goes through food positions with help of asList().
                foodDistance = manhattanDistance(i, currentPos) # Distance between food's position and Pacman's _current_ position.
                if foodDistance < minFoodDistance: # If food distance is less than minimum food distance..
                    minFoodDistance = foodDistance # ..minimun food distance is updated.

            minFoodDistance2 = 1000 # Default minimum food distance.
            for j in foodDots.asList(): # Goes through food positions with help of asList().
                foodDistance = manhattanDistance(j, newPos) # Distance between food's position and Pacman's _new_ position.
                if foodDistance < minFoodDistance2: # If food distance is less than minimum food distance..
                    minFoodDistance2 = foodDistance # ..minimun food distance is updated.

            if minFoodDistance2 < minFoodDistance: # Compares if Pacman's new position is closer to food than current position.
                score += 20 # ..And if so, points are added to score.
            elif minFoodDistance2 == minFoodDistance: # Checks if the new and current positions are just as close to food.
                score += random.randint(1,11) # .. And if so, some points are added to score. Random numbers seem to prevent situations where Pacman gets stuck because of same food distances.

            if action == Directions.STOP: # If Pacman doesn't move it will get minus points.
                score -= 10

            return score # Score is returned.

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
        "*** YOUR CODE HERE ***"
        actionAndScore = self.value(gameState, 0, 0) # Pacman's turn, depth is 0 in the beginning.
        return actionAndScore[0] # actionAndScore is tuple, first(0) place is for action and second(1) for score.

    def value(self, gameState, agentIndex, currentDepth): # agentIndex for keeping track turns, current depth for keeping track of depth.
        if agentIndex == gameState.getNumAgents(): # Checks if agentIndex is the same as maximum number of ghosts in current level.
            agentIndex = 0 # ..If so, it's Pacman's turn.
            currentDepth += 1 # Depth of the tree is incresed.

        # Check if current depth is the same as we get from self.depth or if we're winning or losing.
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        elif agentIndex == 0: # 0 is Pacman.
            return self.maxValue(gameState, agentIndex, currentDepth) # maxValue is for Pacman.

        elif agentIndex != 0: # Indices other than 0 are ghosts.
            return self.minValue(gameState, agentIndex, currentDepth) # minValue is for ghosts.

    def minValue(self, gameState, agentIndex, currentDepth):
        v = ('',10000) # Initializing v, 10000 is infinite enough.

        for action in gameState.getLegalActions(agentIndex): # Goes through current agent's legal actions.
            if action != 'Stop': # If legal action is staying still, it is ignored.
                actionAndScore = self.value(gameState.generateSuccessor(agentIndex, action), agentIndex+1, currentDepth) # Recursively calling value function.
                if isinstance(actionAndScore, tuple): # Check if actionAndScore is tuple.
                    actionAndScore = actionAndScore[1] # And from now on actionAndScore is just score.
                v2 = min(actionAndScore, v[1]) # Picking lowest score.
                if v2 < v[1]: # v is replaced if new score is smaller than the old one.
                    v = (action,v2)
        return v

    def maxValue(self, gameState, agentIndex, currentDepth):
        v = ('',-10000) # Initializing v, -10000 is infinite enough.

        for action in gameState.getLegalActions(agentIndex): # Goes through current agent's legal actions.
            if action != 'Stop': # If legal action is staying still, it is ignored.
                actionAndScore = self.value(gameState.generateSuccessor(agentIndex, action), agentIndex+1, currentDepth) # Recursively calling value function.
                if isinstance(actionAndScore, tuple): # Check if actionAndScore is tuple.
                    actionAndScore = actionAndScore[1] # Now actionAndScore is just score.
                v2 = max(v[1], actionAndScore) # Picking greatest score.
                if v2 > v[1]: # v is replaced if new score is greater than the old one.
                    v = (action,v2)
        return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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
        # Initial depth = 1
        # Pacman agent index = 0
        return self.expectimax(gameState, 1, 0)

    def expectimax(self, gameState, currentDepth, agentIndex):
        # Check if we're winning or losing
        if currentDepth > self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        # Take a note of the legal actions for the current agent. Stopping isn't legal.
        legalActions = [action for action in gameState.getLegalActions(agentIndex) if action != 'Stop']

        # Current & Next values
        nextIndex = agentIndex + 1  # For the Agent
        nextDepth = currentDepth  # For the depth
        if nextIndex >= gameState.getNumAgents():  # Next would be ghost
            nextIndex = 0  # Back to Pacman
            nextDepth += 1  # Add 1 to depth

        # Recursively generate the list of expected actions
        actionList = [self.expectimax(gameState.generateSuccessor(agentIndex, action), nextDepth, nextIndex) for action in legalActions]

        if agentIndex == 0 and currentDepth == 1:  # Pacman's first move
            bestIndices = [index for index in range(len(actionList)) if actionList[index] == max(actionList)]
            return legalActions[random.choice(bestIndices)]  # Pick a random action
        elif agentIndex == 0:  # The Max node
            return max(actionList)  # Return the max expectation
        else:  # The chance node
            return sum(actionList)/len(actionList)  # return the average expectation of all legal actions

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

