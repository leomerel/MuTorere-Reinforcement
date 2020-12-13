# Mu Torere
Within the scope of an artificial intelligence project in the 5th year of the National School of Engineering of Brest, we realized an agent learning to play Mu Torere.

The Mu Torere is a New Zealand board game. Played by two players, this game is made of 9 knots, 1 empty, 4 white and 4 black.

![initial state of MuTorere board](https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Mu_Torere.svg/1200px-Mu_Torere.svg.png =250x)
### Rules
Each player controls four counters which are initially placed on the board . At the beginning of the game the  middle point is empty. (See illustration.)

Players move one of their counters per turn to an empty point. Players can move only to an adjacent knot, and can move to the center point  only when the moved counter is adjacent to an opponent's counter. The player who blocks all the opponent's counters from moving is the winner.

### Reinforcment learning
In order for our agent to learn how to play the game correctly, we used reinforcment learning. Playing randomly at first, the program then earn cumulative rewards depending of the results of his actions.

As games are played, the agent will then use the collected information to choose the most rewarding action according to the state it is in.

In the end, it is able to choose the actions that will lead him to victory when it is pitted many games in a row against a player repeating random actions.

We deliberately chose not to pit two AI against each other. First of all, it allows us to see very clearly the effectiveness of our agent's learning. Secondly, since Mu Torere is a game with simple rules, two players which don't make mistakes can play indefinitely without ever finishing the game.

## The Game
The program MuToReRe.py available at the root of the project is a game for two human players, in order to understand the rules and how the game works. The user can move his counters by selecting the number of his knot with the corresponding key on the numeric keypad.

## The AI Environnement
The environnement in which the agent works is defined according to the same rules :  [Mutorere_Gym_Env/gym-mutorere/gym_mutorere/envs/**mutorere_env.py**](https://git.enib.fr/t6lepoit/mu-torere-reinforcement/-/tree/master/Mutorere_Gym_Env/gym-mutorere/gym_mutorere/envs)

## The Agent
The AI can be started using this file : [Mutorere_Gym_Env/gym-mutorere/**myAgent.py**](https://git.enib.fr/t6lepoit/mu-torere-reinforcement/-/tree/master/Mutorere_Gym_Env/gym-mutorere) with python 3.

On start, the agent is learning how to play the game with randomly selected actions for 2500 games.

As we can see, the time it takes for the ia to win the game reduces considerably. The graph displayed at the end of the execution allows you to see the evolution of the rewards earned by the agent over the course of the games.

## Results
In order to evaluate our agent's performance, we used, among other things, the rewards earned in each epoch.

![Graph of reward per epoch on 10000 games](https://git.enib.fr/t6lepoit/mu-torere-reinforcement/-/raw/master/images/grande_zone.png)

Especially when learning, we can notice the obvious differences between the randomly played turns and those using the Q_table.

![Graph of reward per epoch on the 2500 learning games](https://git.enib.fr/t6lepoit/mu-torere-reinforcement/-/raw/master/images/apprentissage.png)

Finally, once exploration rate is reduced to a minimum, the agent succeeds in winning all parties. Since the random player does not have many options, it is very easy for our agent to choose the winning strategy. We can still note a few games extending more rounds in this sample of 100 games. Thanks to the reward mean, and knowing the agent loose 1 reward per turn but earn 50 when it wins the game, we can tell the average game is finished in 8 turns.

![Graph of reward per epoch on a sample of 100 games](https://git.enib.fr/t6lepoit/mu-torere-reinforcement/-/raw/master/images/resultats.png)
