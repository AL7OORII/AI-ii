import random
import matplotlib.pyplot as plt
import time

N = 20
LOOPS = 10000

class Solution:
    def __init__(self):
        self.variable = [0] * N
        self.utility = 0

def test_function(ind):
    n = len(ind.variable)
    result = (ind.variable[0] - 1) ** 2
    for i in range(1, n):
        result += (i + 1) * ((2 * ind.variable[i] ** 2) - ind.variable[i - 1]) ** 2
    return result

individual = Solution()

# Initialize the individual's variables randomly
for j in range(N):
    individual.variable[j] = random.uniform(-10, 10)
individual.utility = test_function(individual)

def hill_climber(individual, test_function, loops):
    start_time = time.time()  # Record the start time
    utilities = []  # To store utilities for plotting
    for x in range(loops):
        new_ind = Solution()
        new_ind.variable = individual.variable.copy()

        change_point = random.randint(0, N - 1)
        new_ind.variable[change_point] = random.uniform(-10, 10)
        new_ind.utility = test_function(new_ind)

        if individual.utility >= new_ind.utility:
            individual.variable[change_point] = new_ind.variable[change_point]
            individual.utility = new_ind.utility

        utilities.append(individual.utility)  # Store the utility for plotting

    end_time = time.time()  # Record the end time

    # Print the final solution
    print("\nFinal Solution:")
    print("Variables:", individual.variable)
    print("Utility:", individual.utility)

    # Print the execution time
    print(f"Execution Time: {end_time - start_time} seconds")

    # Plot the utility values across iterations
    plt.plot(range(1, loops + 1), utilities, label="Utility")
    plt.xlabel("Iteration")
    plt.ylabel("Utility")
    plt.legend()
    plt.title("Utility over Iterations")
    plt.show()

# Perform hill climbing
hill_climber(individual, test_function, LOOPS)
