# Picobot-AI

This Python program will automatically evolve better Picobot programs with artificial intelligence using a genetic algorithm.
 
## What is Picobot?
Picobot is a program created by Harvey Mudd College. Its goal is to completely traverse its environment. Picobot starts at a random location in a room. The walls of the room are blue, picobot is green, and the empty room is white. Every time Picobot takes a step, it leaves a gray trail.

A Picobot program is simply a list of rules of the form `0 xxxx -> N 0` ,  every rule follows this pattern of `startingState   NEWSsurroundings   ->  moveDirection   nextState
`

The Picobot program can be found here: https://www.cs.hmc.edu/picobot/


## How does this AI work?
This artificial intelligence (AI) uses a genetic algorithm to evolve the Picobot programs. The AI works by first generating a random population, it then calculates the fitness per program which is saved in the `evaluated_fitnesses` list together with the corresponding program. To calculate the survivors, the `evaluated_fitnesses` list is first sorted and then reversed so the best programs will be at the beginning. By slicing this list using the `SURVIVOR_FRACTION`, a new list of `survivors` is created. These are used as "parents" for the next generation. The surviving programs are then supplemented with "children", new programs. Each time 2 random "parents" are picked from the `survivors` list, who then are used to generate "children" using `crossover()`. Then there is still a chance that the programs will mutate, this depends on the `MUTATION_RATE`. At the end the best program will be printed together with its fitness value.

## Usage
This AI can be run using `genetic_algorithm(pop_size, num_gens)` where `pop_size` is the population size and `num_gens` is the number of generations. 

## Example
Here is an example of this program using 5 generations: 
![](/screenshots/example.png)

Fittest Picobot program with a fitness of 1 which completely solves the first room:
```
0 NExx -> S 4
0 NxWx -> E 2
0 Nxxx -> S 3
0 xExS -> W 3
0 xExx -> S 3
0 xxWS -> E 0
0 xxWx -> N 3
0 xxxS -> E 0
0 xxxx -> W 0
1 NExx -> W 1
1 NxWx -> S 2
1 Nxxx -> S 0
1 xExS -> N 3
1 xExx -> W 1
1 xxWS -> N 1
1 xxWx -> E 3
1 xxxS -> W 4
1 xxxx -> W 1
2 NExx -> W 0
2 NxWx -> E 3
2 Nxxx -> E 2
2 xExS -> N 4
2 xExx -> S 1
2 xxWS -> E 4
2 xxWx -> S 3
2 xxxS -> W 2
2 xxxx -> E 2
3 NExx -> W 1
3 NxWx -> E 2
3 Nxxx -> W 2
3 xExS -> N 3
3 xExx -> S 2
3 xxWS -> E 0
3 xxWx -> E 2
3 xxxS -> N 4
3 xxxx -> W 2
4 NExx -> S 4
4 NxWx -> E 1
4 Nxxx -> E 0
4 xExS -> N 0
4 xExx -> W 0
4 xxWS -> E 1
4 xxWx -> S 4
4 xxxS -> E 3
4 xxxx -> N 4
```
***
This program was written by [Aji](https://github.com/securaji) and [Bastiaan](https://github.com/ezelbanaan).
