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
	GAMMA = 0.95
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
		#if i < 100 :
			#print("starting game ", i, time.time()-startTime)
			#startTime = time.time()
		if i < 1000 :
			if i %100 == 0 :
				print('starting game ', i, time.time()-startTime)
				startTime = time.time()
		else :
			if i %1000 == 0 :
				print('starting game ', i, time.time()-startTime)
				startTime = time.time()
		done = False
		epRewardsWhite = 0
		epRewardsBlack = 0
		observation = env.reset()
		observation = stateToString(observation)
		turn = 0


		while not done:

			if turn > 2000 :
				break
			rand = np.random.random()

			# print("start AI turn")
			turn +=1
			#print()
			action = maxAction(Qb,observation, env.possibleActions) if rand < (1-EPS) \
													else env.actionSpaceSample()

			#print("turn: ",turn)
			#print(action)

			observation_, reward, done, info = env.step(int(action),'b')
			observation_ = stateToString(observation_)

			if done :
				AIwins += 1
				info = False

			#env.render()
			# print()

			if info :
				#Playing randomly
				randomAction = env.actionSpaceSample()

				while not env.checkMove('w',int(randomAction)):
					randomAction = env.actionSpaceSample()

				observation_, randomReward, randone, randomInfo = env.step(int(randomAction),'w')
				observation_ = stateToString(observation_)

				if randone :
					RandomWins +=1
					reward -= 50
				turn += 1

			epRewardsBlack += reward
			action_ = maxAction(Qb, observation_, env.possibleActions)
			Qb[observation,action] = Qb[observation,action] + ALPHA*(reward + \
						GAMMA*Qb[observation_,action_] - Qb[observation,action])
			observation = observation_

		if EPS - 2 / 5000 > 0: #exploration rate (plus il y a de games plus la q table est utilisée)
			EPS -= 2 / 5000
		else:
			EPS = 0
		totalRewardsWhite[i] = epRewardsWhite
		totalRewardsBlack[i] = epRewardsBlack

	print()
	print("AI ", AIwins)
	print("Random ", RandomWins)

	plt.plot(totalRewardsBlack)
	plt.show()
