#
#   From: Aji & Bastiaan 
#   Date: 22-1-2021
#

import random
import copy

#
# Global variables
#
HEIGHT = 25
WIDTH = 25
NUM_STATES = 5
POSSIBLE_MOVES = ["xxxx", "Nxxx", "NExx", "NxWx", "xxxS", "xExS", "xxWS", "xExx", "xxWx"]
POSSIBLE_DIRECTIONS = ["N", "E", "W", "S"]

# Global variables for artificial intelligence
TESTS = 20
STEPS = 800
SURVIVOR_FRACTION = 0.1
MUTATION_RATE = 0.3

# Class Program
#
class Program(object):
    """A data type representing picobot code.
    """    
    def __init__(self, rules=None):
        """Construct objects of type Program.
        """
        if(rules == None):
            self.rules = {}
            self.randomize()
        else:
            self.rules = rules
            
    def __repr__(self):
        """This method returns a string representation
           for an object of type Program.
        """
        keys = list(self.rules.keys())
        sorted_keys = sorted(keys)
        rules = ""
        for key in sorted_keys:
            rules += str(key[0]) + ' ' + key[1] + ' ' + "->"+ ' ' + self.rules[key][0]+ ' ' + str(self.rules[key][1]) + '\n'
        return rules

    def randomize(self):
        """Generates 45 random picobot commands and stores them in self.rules
        """
        for state in range(NUM_STATES):
            for pattern in POSSIBLE_MOVES:
                movedir = random.choice(POSSIBLE_DIRECTIONS)
                next_state = random.choice(range(NUM_STATES))
                while movedir in pattern:
                    movedir = random.choice(POSSIBLE_DIRECTIONS)
                self.rules[(state, pattern)] = (movedir, next_state)
    
    def __gt__(self, other):
        """Greater-than operator -- works randomly, but works!"""
        return random.choice([True, False])

    def __lt__(self, other):
        """Less-than operator -- works randomly, but works!"""
        return random.choice([True, False])


    def get_move(self, state, surroundings):
        """Returns the move from the dictionary self.rules for state, surroundings
        """
        return self.rules[(state, surroundings)]

    def mutate(self):
        """Chooses a random rule and changes the direction and state for that rule
        """
        random_rule = random.choice(list(self.rules.keys()))
        move = self.rules[random_rule]
        newmove = move 
        random_state = random.choice(range(NUM_STATES))
        
        while move == newmove:
            random_direction = random.choice(POSSIBLE_DIRECTIONS)
            while random_direction in random_rule[1]:
                random_direction = random.choice(POSSIBLE_DIRECTIONS)

            newmove = (random_direction, random_state)
        
        self.rules[random_rule] = newmove

    def crossover(self, other):
        """Creates a "child" from self and other by combining there rules
        """
        cross = random.randint(1, 3)
        nd = {}
        for x in POSSIBLE_MOVES:
            for i in range(cross+1):
               nd[(i, x)] = self.rules[i, x]

        for x in POSSIBLE_MOVES:
            for i in range(cross+1, NUM_STATES):
                nd[(i, x)] = other.rules[i, x]
            
        np = Program(nd)
        return(np)

class World(object):
    """A datatype representing a picobot game
    """
    def __init__(self, initial_row, initial_col, program):
        """Construct objects of type Board, with the given width and height
        """
        self.prow = initial_row
        self.pcol = initial_col
        self.state = 0
        self.prog = program
        self.room = [['|'] + [' '] * (WIDTH-2) + ['|'] for row in range(HEIGHT)]
        self.room[0] = ['+'] + ['-'] * (WIDTH-2) + ['+']
        self.room[-1] = ['+'] + ['-'] * (WIDTH-2) + ['+']
        self.room[self.prow][self.pcol] = 'P'

    def __repr__(self):
        """This method returns a string representation
           for an object of type Board
        """
        s = ''
        for row in range(HEIGHT):
            for col in range(WIDTH):
                s += self.room[row][col] + ' '
            s+= '\n'
        return s       # The board is complete, return

    def get_current_surroundings(self):
        """Returns the current surroundings of self in picobot format
        """
        s = ''
        # Checks north
        if self.room[self.prow - 1][self.pcol] == '-':
            s += 'N'
        else:
            s += 'x'
        
        # Checks east
        
        if self.room[self.prow][self.pcol + 1] == '|':
            s += 'E'
        else:
            s += 'x'
        
        # Checks west
        
        if self.room[self.prow][self.pcol - 1] == '|':
            s += 'W'
        else:
            s += 'x'

        # Checks south
        if self.room[self.prow + 1][self.pcol] == '-':
            s += 'S'
        else:
            s += 'x'

        return s

    def step(self):
        """Moves the game 1 step further
        """
        orow = copy.copy(self.prow)
        ocol = copy.copy(self.pcol)

        cs = self.get_current_surroundings()
        nm, ns = self.prog.get_move(self.state, cs)
    
        self.state = ns
        if nm == 'N':
            self.prow -= 1
        elif nm == 'E':
            self.pcol += 1
        elif nm == 'W':
            self.pcol -= 1
        elif nm == 'S':
            self.prow += 1
        
        self.room[orow][ocol] = 'o'
        self.room[self.prow][self.pcol] = 'P'

    def run(self, steps):
        """Moves the game the given ammount of steps further
        """
        for i in range(steps):
            self.step()

    def fraction_visited_cells(self):
        """Returns the fraction of the ammount of visited cells
        """
        total = (WIDTH-2) * (HEIGHT-2)
        count = 0
        for row in range(1, HEIGHT-1):
            for col in range(1, WIDTH-1):
                if self.room[row][col] == 'o' or self.room[row][col] == 'P':
                    count += 1
        return count / total

def save_to_file(filename, p):
    """Saves the data from Program p
       to a file named filename."""
    f = open(filename, 'w')
    print(p, file=f)        # Prints the picobot program using the __repr__
    f.close()

def evaluate_fitness(program, trials, steps):
    """Tests the program given trails ammount of times by allowing it to move only a 
       certain ammount of steps and returns the average fitness.
    """
    average = 0
    for trail in range(trials):
        r_row = random.choice(range(1, HEIGHT-1))
        r_col = random.choice(range(1, WIDTH-1))
        world = World(r_row, r_col, program)
        world.run(steps)
        average += world.fraction_visited_cells()
    return average / trials
       
def genetic_algorithm(pop_size, num_gens):
    """Generates a pop_size ammount of random programs, then it wil decide who is the fitest and the 
       fittest few will be used to generate the new generation, with num_gens ammount of generations.
    """
    programs = []
    best_game = {}
    top_fitness = 0
    print(f"Fitness will be calculated with {TESTS} random tests and with {STEPS} steps a test:\n")

    # Generate the starting population
    for pop in range(pop_size):
        program = Program()
        programs.append(program)

    for gen in range(num_gens):
        evaluated_fitnesses = []
        
        # Calculate the fitness per program
        for program in programs:
            fitness = evaluate_fitness(program, TESTS, STEPS)
            evaluated_fitnesses.append((fitness, program))
        
        # Calculate the average fitness
        sum_fitness = 0
        for fitness in evaluated_fitnesses:
            sum_fitness += fitness[0]
        avg_fitness = sum_fitness / len(evaluated_fitnesses)

        # Define the highest fitness
        max_fitness = max(evaluated_fitnesses)[0]

        save_to_file("generation" + str(gen) + ".txt", max(evaluated_fitnesses)[1])

        # Calculate survivors
        evaluated_fitnesses.sort()
        evaluated_fitnesses.reverse()
        survivors = evaluated_fitnesses[:int(len(programs) * SURVIVOR_FRACTION)]

        # Checks if fitness is higher then the fitness of the last generation
        if max(evaluated_fitnesses)[0] > top_fitness:
            top_fitness = max(evaluated_fitnesses)[0]
            best_game[top_fitness] = survivors[0][1] 

        # Generate the next generation
        fit_programs = [program[1] for program in survivors]     
        new_programs = fit_programs
        for _ in range(pop_size - len(survivors)):
            program1 = random.choice(fit_programs)
            program2 = random.choice(fit_programs)
            new_program = program1.crossover(program2)
            if random.random() < MUTATION_RATE:
                new_program.mutate()
            new_programs.append(new_program)
        programs = new_programs

        print("Generation " + str(gen))
        print("  Average fitness:  " + str(avg_fitness))
        print("  Highest fitness:  " + str(max_fitness) + "\n")

    
    print(f"Best picobot program with a fitness of {str(top_fitness)}, saved to generation{num_gens-1}.txt:")
    return best_game[top_fitness]

if __name__ == '__main__':
    genetic_algorithm(200, 20)
