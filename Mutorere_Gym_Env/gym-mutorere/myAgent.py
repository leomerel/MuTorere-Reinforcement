import gym
import gym_mutorere
import numpy as np
import matplotlib.pyplot as plt
import time

env = gym.make('mutorere-v0')

env.reset() # reset environment to a new, random state

def maxAction(Q, state, actions):
	#chooses the action that has the highest reward value
	values = np.array([Q[state,a] for a in actions])
	action = np.argmax(values)
	return actions[action]

def stateToString(state):
	strState = ""
	for row in state :
		for case in row :
			strState += case.color

	return strState

def moving_average(a, n=100) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

if __name__ == '__main__':

	# model hyperparameters
	ALPHA = 0.1
	GAMMA = 0.95
	EPS = 1.0

	numGames = 10000

	#initialisation of the Q-table
	Qb = {}
	for state in env.stateSpacePlus:
		for action in env.possibleActions:
			Qb[stateToString(state), action] = 0

	#storing data to display statistics and graphs in the end
	totalRewardsBlack = np.zeros(numGames)
	AIwins = 0
	RandomWins = 0

	startTime = time.time()
	for i in range(numGames):
		if i < 1000 :
			if i %100 == 0 :
				print('starting game ', i, time.time()-startTime)
				startTime = time.time()
		else :
			if i %1000 == 0 :
				print('starting game ', i, time.time()-startTime)
				startTime = time.time()

		blackVictory = False
		epRewardsBlack = 0
		observation = env.reset()
		observation = stateToString(observation)
		turn = 0


		while not blackVictory:

			if turn > 2000 :
				break
			rand = np.random.random()

			# print("start AI turn")
			turn +=1
			action = maxAction(Qb,observation, env.possibleActions) if rand < (1-EPS) \
													else env.randomAction()

			observation_, blackReward, blackVictory, blackHasPlayed = env.step(int(action),'b')
			observation_ = stateToString(observation_)

			if blackVictory :
				blackHasPlayed = False

			if blackHasPlayed :
				#Playing randomly
				randomAction = env.randomAction()

				while not env.checkMove('w',int(randomAction)):
					randomAction = env.randomAction()

				observation_, randomReward, randone, randomInfo = env.step(int(randomAction),'w')
				observation_ = stateToString(observation_)

				if randone :
					blackReward -= 50
				turn += 1

			epRewardsBlack += blackReward
			action_ = maxAction(Qb, observation_, env.possibleActions)
			Qb[observation,action] = Qb[observation,action] + ALPHA*(blackReward + \
						GAMMA*Qb[observation_,action_] - Qb[observation,action])
			observation = observation_

		if EPS - 2 / 5000 > 0:
			EPS -= 2 / 5000
		else:
			if blackVictory :
				AIwins += 1
			elif randone :
				RandomWins +=1
			EPS = 0

		totalRewardsBlack[i] = epRewardsBlack
		if i % 100 == 0 and i != 0:
			mean = np.mean(totalRewardsBlack[(i-100):(i)])


	print()
	print("AI ", AIwins)
	print("Random ", RandomWins)
	print("Winrate ", RandomWins/AIwins if RandomWins!=0 else 100, "%")


	plt.plot(totalRewardsBlack[:len(moving_average(totalRewardsBlack,500))], marker='.', linestyle='',label='total reward per epoch')
	plt.plot(moving_average(totalRewardsBlack,500),label = 'reward mean')
	plt.legend(loc='center right')
	plt.xlabel('epoch')
	plt.ylabel('reward')
	plt.show()
