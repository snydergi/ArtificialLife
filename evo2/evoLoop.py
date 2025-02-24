# from diffmpmLab3 import main as live
import subprocess
import random
import ast
import re

def evaluate_fitness(params):
    """
    Evaluate the fitness of a set of parameters by running the script.

    Args:
        params (dict): Dictionary of parameters to pass to the script.

    Returns:
        float: Fitness value (e.g., final loss).
    """
    # Construct the command to run the script
    command = [
        "/home/gis/Documents/ArtificialLife/difftaichiVenv/bin/python3",
        "/home/gis/Documents/ArtificialLife/alifegh/evo2/diffmpmLab3.py",
        "--numVertebrae", str(params["numVertebrae"]),
        "--vertebraeRadius", str(params["vertebraeRadius"]),
        "--numLegs", str(params["numLegs"]),
        "--numLegSegments", str(params["numLegSegments"]),
        "--legLength", str(params["legLength"]),
        "--iters", str(params["iters"])
    ]

    # Run the script
    result = subprocess.run(command, capture_output=True, text=True)

    # Check if the script ran successfully
    if result.returncode != 0:
        print(f"Error running script: {result.stderr}")
        return float('inf')  # Return a high loss value to indicate failure

    # Extract the final loss from the output
    output = result.stdout
    for line in output.splitlines():
        if "Final Loss:" in line:
            final_loss = float(line.split(":")[1].strip())
            return final_loss

    # If the final loss is not found, return a high loss value
    print("Final loss not found in output.")
    return float('inf')


def evolutionary_algorithm():
    """
    Simple evolutionary algorithm to optimize parameters.
    Ensures all parameters are greater than zero.
    """
    # Initial population
    population = [
        {
            "numVertebrae": random.randint(2, 10),  # Already >= 2
            "vertebraeRadius": max(0.005, random.uniform(0.005, 0.05)),  # Ensure > 0
            "numLegs": random.randint(1, 6),  # Ensure >= 1
            "numLegSegments": random.randint(1, 5),  # Ensure >= 1
            "legLength": max(0.01, random.uniform(0.01, 0.05)),  # Ensure > 0
            "iters": 100
        }
        for _ in range(10)  # Population size
    ]

    # Evolution loop
    for generation in range(10):  # Number of generations
        print(f"Generation {generation + 1}")

        # Evaluate fitness for each individual
        fitness_scores = []
        for individual in population:
            fitness = evaluate_fitness(individual)
            fitness_scores.append(fitness)
            print(f"Parameters: {individual}, Fitness: {fitness}")

        # Select the best individuals (e.g., top 50%)
        sorted_population = [x for _, x in sorted(zip(fitness_scores, population),
                                                  key=lambda pair: pair[0])]
        population = sorted_population[:len(population) // 2]

        # Create new generation through mutation
        new_population = []
        for individual in population:
            # Mutate parameters with constraints
            mutated_individual = {
                "numVertebrae": max(1, individual["numVertebrae"] +
                                    random.randint(-1, 1)),  # Ensure >= 1
                "vertebraeRadius": max(0.005, individual["vertebraeRadius"] +
                                       random.uniform(-0.1, 0.1)),  # Ensure > 0
                "numLegs": max(1, individual["numLegs"] + random.randint(-1, 1)),  # Ensure >= 1
                "numLegSegments": max(1, individual["numLegSegments"] +
                                      random.randint(-1, 1)),  # Ensure >= 1
                "legLength": max(0.01, individual["legLength"] +
                                 random.uniform(-0.1, 0.1)),  # Ensure > 0
                "iters": 100
            }
            new_population.append(mutated_individual)

        population.extend(new_population)

    print("Evolution complete.")


if __name__ == '__main__':
    evolutionary_algorithm()