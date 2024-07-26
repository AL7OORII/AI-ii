import random
import copy
import matplotlib.pyplot as plt
import time

GENS = 100
P = 100
N = 20
MUTRATE = 0.03
MUTSTEP = 0.3
MAX = 10
MIN = -10

# Initialize a list to store fitness values
fitness_values = []
smallest_fitness = []
average_fitness = []

class individual:
    def __init__(self):
        self.gene = [0] * N
        self.fitness = 0

def test_function(ind):
    n = len(ind.gene)
    result = (ind.gene[0] - 1) ** 2
    for i in range(1, n):
       result += (i+1) * ((2 * ind.gene[i] ** 2) - ind.gene[i-1]) ** 2
    return result

population = []

for x in range(0, P):
    tempgene = []
    for y in range(0, N):
        tempgene.append(random.uniform(MIN, MAX))
    newind = individual()
    newind.gene = tempgene.copy()
    population.append(newind)
    fitness_values.append(newind.fitness)

# Calculate fitness for each individual in the population:
for i in range(P):
    population[i].fitness = test_function(population[i])

start_time = time.time()  # Record the start time

for g in range(0, GENS):
    offspring = []

    # performing a selection:
    for i in range(0, P):
        parent1 = random.randint(0, P - 1)
        off1 = copy.deepcopy(population[parent1])
        parent2 = random.randint(0, P - 1)
        off2 = copy.deepcopy(population[parent2])
        if off1.fitness < off2.fitness:
            offspring.append(off1)
        else:
            offspring.append(off2)

    # two-point crossover implementation:
    toff1 = individual()
    toff2 = individual()
    temp = individual()
    for i in range(0, P, 2):
        toff1 = copy.deepcopy(offspring[i])
        toff2 = copy.deepcopy(offspring[i + 1])
        temp = copy.deepcopy(offspring[i])
        crosspoint1 = random.randint(1, N - 1)
        crosspoint2 = random.randint(crosspoint1 + 1, N)
        for j in range(crosspoint1, crosspoint2):
            toff1.gene[j] = toff2.gene[j]
            toff2.gene[j] = temp.gene[j]
        offspring[i] = copy.deepcopy(toff1)
        offspring[i + 1] = copy.deepcopy(toff2)

    # Mutation implementation:
    for i in range( 0, P ):
          newind = individual()
          newind.gene = []
          for j in range( 0, N ):
                    gene = offspring[i].gene[j]
                    mutprob = random.random()
                    if mutprob < MUTRATE:
                            alter = random.uniform(-MUTSTEP,MUTSTEP)
                            gene = gene + alter
                            if gene > MAX:
                                    gene = MAX
                            if gene < MIN:
                                    gene = MIN
                    newind.gene.append(gene)
          offspring[i] = copy.deepcopy(newind)


    for ind in offspring:
        ind.fitness = test_function(ind)

    # Update the population with the mutated individuals
    population = copy.deepcopy(offspring)

    # Calculate and print best, average, and worst fitness
    fitness_values = [ind.fitness for ind in population]
    smallest_fitness.append(min(fitness_values))
    average_fitness.append(sum(fitness_values) / len(fitness_values))  

     # Implement elitism: Find the best individual from the current population
    best_individual = max(population, key=lambda ind: ind.fitness)
    
    # Find the position of the worst individual in the new offspring
    worst_index = fitness_values.index(min(fitness_values))
    
    # Copy the best individual from the previous generation over the worst individual in the offspring
    offspring[worst_index] = copy.deepcopy(best_individual)      

    print(f"Generation {g}:")
    print(f"Smallest Fitness: {smallest_fitness[-1]}")
    print(f"Average Fitness: {average_fitness[-1]}")

end_time = time.time()  # Record the end time

# Print the execution time
print(f"Total Execution Time: {end_time - start_time} seconds")

# Plot the fitness values across generations
plt.plot(smallest_fitness, label="Smallest Fitness")
plt.plot(average_fitness, label="Average Fitness")
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.legend()
plt.title("Fitness over the Generations")
plt.show()
