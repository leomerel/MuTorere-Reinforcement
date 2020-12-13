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
	agentTotalRewards = np.zeros(numGames)
	agentVictories = 0
	randomPlayerVictories = 0

	startTime = time.time()
	for i in range(numGames):
		if i < 1000 :
			if i %100 == 0 :
				print('starting game ', i, " (took ", round(time.time()-startTime,2), "s)", sep = '')
				startTime = time.time()
		else :
			if i %1000 == 0 :
				print('starting game ', i, " (took ", round(time.time()-startTime,2), "s)", sep = '')
				startTime = time.time()

		agentWon = False
		agentEpRewards = 0
		observation = env.reset()
		observation = stateToString(observation)
		turn = 0


		while not agentWon:

			if turn > 2000 :
				break
			rand = np.random.random()

			# print("start AI turn")
			turn +=1
			agentAction = maxAction(Qb,observation, env.possibleActions) if rand < (1-EPS) \
													else env.randomAction()

			#The agent tries to make a move
			observation_, agentReward, agentWon, agentHasPlayed = env.step(int(agentAction),'b')
			observation_ = stateToString(observation_)

			if agentHasPlayed and not agentWon:
				randomPlayerAction = env.randomAction()

				while not env.checkMove('w',int(randomPlayerAction)):
					randomPlayerAction = env.randomAction()

				#The random player makes his random move
				observation_, randomPlayerReward, randomPlayerWon, randomPlayerHasPlayed = env.step(int(randomPlayerAction),'w')
				observation_ = stateToString(observation_)

				if randomPlayerWon :
					agentReward -= 50
				turn += 1

			agentEpRewards += agentReward

			#Get the best possible action given the current state (after both players played)
			agentAction_ = maxAction(Qb, observation_, env.possibleActions)

			#Update the Q-table
			Qb[observation,agentAction] = Qb[observation,agentAction] + ALPHA*(agentReward + \
						GAMMA*Qb[observation_,agentAction_] - Qb[observation,agentAction])

			observation = observation_

		if EPS - 2 / 5000 > 0:
			EPS -= 2 / 5000
		else:
			if agentWon :
				agentVictories += 1
			elif randomPlayerWon :
				randomPlayerVictories +=1
			EPS = 0

		agentTotalRewards[i] = agentEpRewards

	#Display results
	print()
	print("AI won", agentVictories, "times.")
	print("Random player won", randomPlayerVictories, "times.")
	print("AI has a winrate of", randomPlayerVictories/agentVictories if randomPlayerVictories!=0 else 100, "%")

	plt.plot(agentTotalRewards[:len(moving_average(agentTotalRewards,500))], marker='.', linestyle='',label='total reward per epoch')
	plt.plot(moving_average(agentTotalRewards,500),label = 'reward mean')
	plt.legend(loc='center right')
	plt.xlabel('epoch')
	plt.ylabel('reward')
	plt.show()
