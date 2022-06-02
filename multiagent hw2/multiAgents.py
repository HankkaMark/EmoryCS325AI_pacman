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
#
# Modified by Eugene Agichtein for CS325 Sp 2014 (eugene@mathcs.emory.edu)
#

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
        Note that the successor game state includes updates such as available food,
        e.g., would *not* include the food eaten at the successor state's pacman position
        as that food is no longer remaining.
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        currentFood = currentGameState.getFood() #food available from current state
        newFood = successorGameState.getFood() #food available from successor state (excludes food@successor)
        currentCapsules=currentGameState.getCapsules() #power pellets/capsules available from current state
        newCapsules=successorGameState.getCapsules() #capsules available from successor (excludes capsules@successor)
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        score = 0
        if util.manhattanDistance(newPos, successorGameState.getGhostPosition(1)) <= 1:
            return -99999
        if len(newFood.asList()) < len(currentFood.asList()):
            return 99999
        fd = []
        for food in newFood.asList():
            fd.append(util.manhattanDistance(newPos,food))
        score -= min(fd)

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
        "*** YOUR CODE HERE ***"
        # input:gameState
        # v=max(state)
        # return action in successors(state) with value v
        score,max_action = self.max_value(gameState,1)
        return max_action


    def max_value(self,gameState,cur_depth):
        #if terminal_state then return utility
        max_action = None
        if cur_depth>self.depth:
            return self.evaluationFunction(gameState),max_action
        actions = gameState.getLegalActions(0)
        if len(actions) == 0:
            return self.evaluationFunction(gameState),max_action
        # v=inf
        score=-99999
        # for a,s in successors(state) do
        #     v=MAX(v,Min_value(s,1))
        # return v
        for action in actions:
            tempScore = self.min_value(gameState.generateSuccessor(0, action), cur_depth, 1)
            if tempScore > score:
                score = tempScore
                max_action = action
        return score, max_action

    def min_value(self,gameState,cur_depth,agent_index):
        #if terminal_state then return utility
        if cur_depth>self.depth:
            return self.evaluationFunction(gameState)
        actions = gameState.getLegalActions(agent_index)
        if len(actions) == 0:
            return self.evaluationFunction(gameState)
        # v=inf
        score=99999
        # for a,s in successors(state) do
        #     v=MAX(v,Min_value(s,1))
        # return v
        for action in actions:
            if agent_index>= gameState.getNumAgents()-1:
                tempScore,max_action = self.max_value(gameState.generateSuccessor(agent_index, action), cur_depth+1)
            else:
                tempScore = self.min_value(gameState.generateSuccessor(agent_index, action), cur_depth, agent_index+ 1)
            if tempScore < score:
                score = tempScore
        return score


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        a,b =float(-999999),float(999999)
        score, max_action = self.max_value(gameState, 1,a,b)
        return max_action

    def max_value(self,gameState,cur_depth,a,b):
        # if terminal_state then return utility
        max_action = None
        if cur_depth > self.depth:
            return self.evaluationFunction(gameState), max_action
        actions = gameState.getLegalActions(0)
        if len(actions) == 0:
            return self.evaluationFunction(gameState), max_action
        # v=inf
        score = float(-99999)
        # for a,s in successors(state) do
        #     v=MAX(v,Min_value(s,1))
        # return v
        for action in actions:
            tempScore = self.min_value(gameState.generateSuccessor(0, action), cur_depth, 1,a,b)
            if tempScore > score:
                score = tempScore
                max_action = action
            if score > b:
                return score,max_action
            if a < score:
                a = score
        return score, max_action

    def min_value(self, gameState, cur_depth, agent_index,a,b):
        # if terminal_state then return utility
        if cur_depth > self.depth:
            return self.evaluationFunction(gameState)
        actions = gameState.getLegalActions(agent_index)
        if len(actions) == 0:
            return self.evaluationFunction(gameState)
        # v=inf
        score = float(99999)
        # for a,s in successors(state) do
        #     v=MAX(v,Min_value(s,1))
        # return v
        for action in actions:
            if agent_index >= gameState.getNumAgents() - 1:
                tempScore, max_action = self.max_value(gameState.generateSuccessor(agent_index, action), cur_depth + 1,a,b)
            else:
                tempScore = self.min_value(gameState.generateSuccessor(agent_index, action), cur_depth, agent_index + 1,a,b)
            if tempScore < score:
                score = tempScore
            if score < a:
                return score
            if b > score:
                b = score
        return score

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
        a,b =float(-999999),float(999999)
        score, max_action = self.max_value(gameState, 1,a,b)
        return max_action

    def max_value(self,gameState,cur_depth,a,b):
        # if terminal_state then return utility
        max_action = None
        if cur_depth > self.depth:
            return self.evaluationFunction(gameState), max_action
        actions = gameState.getLegalActions(0)
        if len(actions) == 0:
            return self.evaluationFunction(gameState), max_action
        # v=inf
        score = float(-99999)
        # for a,s in successors(state) do
        #     v=MAX(v,Min_value(s,1))
        # return v
        for action in actions:
            tempScore = self.min_value(gameState.generateSuccessor(0, action), cur_depth, 1,a,b)
            if tempScore > score:
                score = tempScore
                max_action = action
            if score > b:
                return score,max_action
            if a < score:
                a = score
        return score, max_action

    def min_value(self, gameState, cur_depth, agent_index,a,b):
        # if terminal_state then return utility
        if cur_depth > self.depth:
            return self.evaluationFunction(gameState)
        actions = gameState.getLegalActions(agent_index)
        if len(actions) == 0:
            return self.evaluationFunction(gameState)
        # v=inf
        score = 0
        # for a,s in successors(state) do
        #     v=MAX(v,Min_value(s,1))
        # return v
        for action in actions:
            if agent_index >= gameState.getNumAgents() - 1:
                tempScore, max_action = self.max_value(gameState.generateSuccessor(agent_index, action), cur_depth + 1,a,b)
            else:
                tempScore = self.min_value(gameState.generateSuccessor(agent_index, action), cur_depth, agent_index + 1,a,b)
            score += tempScore
        return score/len(actions)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <I didn't used a lot of 1/value in my calculation since I found it's hard
      for me to manipulate the weight of each function when there're a mixture of inversed value
      and normal value. While considering the function, I first listed out every possible
      factors, including distance to nearest ghost, distance to nearest food, distance to
      nearst capsules and the number of all three things left. By making a linear combination
      of them I get my first version. Then I added more features like if I can predate the
      ghost. TBH that didn't make huge difference to the final result and It seems for the test
      case given, my eva function did pretty well.
      Instead of inverse, I used -1* weight * that value. That has almost same function,
      but making my every score a huge negative number. I want to maximize (to some extend) the
      distance between me and ghost, while minimize all other factors. I gave weight according
      to the priority of each factors. For example, I think the food rest is important since
      we are getting point while we minimize food lefts.>
    """
    "*** YOUR CODE HERE ***"
    currentPos = currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood().asList()
    currentCapsules = currentGameState.getCapsules()
    currentGhostStates = currentGameState.getGhostStates()
    currentScaredTimes = [ghostState.scaredTimer for ghostState in currentGhostStates]

    if currentGameState.isWin():
        return 9999999
    if util.manhattanDistance(currentPos, currentGameState.getGhostPosition(1)) <= 1:
        return -9999999
    # fd = []
    # for food in currentFood:
    #     fd.append(util.manhattanDistance(currentPos,food))
    fd = [util.manhattanDistance(currentPos, food) for food in currentFood]
    min_fd = min(fd)
    predate=0
    currentGhostDistances = [util.manhattanDistance(currentPos, ghost.getPosition()) for ghost in currentGameState.getGhostStates()]
    if min(currentGhostDistances) >= 1:
        if sum(currentScaredTimes) < 0:
            predate = predate -100 / min(currentGhostDistances)
        else:
            predate = predate +100 / min(currentGhostDistances)

    score = 50 * util.manhattanDistance(currentPos,currentGameState.getGhostPosition(1)) \
            - 100 * min_fd - 500 * len(currentCapsules) \
            - 1000 * len(currentFood) + predate

    return score

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

