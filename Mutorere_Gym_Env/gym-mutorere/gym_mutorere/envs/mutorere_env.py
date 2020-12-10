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

		# Initialisation de la liste des états
		self.stateSpacePlus = []
		colorList = ['o','b','w']

		#case 1
		for a in colorList:
			#case 2
			for b in colorList :
				#case 3
				for c in colorList :
					#case 4
					for d in colorList :
						#case 5
							for e in colorList:
								#case 6
								for f in colorList :
									#case 7
									for g in colorList :
										#case 8
										for h in colorList :
											#case 9
											for i in colorList :

												countList = [a,b,c,d,e,f,g,h,i]

												if countList.count('o') != 1 :
													continue

												if countList.count('b') != 4 :
													continue

												if countList.count('w') != 4 :
													continue

												self.stateSpacePlus.append([[Case(7,g),Case(8,h),Case(9,i)],[Case(4,d),Case(5,e),Case(6,f)],[Case(1,a),Case(2,b),Case(3,c)]])

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
			#print("id not between 1 and 9")
			return False

		case = self.searchCaseById(id)

		if id != 5 :
			neighbors = (self.searchCaseById(self.neighbors[id-1][0]),self.searchCaseById(self.neighbors[id-1][1]))

		if player != self.turn :
			#print("not your turn", player, self.turn)
			return False

		if player != case.color :
			#print("wrong color", player, case.color)
			return False

		if case.id != 5 :
			if not self.checkNeighbors(case.id) :
				#print("both neighbors are the same color", player, self.searchCaseById(id).color, self.searchCaseById(self.neighbors[id-1][1]).color, self.searchCaseById(self.neighbors[id-1][0]).color)
				return False

		if id != 5 :
			if self.state[1][1].color != 'o' and neighbors[0].color != 'o' and neighbors[1].color != 'o' :
				#print("no empty neighbors", player, self.state[1][1].color, neighbors[0].color, neighbors[1].color)
				return False

		return True

	def checkEndConditions(self,player):
		canMove = False
		for i in range(1,10) :
			canMove |= self.checkMove(player,i)
		return canMove

	def step(self, id, player):
		case = self.searchCaseById(id)

		isPossible = self.checkMove(player,id)

		if isPossible :
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


			self.turn = self.otherPlayer(player)

			isWon = not self.checkEndConditions(self.otherPlayer(player))
			reward = -1 if not isWon else 50

			#print("Possible")
			return [self.state, reward, isWon, isPossible]
		else :
			self.turn = self.otherPlayer(player)
			isWon = not self.checkEndConditions(self.otherPlayer(player))
			self.turn = player
			#print("Not possible")
			reward = -5

			return [self.state, reward, isWon, isPossible]

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
