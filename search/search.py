# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

"""
Global constants used to track state indexes in the frontier data structure.
"""
getNode = 0
getPath = 1
getCost = 2

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def costFunctionHelper(problem, frontier, visited, cost, state, path, successor, heuristic=nullHeuristic):
    """
    Helper function for cost functions for adding states to the frontier.

    Args:
        problem: The search problem.
        frontier: The frontier data structure.
        visited: The set of visited states.
        cost: The dictionary of costs for each state.
        state: The current state.
        path: The current path.
        successor: The successor state.
        heuristic: The heuristic function.

    Returns:
        None
    """
    if successor[getNode] not in visited:
        if successor[getNode] not in cost or cost[successor[getNode]] > cost[state] + successor[getCost]:
            cost[successor[getNode]] = cost[state] + successor[getCost]
            frontier.push((successor[getNode], path + [successor[getPath]]), cost[successor[getNode]] + heuristic(successor[getNode], problem))

def searchHelper(problem, frontierDataStructure, isCostFunction=False, heuristic=nullHeuristic):
    """
    Helper function for search algorithms. Generic search algorithm that is called by each search algorithm.

    Args:
        problem: The search problem.
        frontierDataStructure: The frontier data structure (stack, queue, priority queue, etc).
        isCostFunction: Boolean value that determines whether the search algorithm is a cost function.
        heuristic: The heuristic function.

    Returns:
        The path to the goal state.
    """
    frontier = frontierDataStructure
    visited = set()

    if isCostFunction:
        cost = dict()
        cost[problem.getStartState()] = 0
        frontier.push((problem.getStartState(), []), 0)
    else:
        frontier.push((problem.getStartState(), []))

    while not frontier.isEmpty():
        state, path = frontier.pop()
        if problem.isGoalState(state):
            return path
        if state not in visited:
            visited.add(state)
            for successor in problem.getSuccessors(state):
                if isCostFunction:
                    costFunctionHelper(problem, frontier, visited, cost, state, path, successor, heuristic) 
                else:
                    frontier.push((successor[getNode], path + [successor[getPath]]))
    
    return []

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    return searchHelper(problem, util.Stack())

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    return searchHelper(problem, util.Queue())

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    return aStarSearch(problem)

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    return searchHelper(problem, util.PriorityQueue(), True, heuristic)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
