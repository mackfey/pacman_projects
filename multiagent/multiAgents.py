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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        minFoodDistance = float('inf')
        for food in newFood.asList():
            minFoodDistance = min([manhattanDistance(newPos, food)])

        for ghost in newGhostStates:
            minGhostDistance = min([manhattanDistance(newPos, ghost.getPosition())])

        if minGhostDistance < 2:
            return float('-inf')

        return successorGameState.getScore() + 1.0 / minFoodDistance

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        depth = self.depth * gameState.getNumAgents()
        return self.maxValue(gameState, depth, 0)[1]

    def minimax(self, gameState, depth, agentIndex):
        """
        Returns the minimax value of the given gameState at the given depth and agentIndex
        """
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if agentIndex == 0:
            return self.maxValue(gameState, depth, agentIndex)[0]
        else:
            return self.minValue(gameState, depth, agentIndex)[0]
        
    def maxValue(self, gameState, depth, agentIndex):
        """
        Returns the max value of the given gameState at the given depth and agentIndex
        """
        v = (float('-inf'), None)
        
        return self.valueHelper(gameState, depth, agentIndex, v, max)
    
    def minValue(self, gameState, depth, agentIndex):
        """
        Returns the min value of the given gameState at the given depth and agentIndex
        """
        v = (float('inf'), None)
        
        return self.valueHelper(gameState, depth, agentIndex, v, min)
    
    def valueHelper(self, gameState, depth, agentIndex, v, valueFunction):
        """
        Returns the value of the given gameState at the given depth and agentIndex
        """
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()
            v = valueFunction(v, 
                              (self.minimax(successor, depth - 1, nextAgentIndex), action), 
                              key=lambda x: x[0])
        
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
        depth = self.depth * gameState.getNumAgents()
        return self.maxValue(gameState, depth, 0, float('-inf'), float('inf'))[1]

    def alphaBetaPrune(self, gameState, depth, agentIndex, alpha, beta):
        """
        Returns the alpha-beta pruned value of the given gameState at the given depth and agentIndex with alpha-beta pruning
        """
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if agentIndex == 0:
            return self.maxValue(gameState, depth, agentIndex, alpha, beta)[0]
        else:
            return self.minValue(gameState, depth, agentIndex, alpha, beta)[0]
        
    def maxValue(self, gameState, depth, agentIndex, alpha, beta):
        """
        Returns the max value of the given gameState at the given depth and agentIndex with alpha-beta pruning
        """
        v = (float('-inf'), None)
        
        return self.valueHelper(gameState, depth, agentIndex, v, alpha, beta)
    
    def minValue(self, gameState, depth, agentIndex, alpha, beta):
        """
        Returns the min value of the given gameState at the given depth and agentIndex with alpha-beta pruning
        """
        v = (float('inf'), None)
        
        return self.valueHelper(gameState, depth, agentIndex, v, alpha, beta)
    
    def valueHelper(self, gameState, depth, agentIndex, v, alpha, beta):
        """
        Returns the value of the given gameState at the given depth and agentIndex with alpha-beta pruning
        """
        valueFunction = max if agentIndex == 0 else min

        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()
            v = valueFunction(v, 
                              (self.alphaBetaPrune(successor, depth - 1, nextAgentIndex, alpha, beta), action), 
                              key=lambda x: x[0])
            
            if agentIndex == 0:
                if v[0] > beta:
                    return v
                alpha = valueFunction(alpha, v[0])
            else:
                if v[0] < alpha:
                    return v
                beta = valueFunction(beta, v[0])
        
        return v

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
        "*** YOUR CODE HERE ***"
        depth = self.depth * gameState.getNumAgents()
        return self.maxValue(gameState, depth, 0)[1]
        
    def expectimax(self, gameState, depth, agentIndex):
        """
        Returns the expectimax value of the given gameState at the given depth and agentIndex
        """
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if agentIndex == 0:
            return self.maxValue(gameState, depth, agentIndex)[0]
        else:
            return self.expValue(gameState, depth, agentIndex)
        
    def maxValue(self, gameState, depth, agentIndex):
        """
        Returns the max value of the given gameState at the given depth and agentIndex
        """
        v = (float('-inf'), None)
        
        return self.valueHelper(gameState, depth, agentIndex, v, max)
    
    def expValue(self, gameState, depth, agentIndex):
        """
        Returns the expected value of the given gameState at the given depth and agentIndex
        """
        v = 0
        
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()
            v += self.expectimax(successor, depth - 1, nextAgentIndex)
        
        return v / len(gameState.getLegalActions(agentIndex))
    
    def valueHelper(self, gameState, depth, agentIndex, v, valueFunction):
        """
        Returns the value of the given gameState at the given depth and agentIndex
        """
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)
            nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()
            v = valueFunction(v, 
                              (self.expectimax(successor, depth - 1, nextAgentIndex), action), 
                              key=lambda x: x[0])
        
        return v

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: Similar to reflex agent, but with more variables to consider. 
    Tinkered with the weights of the variables to get a better score.
    Had some success with using non-linear weights for the variables.
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newCapsules = currentGameState.getCapsules()
    minFoodDistance = minGhostDistance = minCapsuleDistance = minScaredGhostDistance = minScaredGhostTimer = float('inf')
    numFood = numCapsules = numScaredGhosts = numNonScaredGhosts = 0

    for food in newFood.asList():
        minFoodDistance = min([manhattanDistance(newPos, food)])
        numFood += 1

    for ghost in newGhostStates:
        minGhostDistance = min([manhattanDistance(newPos, ghost.getPosition())])
        if ghost.scaredTimer > 0:
            numScaredGhosts += 1
            minScaredGhostDistance = min([manhattanDistance(newPos, ghost.getPosition())])
            minScaredGhostTimer = min([ghost.scaredTimer])
        else:
            numNonScaredGhosts += 1

    for capsule in newCapsules:
        minCapsuleDistance = min([manhattanDistance(newPos, capsule)])
        numCapsules += 1

    #print all the values from the return statement below to see the values of the variables
    #print(minFoodDistance, numFood, minGhostDistance, minScaredGhostDistance, numScaredGhosts, numNonScaredGhosts, minCapsuleDistance, numCapsules)

    return currentGameState.getScore() \
        + 1.0 / 10**(minFoodDistance+1) \
        + 1.0 / (numFood+1) \
        + 1.0 / (minGhostDistance+1) \
        + 1.0 / (minScaredGhostDistance+1) \
        + 1.0 / (numScaredGhosts+1) \
        + 1.0 / (numNonScaredGhosts+1)**2 \
        + 1.0 / 1.5**(minCapsuleDistance+1) \
        + 1.0 / (numCapsules+1) \

# Abbreviation
better = betterEvaluationFunction
