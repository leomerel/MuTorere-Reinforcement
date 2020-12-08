import gym
from gym import error, spaces, utils
from gym.utils import seeding
import gym
import numpy as np

class Case :

	def __init__(self,id,color):
		self.id = id
		self.color = color

class MuToRere(gym.Env):
	metadata = {'render.modes': ['human']}


	def __init__(self):
		self.state = [[Case(7,'w'),Case(8,'w'),Case(9,'w')],[Case(4,'w'),Case(5,'o'),Case(6,'b')],[Case(1,'b'),Case(2,'b'),Case(3,'b')]]
		self.neighbors = [(4,2),(1,3),(2,6),(1,7),None,(3,9),(4,8),(7,9),(6,8)]
		self.turn = 'b'

		self.stateSpacePlus = []
		self.possibleActions = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

		self.stateSpacePlus.append(self.state)

	def checkNeighbors(self,id):
		return not (self.searchCaseById(self.neighbors[id-1][0]).color == self.searchCaseById(self.neighbors[id-1][1]).color and self.searchCaseById(self.neighbors[id-1][0]).color == self.searchCaseById(id).color)

	def searchCaseById(self,id):
		for row in self.state :
			for case in row :
				if case.id == id :
					return case

	def checkMove(self,player,id):
		if not (id < 10 and id > 0):
			return False

		case = self.searchCaseById(id)

		if id != 5 :
			neighbors = (self.searchCaseById(self.neighbors[id-1][0]),self.searchCaseById(self.neighbors[id-1][1]))

		if player != self.turn :
			return False

		if player != case.color :
			return False

		if case.id != 5 :
			if not self.checkNeighbors(case.id) :
				return False

		if id != 5 :
			if self.state[1][1].color != 'o' and neighbors[0].color != 'o' and neighbors[1].color != 'o' :
				return False

		return True

	def checkEndConditions(self,player):
		canMove = False
		for i in range(1,10) :
			canMove |= self.checkMove(player,i)
		return canMove

	def step(self, id, player):
		case = self.searchCaseById(id)

		if id != 5 :
			neighbors = (self.searchCaseById(self.neighbors[id-1][0]),self.searchCaseById(self.neighbors[id-1][1]))

			if self.state[1][1].color == 'o' :
				self.state[1][1].color = case.color
				case.color = 'o'

			elif neighbors[0].color == 'o':
				neighbors[0].color = case.color
				case.color = 'o'

			elif neighbors[1].color == 'o' :
				neighbors[1].color = case.color
				case.color = 'o'

		else :
			for row in self.state :
				for a in row :
					if a.id != 5 and a.color == 'o' :
						a.color = case.color
						case.color = 'o'

		if self.state not in self.stateSpacePlus :
			self.stateSpacePlus.append(self.state)

		isWon = not self.checkEndConditions(self.otherPlayer(player))
		reward = -1 if not isWon else 10


		return [self.state, reward, isWon, None]

	def reset(self):
		self.state = [[Case(7,'w'),Case(8,'w'),Case(9,'w')],[Case(4,'w'),Case(5,'o'),Case(6,'b')],[Case(1,'b'),Case(2,'b'),Case(3,'b')]]
		self.neighbors = [(4,2),(1,3),(2,6),(1,7),None,(3,9),(4,8),(7,9),(6,8)]
		self.turn = 'b'
		self.counter = 0
		self.reward = 0
		return self.state

	def render(self):
		for row in self.state :
			print(row[0].color + ' ' + row[1].color + ' ' + row[2].color)

	def actionSpaceSample(self):
		return np.random.choice(self.possibleActions)

	def otherPlayer(self,player):
		if player == 'b':
			return 'w'
		else :
			return 'b'
