import gym
import gym_mutorere
import numpy as np
import matplotlib.pyplot as plt
import time

env = gym.make('mutorere-v0')

env.reset() # reset environment to a new, random state
# env.render()

def maxAction(Q, state, actions):
	values = np.array([Q[state,a] for a in actions])
	action = np.argmax(values)
	#if state == "wwwowbbbb":
		#print(values)
	# print("maxAction")
	return actions[action]

def stateToString(state):
	strState = ""
	for row in state :
		for case in row :
			strState += case.color

	return strState

if __name__ == '__main__':

	# model hyperparameters
	ALPHA = 0.1
	GAMMA = 1.0
	EPS = 1.0

	Qw = {}
	Qb = {}
	for state in env.stateSpacePlus:
		for action in env.possibleActions:
			Qw[stateToString(state), action] = 0
			Qb[stateToString(state), action] = 0

	numGames = 10000
	totalRewardsWhite = np.zeros(numGames)
	totalRewardsBlack = np.zeros(numGames)

	AIwins = 0
	RandomWins = 0
	startTime = time.time()
	for i in range(numGames):
		if i < 100 :
			#print("starting game ", i, time.time()-startTime)
			startTime = time.time()
		elif i < 1000 :
			if i %100 == 0 :
				#print('starting game ', i, time.time()-startTime)
				startTime = time.time()
		else :
			if i %1000 == 0 :
				print('starting game ', i, time.time()-startTime)
				startTime = time.time()
		done = False
		player = 'w'
		epRewardsWhite = 0
		epRewardsBlack = 0
		observation = env.reset()
		observation = stateToString(observation)
		turn = 0


		while not done:

			if turn > 500 :
				break
			rand = np.random.random()
			# print(rand)
			if player == 'b' :
				# print("start AI turn")
				turn +=1
				#print()
				action = maxAction(Qb,observation, env.possibleActions) if rand < (1-EPS) \
														else env.actionSpaceSample()

				#print("turn: ",turn)
				#print(action)

				# while not env.checkMove(player,int(action)):
				# 	epRewardsBlack -= 5
				# 	action = maxAction(Qb,observation, env.possibleActions) if rand < (1-EPS) \
				# 											else env.actionSpaceSample()
				#
				# 	print(action)


				observation_, reward, done, info = env.step(int(action),player)
				observation_ = stateToString(observation_)
				epRewardsBlack += reward

				action_ = maxAction(Qb, observation_, env.possibleActions)
				Qb[observation,action] = Qb[observation,action] + ALPHA*(reward + \
							GAMMA*Qb[observation_,action_] - Qb[observation,action])
				observation = observation_



				#env.render()
				# print()

				if info :
					player = 'w'

				if done :
					AIwins += 1


			else :
				#Playing randomly
				action = env.actionSpaceSample()

				while not env.checkMove(player,int(action)):
					action = env.actionSpaceSample()

				observation, reward, done, info = env.step(int(action),player)

				# env.render()
				# print()
				observation = stateToString(observation)

				# action = maxAction(Qw,observation, env.possibleActions) if rand < (1-EPS) \
				# 										else env.actionSpaceSample()
				#
				# while not env.checkMove(player,int(action)):
				# 	epRewardsWhite -= 5
				# 	action = maxAction(Qw,observation, env.possibleActions) if rand < (1-EPS) \
				# 											else env.actionSpaceSample()
				#
				# observation_, reward, done, info = env.step(int(action),player)
				# epRewardsWhite += reward
				#
				# action_ = maxAction(Qw, observation_, env.possibleActions)
				# Qw[observation,action] = Qw[observation,action] + ALPHA*(reward + \
				# 			GAMMA*Qw[observation_,action_] - Qw[observation,action])
				# observation = observation_

				if done :
					RandomWins +=1

				turn += 1
				player = 'b'

		if EPS - 2 / numGames > 0: #exploration rate (plus il y a de games plus la q table est utilisée)
			EPS -= 2 / numGames
		else:
			EPS = 0
		totalRewardsWhite[i] = epRewardsWhite
		totalRewardsBlack[i] = epRewardsBlack

	print()
	print("AI ", AIwins)
	print("Random ", RandomWins)

	plt.plot(totalRewardsBlack)
	plt.show()
