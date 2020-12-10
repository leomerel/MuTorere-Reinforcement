# Mu Torere
Within the scope of an artificial intelligence project in the 5th year of the National School of Engineering of Brest, we realized an agent learning to play Mu Torere.

The Mu Torere is a New Zealand board game. Played by two players, this game is made of 9 knots, 1 empty, 4 white and 4 black.

![initial state of MuTorere board](https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Mu_Torere.svg/1200px-Mu_Torere.svg.png)
### Rules
Each player controls four counters which are initially placed on the board . At the beginning of the game the  middle point is empty. (See illustration.)

Players move one of their counters per turn to an empty point. Players can move only to an adjacent knot, and can move to the center point  only when the moved counter is adjacent to an opponent's counter. The player who blocks all the opponent's counters from moving is the winner.

### Reinforcment learning
In order for our agent to learn how to play the game correctly, we used reinforcment learning. Playing randomly at first, the program then earn cumulative rewards depending of the results of his actions.

As games are played, the agent will then use the collected information to choose the most rewarding action according to the state it is in.

In the end, it is able to choose the actions that will lead him to victory when it is pitted many games in a row against a player repeating random actions.

## The Game
The program MuToReRe.py available at the root of the project is a game for two human players, in order to understand the rules and how the game works. The user can move his counters by selecting the number of his knot with the corresponding key on the numeric keypad.

## The AI Environnement
The environnement in which the agent works is defined according to the same rules :  [Mutorere_Gym_Env/gym-mutorere/gym_mutorere/envs/**mutorere_env.py**](https://git.enib.fr/t6lepoit/mu-torere-reinforcement/-/tree/master/Mutorere_Gym_Env/gym-mutorere/gym_mutorere/envs)

## The Agent
The AI can be started using this file : [Mutorere_Gym_Env/gym-mutorere/**myAgent.py**](https://git.enib.fr/t6lepoit/mu-torere-reinforcement/-/tree/master/Mutorere_Gym_Env/gym-mutorere) with python 3.
