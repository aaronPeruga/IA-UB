# multiAgents.py
# --------------
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
        #Calculate the next event
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        #Calculate new position
        newPos = successorGameState.getPacmanPosition()
        #Get where's the food
        newFood = successorGameState.getFood()
        #Where's the ghost
        newGhostStates = successorGameState.getGhostStates()
        #holds the number of moves that each ghost will remain scared because of Pacman having eaten a power pellet
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        
        newFoodPosition = newFood.asList()
        newGhostPosition = successorGameState.getGhostPositions()
        
        food = [util.manhattanDistance(newPos,food) for food in newFoodPosition]
        ghostDistance = [util.manhattanDistance(newPos,ghost) for ghost in newGhostPosition]
        score = 0
        
        if len(food):
            if 0 in newScaredTimes:
                score = successorGameState.getScore() + max(ghostDistance) - min(food)
            else:
                score = successorGameState.getScore() + min(ghostDistance) - min(food)
            
        else:
            if 0 in newScaredTimes:
                score = successorGameState.getScore() + max(ghostDistance)
            else:
                score = successorGameState.getScore() + min(ghostDistance)
       
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
    
    def minimax(self, gameState, depth, index, maxi = True):
        
        num_agents = gameState.getNumAgents()
        
        if gameState.isLose() or gameState.isWin() or self.depth == depth:
            return (self.evaluationFunction(gameState),None)
        else:
            agents = index%num_agents
            v = []
            if maxi == True:
                
                for action in gameState.getLegalActions(agents):
                    v.append((self.minimax(gameState.generateSuccessor(agents,action),depth,agents+1,False)[0],action))
                max_value = max(v)
                return max_value

            else:
                             
                if agents == num_agents-1:
                    for action in gameState.getLegalActions(agents):
                        v.append((self.minimax(gameState.generateSuccessor(agents,action),depth+1,agents+1,True)[0],action))
                    min_value = min(v)
                    return min_value
                         
                else:
                    for action in gameState.getLegalActions(agents):
                        v.append((self.minimax(gameState.generateSuccessor(agents,action),depth,agents+1,False)[0],action))
                    min_value = min(v)
                    return min_value
                

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
        
        pacman = 0
        
        a = self.minimax(gameState,0,pacman,True)
        
        return a[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    
    def alpha_beta(self, gameState, depth, index, alpha, beta, maxi = True):
        
        num_agents = gameState.getNumAgents()
        if gameState.isLose() or gameState.isWin() or self.depth == depth:
            return (self.evaluationFunction(gameState),None)
        else:
            
            agents = index%num_agents
            v = []
            
            if maxi == True:
                value = -float('inf')
                for action in gameState.getLegalActions(agents):
                    
                    successor = gameState.generateSuccessor(agents,action)
                    v.append((self.alpha_beta(successor,depth,agents+1,alpha,beta,False)[0],action))
                    
                    value = max(v)                   
                    
                    if value[0] > beta:
                        return value
                    
                    alpha = max(alpha,value[0])
                    
                return value

            else:
                value = float('inf')       
                if agents == num_agents-1: #PACMAN
                    for action in gameState.getLegalActions(agents):
                        successor = gameState.generateSuccessor(agents,action)
                        v.append((self.alpha_beta(successor,depth+1,agents+1,alpha,beta,True)[0],action))
                        
                        value = min(v)
                        
                        
                        if value[0] < alpha:
                            return value
                        beta = min(beta,value[0])
                        
                    return value
                         
                else:
                    for action in gameState.getLegalActions(agents):
                        successor = gameState.generateSuccessor(agents,action)
                        v.append((self.alpha_beta(successor,depth,agents+1,alpha,beta,False)[0],action))
                       
                        value = min(v)
                        
                        if value[0] < alpha:
                            return value
                        beta = min(beta,value[0])
                    return value
    
    
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        pacman = 0
        alpha = -float('inf')
        beta = float('inf')
        
        a = self.alpha_beta(gameState, 0, pacman, alpha, beta, True)
        
        return a[1]

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
        util.raiseNotDefined()

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

