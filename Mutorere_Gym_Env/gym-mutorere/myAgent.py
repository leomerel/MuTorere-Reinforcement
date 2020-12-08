import gym
import gym_mutorere
import numpy as np

env = gym.make('mutorere-v0')

env.reset() # reset environment to a new, random state
env.render()

def maxAction(Q, state, actions):
	values = np.array([Q[state,a] for a in actions])
	action = np.argmax(values)
	return actions[action]

if __name__ == '__main__':

	# model hyperparameters
	ALPHA = 0.1
	GAMMA = 1.0
	EPS = 1.0

	Qw = {}
	Qb = {}
	# for state in env.stateSpacePlus:
	#     for action in env.possibleActions:
	#         Q[state, action] = 0

	numGames = 5000
	totalRewardsWhite = np.zeros(numGames)
	totalRewardsBlack = np.zeros(numGames)
	for i in range(numGames):
		if i % 1000 == 0:
			print('starting game ', i)
		done = False
		player = 'w'
		epRewardsWhite = 0
		epRewardsBlack = 0
		observation = env.reset()
		while not done:
			rand = np.random.random()
			if player == 'b' :
				action = maxAction(Qb,observation, env.possibleActions) if rand < (1-EPS) \
														else env.actionSpaceSample()

				while not env.checkMove(player,int(action)):
					epRewardsBlack -= 5
					action = maxAction(Qb,observation, env.possibleActions) if rand < (1-EPS) \
															else env.actionSpaceSample()

				observation_, reward, done, info = env.step(int(action),player)
				epRewardsBlack += reward

				action_ = maxAction(Qb, observation_, env.possibleActions)
				Qb[observation,action] = Qb[observation,action] + ALPHA*(reward + \
							GAMMA*Qb[observation_,action_] - Qb[observation,action])
				observation = observation_
			else :
				action = maxAction(Qw,observation, env.possibleActions) if rand < (1-EPS) \
														else env.actionSpaceSample()
				observation_, reward, done, info = env.step(int(action),player)
				epRewardsWhite += reward

				action_ = maxAction(Qw, observation_, env.possibleActions)
				Qw[observation,action] = Qw[observation,action] + ALPHA*(reward + \
							GAMMA*Qw[observation_,action_] - Qw[observation,action])
				observation = observation_

		if EPS - 2 / numGames > 0: #exploration rate (plus il y a de games plus la q table est utilisée)
			EPS -= 2 / numGames
		else:
			EPS = 0
		totalRewardsWhite[i] = epRewardsWhite
		totalRewardsBlack[i] = epRewardsBlack

	fig1 = plt.fig()
	fig1.plot(totalRewardsWhite)

	fig2 = plt.fig()
	fig2.plot(totalRewardsBlack)
