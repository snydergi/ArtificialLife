import subprocess
import random
import csv
import os

populationSize = 4


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
        "/home/gis/Documents/ArtificialLife/alifegh/evo3/diffmpmLab3.py",
        "--numVertebrae", str(params["numVertebrae"]),
        "--vertebraeRadius", str(params["vertebraeRadius"]),
        "--numLegs", str(params["numLegs"]),
        "--numLegSegments", str(params["numLegSegments"]),
        "--legLength", str(params["legLength"]),
    ]

    # Run the script
    result = subprocess.run(command, capture_output=True, text=True)

    # Extract the final loss from the output
    output = result.stdout
    for line in output.splitlines():
        if "Final Loss:" in line:
            final_loss = float(line.split(":")[1].strip())
            return final_loss

    # If the final loss is not found, return a high loss value
    print("Final loss not found in output.")
    return float('inf')


def read_population_from_csv(csv_file):
    """
    Reads the population from a CSV file.
    Each row in the CSV should contain the parameters and final_loss (fitness).
    """
    population = []
    if os.path.isfile(csv_file):
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert CSV data to the correct types
                individual = {
                    "numVertebrae": int(row["numVertebrae"]),
                    "vertebraeRadius": float(row["vertebraeRadius"]),
                    "numLegs": int(row["numLegs"]),
                    "numLegSegments": int(row["numLegSegments"]),
                    "legLength": float(row["legLength"]),
                    "final_loss": float(row["final_loss"])  # Fitness is stored as final_loss
                }
                population.append(individual)
    return population


def evolutionary_algorithm(csv_file='results.csv'):
    """
    Evolutionary algorithm to optimize parameters.
    Handles initial population creation and evolution without additional writing.
    """
    # Read the population from the CSV file (if it exists)
    population = read_population_from_csv(csv_file)

    # If the CSV file is empty or doesn't exist, create an initial population
    if not population:
        print("Initializing initial population...")
        population = [
            {
                "numVertebrae": random.randint(2, 10),  # Already >= 2
                "vertebraeRadius": max(0.005, random.uniform(0.005, 0.05)),  # Ensure > 0
                "numLegs": random.randint(1, 6),  # Ensure >= 1
                "numLegSegments": random.randint(1, 5),  # Ensure >= 1
                "legLength": max(0.01, random.uniform(0.01, 0.05)),  # Ensure > 0
                "final_loss": None  # Fitness will be calculated later
            }
            for _ in range(populationSize)  # Population size
        ]

        # Evaluate fitness for the initial population and write to CSV
        for individual in population:
            individual["final_loss"] = evaluate_fitness(individual)

    # Evolution loop
    for generation in range(populationSize):  # Number of generations
        print(f"Generation {generation + 1}")

        # Evaluate fitness for each individual (this will write to the CSV)
        for individual in population:
            if individual["final_loss"] is None:  # Only evaluate if fitness is not already calculated
                individual["final_loss"] = evaluate_fitness(individual)
            print(f"Parameters: {individual}, Fitness: {individual['final_loss']}")

        # Sort population by fitness (ascending order, since lower loss is better)
        population.sort(key=lambda x: x["final_loss"])

        # Select the best 50%
        top_50_percent = population[:len(population) // 2]

        # Create new generation:
        # 1. Keep the top 50% unchanged
        # 2. Mutate the top 50% to create the remaining 50%
        new_population = top_50_percent.copy()
        for individual in top_50_percent:
            # Mutate parameters with constraints
            mutated_individual = {
                "numVertebrae": max(2, individual["numVertebrae"] + random.randint(-1, 1)),  # Ensure >= 2
                "vertebraeRadius": max(0.005, individual["vertebraeRadius"] + random.uniform(-0.01, 0.01)),  # Ensure > 0
                "numLegs": max(1, individual["numLegs"] + random.randint(-1, 1)),  # Ensure >= 1
                "numLegSegments": max(1, individual["numLegSegments"] + random.randint(-1, 1)),  # Ensure >= 1
                "legLength": max(0.01, individual["legLength"] + random.uniform(-0.01, 0.01)),  # Ensure > 0
                "final_loss": None  # Fitness will be calculated in the next generation
            }
            new_population.append(mutated_individual)

        population = new_population

    print("Evolution complete.")


if __name__ == '__main__':
    evolutionary_algorithm()