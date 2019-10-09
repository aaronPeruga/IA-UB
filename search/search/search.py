# -*- coding: utf-8 -*-
#
# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
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
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    
    
    frontier = util.Stack()  #Frontier is a Stack. We put the states we will visit.
    closed = list()         #Visited states list.
    solution = list()       #Our solution
    
    start = problem.getStartState()  #start position.
    
    frontier.push((start,[],0))  #Push into the stack
    
    
    while not frontier.isEmpty():  #If the frontier is not empty
        
        node,path,cost = frontier.pop()   #Extract a state
        
        if problem.isGoalState(node):   #If node is the end, return solution.
            
            solution = path
            break
            
        else:    #If the node is not in close, we add it and push their neighboors into the stack.
            
            if node not in closed:
                closed.append(node)
                for packet in problem.getSuccessors(node):
                    
                    newNode = packet[0]
                    newPath = path +  [packet[1]]
                    newCost = cost + packet[2]
                    if newNode not in closed:
                        frontier.push((newNode,newPath,cost))
                        
    return solution #return the path to our solution 
    
    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    
    frontier = util.Queue()    #Frontier is a Queue. We put the states we will visit.
    closed = list()         #Visited states list.
    solution = list()       #Our solution
    
    start = problem.getStartState()      #start position.
    
    frontier.push((start,[],0))         #Push into the stack
    closed.append(start)           #Put the state as visited
    
    while not frontier.isEmpty():   #If the frontier is not empty

        node, path, cost = frontier.pop()   #Extract a state
        
        if problem.isGoalState(node):    #If node is the end, return solution.
            solution = path
            break
            
        else:
            for pack in problem.getSuccessors(node):  #If the node is not in the Queue, we add it and push 
                                                      #their neighboors into the stack.
                if pack[0] not in closed:
                    
                    newNode = pack[0]
                    newPath = path + [pack[1]]
                    newCost = cost + pack[2]
                    
                    frontier.push((newNode,newPath,newCost))
                    closed.append(pack[0])
                    
    
    
    return solution  #Return the path to our solution
        
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    
    frontier = util.PriorityQueue()   #Priority Queue   
    solution = list()                 #Our solution
    closed = list()
    
    start = problem.getStartState()
    
    frontier.push((start,[],0),heuristic(start,problem))
    
    while not frontier.isEmpty():           #If frontier is not empty
        
        node,path,cost = frontier.pop()    #Extract the node with the lowest heuristic
        
        if not node in closed:         #if the node not in closed, append it.
            closed.append(node)
            
            if problem.isGoalState(node):  #if the node is the goal, we return the solution
                solution = path        
                break
            for pack in problem.getSuccessors(node): #For every successor:
                
                newNode = pack[0]          #Extract the new node
                newPath = path + [pack[1]] #add action to the path
                
                #Calculate the new heuristic for this node
                newCost = problem.getCostOfActions(newPath) + heuristic(newNode,problem)
                
                #Push state in the Priority Queue
                frontier.push((newNode,newPath,problem.getCostOfActions(newPath)),newCost)
                           
    return solution #Return solution-


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
