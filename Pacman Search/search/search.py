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
    return [s, s, w, s, w, w, s, w]


def genericSearch(problem, fringe, heuristic=None):
    """
    A generic search algorithm to solve the Pacman Search
    :param problem: The problem
    :param fringe: The fringe, either of type:
        - Stash, for DFS. A Last-In-First-Out type of stash.
        - Queue, for BFS. A First-In-First-Out type of stash.
        - PriorityQueue, for UCS (and the A* search). Drops items from the stash based
          on the priority/cost given to them
    :param heuristic: The type of heuristic being used. Default = None
    :return []: Empty array (Safe exit, should not happen)
    :return actions: The actions done to get to the goal state.
    """

    visited = []  # The nodes that have already been visited
    actions = []  # The actions that have already been made
    initial = problem.getStartState()  # The initial state of the problem

    # Push the initial start state + blank action (because we've done nothing to get there) to the fringe
    if isinstance(fringe, util.Stack) or isinstance(fringe, util.Queue):
        fringe.push((initial, actions))
    # If using the PriorityQueue, calculate the priority according to the given heuristic
    elif isinstance(fringe, util.PriorityQueue):
        fringe.push((initial, actions), heuristic(initial, problem))

    """
    Go through the fringe.
    Remove the current value from the fringe
    If the node was NOT visited, see if it's goal
    If not goal, add node's successors to fringe
    """
    while fringe:
        # If using Stack (DFS) or Queue (BFS)
        if isinstance(fringe, util.Stack) or isinstance(fringe, util.Queue):
            node, actions = fringe.pop()  # Record the node and the actions taken, remove them from the fringe
        # If using PriorityQueue (UCS and A*)
        elif isinstance(fringe, util.PriorityQueue):
            node, actions = fringe.pop()  # Record the node and the actions taken, remove them from the fringe

        # If the node has NOT been visited
        if node not in visited:
            visited.append(node)  # Add the node to visited
            # If at goal --> return with the path (actions) taken
            if problem.isGoalState(node):
                return actions
            """
            The code below only executes if the node wasn't the goal
            """
            successors = problem.getSuccessors(node)  # Save the successor nodes of the current node
            # Cycle through the successors
            for successor in successors:
                coordinate, direction, cost = successor  # Record the values of the current (successor) node
                new_actions = actions + [direction]  # Expand the actions done so far

                # Stack (DFS) and Queue (BFS):
                if isinstance(fringe, util.Stack) or isinstance(fringe, util.Queue):
                    fringe.push((coordinate, new_actions))  # Add the new actions and the coordinate into the fringe
                # PriorityQueue (UCS and A*):
                elif isinstance(fringe, util.PriorityQueue):
                    # The new cost is the previous cost + the heuristic factor (which is 0 for UCS)
                    new_cost = problem.getCostOfActions(new_actions) + heuristic(coordinate, problem)
                    # Add the new actions, coordinate + cost into the Fringe
                    fringe.push((coordinate, new_actions), new_cost)
            """
            At this point, we have looped through all of the new node's successors and
            added them into the fringe according to the Stack (DFS)/Queue (BFS)/PriorityQueue (UCS, A*).
            Next we will cycle into the next item in the fringe and start again.
            
            If the next item in the fringe was a node we had already visited, we'll jump over it.
            """
    return []  # This only ever happens if the fringe didn't exist or goal was not found.


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Use the genericSearch-algorithm to solve the problem. We use the Stash (LastIn-FirstOut)
    to maintain the fringe.
    """
    return genericSearch(problem, util.Stack())


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.

    Use the genericSearch-algorithm to solve the problem. We use the Queue (FirstIn-FirstOut)
    to maintain the fringe.
    """
    return genericSearch(problem, util.Queue())


def uniformCostSearch(problem):
    """
    Search the node of least total cost first.

    Use the genericSearch-algorithm to solve the problem. The UCS is essentially
    the same as using A* without a heuristic, thus we will simply call A*
    with the heuristic set as null
    """
    return aStarSearch(problem)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.

    Use the genericSearch-algorithm to solve the A* search. We use the PriorityQueue
    to maintain the fringe. With the priority queue, each item in the fringe has a
    priority assigned to it, which defines when the item will be dropped out of the fringe.
    Essentially, the heuristic given defines the priority of the item.

    If no heuristic given, the nullHeuristic is chosen by default. If nullHeuristic is being
    used, the search will act like UCS. We call this function from the UCS with the heuristic
    set as null.
    """
    return genericSearch(problem, util.PriorityQueue(), heuristic)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
