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
        
        newFoodPosition = newFood.asList() #Food positions list.
        newGhostPosition = successorGameState.getGhostPositions() #Ghost positions list.
        
        #Calculate the manhattan distance between pacman and food.
        food = [util.manhattanDistance(newPos,food) for food in newFoodPosition]
        
        #Distance between pacman and the ghosts.
        ghostDistance = [util.manhattanDistance(newPos,ghost) for ghost in newGhostPosition]
        score = 0
        
        for i in ghostDistance:
            if i <= 1.0:
                return -float('inf')
        
        #If there still are dots in the map, we will check if our pacman has eaten a capsule
        if len(food):
            #If our pacman didn't eat a capsule, we will consider our score as the state's score                 # adding the ghost's maximun distance and minus the nearest food distance.
            if 0 in newScaredTimes:
                score = successorGameState.getScore() + max(ghostDistance) - min(food)
                
            #If did it, we will considerate our score as the state's score minus the
            # ghost's minimun distance and the nearest food distance.
            else:
                score = successorGameState.getScore() - min(ghostDistance) - min(food)
        
        #If there's no food, we have to make a evaluation of the state too.
        #If our pacman didn't eat a capsule we will consider the farest ghost
        #Else, the nearest ghost.
        else:
            if 0 in newScaredTimes:
                score = successorGameState.getScore() + max(ghostDistance)
            else:
                score = successorGameState.getScore() - min(ghostDistance)
       
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
    
    def minimax(self, gameState, depth, index):
        """
        MINIMAX Function.
        
        @param: gameState
        @param: depth
        @param: index of the agent
        """
        num_agents = gameState.getNumAgents() #Get the number of agents in the game
        agents = index%num_agents #Get the agent we are evaluating now
        depth += index//num_agents # the depth where we are
            
        #If we arrive at the end of the game or we are at the specific depth we return the evaluation of the state. 
        if gameState.isLose() or gameState.isWin() or self.depth == depth:
            return (self.evaluationFunction(gameState),None)
        
        #Now:if the agent is 0 (PACMAN), we will maximize.
        # Else we will minimize.
        else:    
            v = list()
            
            if agents == 0:
                
                for action in gameState.getLegalActions(agents):
                    state = gameState.generateSuccessor(agents,action)
                    v.append((self.minimax(state,depth,agents+1)[0],action))
                max_value = max(v)
                return max_value

            else:
                
                for action in gameState.getLegalActions(agents):
                    state = gameState.generateSuccessor(agents,action)
                    v.append((self.minimax(state,depth,agents+1)[0],action))
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
        a = self.minimax(gameState,0,pacman)
        
        return a[1] #Return the action.

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    
    def alpha_beta(self, gameState, depth, index, alpha, beta):
        """
        Alpha-Beta Pruning Function.
        
        @param: gameState
        @param: depth
        @param: index of the agent
        """
        
        num_agents = gameState.getNumAgents()
        agents = index%num_agents
        depth += index//num_agents
        
        if gameState.isLose() or gameState.isWin() or self.depth == depth:
            return (self.evaluationFunction(gameState),None)
        
        else:
            
            v = []
            
            #Maximize
            if agents == 0:
                value = -float('inf')
                for action in gameState.getLegalActions(agents):
                    
                    successor = gameState.generateSuccessor(agents,action)
                    v.append((self.alpha_beta(successor,depth,agents+1,alpha,beta)[0],action))
                    value = max(v)                   
                    if value[0] > beta: #If the value it's higher than beta, we prunning and return this value
                        return value
                    
                    #Change alpha as the greatest value we have visited.
                    alpha = max(alpha,value[0])
                return value
            
            #Minimize
            else:
                value = float('inf')       
                for action in gameState.getLegalActions(agents):
                    successor = gameState.generateSuccessor(agents,action)
                    v.append((self.alpha_beta(successor,depth,agents+1,alpha,beta)[0],action))
                    value = min(v)
                    if value[0] < alpha: #If the value it'lower than alpha, we prunning and return this value
                        return value
                    
                    #Change beta as the lowest value we have visited.
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
        
        a = self.alpha_beta(gameState, 0, pacman, alpha, beta)
        
        return a[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    
    def expectimax(self,gameState,depth,index):
        """
        Expectimax Function.
        
        @param: gameState
        @param: depth
        @param: index of the agent
        """
        
        num_agents = gameState.getNumAgents()
        agents = index%num_agents
        depth += index//num_agents
            
        if gameState.isLose() or gameState.isWin() or self.depth == depth:
            return (self.evaluationFunction(gameState),None)
        
        else:
            
            v = []
            
            #If its pacman, we will maximize
            if agents == 0:
                
                
                for action in gameState.getLegalActions(agents):
                    v.append((self.expectimax(gameState.generateSuccessor(agents,action),depth,agents+1)[0],action))
                max_value = max(v)
                
                return max_value

            #if not, for every action of the agent we will return the mean of the all evaluations
            else:
                
                beta = 0
                num_actions = 0
                
                for action in gameState.getLegalActions(agents):
                    num_actions += 1
                    beta += self.expectimax(gameState.generateSuccessor(agents,action),depth,agents+1)[0]
                
                return (beta/num_actions,None)
                
    

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        pacman = 0
        a = self.expectimax(gameState,0,pacman)
        
        return a[1]
        

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION:
      
      Due to we have to evaluate the current State instead of the actions, I decide
      to check the ghosts and the food in the current state.
      
      The evaluation we will return is calculated from the current score minus the nearest
      food and the farest ghost.
      
      Also, if we arrive at the end of the game or a ghost is too close of us, we will return -inf
      because we dont want to arrive at this state. On the other hand, we will return inf if we win the game.
      
    """
    
    gameState = currentGameState
    
    newPos = gameState.getPacmanPosition()
    newFoodPosition = gameState.getFood().asList()
    newGhostPosition = gameState.getGhostPositions()
    
    food = [util.manhattanDistance(newPos,food) for food in newFoodPosition]
    ghostDistance = [util.manhattanDistance(newPos,ghost) for ghost in newGhostPosition]
    
    score = gameState.getScore()
    
    distFood = 0
    distGhost = 0
    
    if gameState.isWin():
        return float('inf')
    if gameState.isLose():
        return -float('inf')
    
    for i in ghostDistance:
        if i <= 1:
            return -float('inf')
    
    if(len(food)>0):
        distFood = min(food)
      
    
    return gameState.getScore() - distFood - max(ghostDistance)
    

# Abbreviation
better = betterEvaluationFunction

