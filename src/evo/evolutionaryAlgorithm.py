import subprocess
import random
import ast
import re
import matplotlib.pyplot as plt


def evaluate_individual(num_vertebrae, num_legs, num_leg_segments, leg_length):
    # Run the simulation and capture the output
    result = subprocess.run(
        ["python", "diffmpmEvoTest.py", str(num_vertebrae), str(num_legs), str(num_leg_segments), str(leg_length)],
        capture_output=True, text=True
    )

    # Parse the output
    if result.returncode == 0:
        output = result.stdout.strip()
        lines = output.split("\n")
        for line in reversed(lines):
            match = re.search(r"i=(\d+), loss=(\d+\.\d+)", line)
            if match:
                iter = int(match.group(1))
                loss = float(match.group(2))
                return loss
    return float('inf')  # Return a high loss if the simulation fails


def evolutionary_algorithm(population_size, generations):
    # Initialize population
    population = []
    for _ in range(population_size):
        num_vertebrae = random.randint(3, 6)
        num_legs = random.randint(2, 4)
        num_leg_segments = random.randint(2, 4)
        leg_length = random.uniform(0.02, 0.05)
        population.append((num_vertebrae, num_legs, num_leg_segments, leg_length))

    for generation in range(generations):
        print(f"Generation {generation + 1}")
        # Evaluate fitness for each individual
        fitness = []
        for individual in population:
            loss = evaluate_individual(*individual)
            fitness.append(loss)

        # Select the best individuals
        sorted_population = [x for _, x in sorted(zip(fitness, population))]
        best_individuals = sorted_population[:population_size // 2]

        # Create the next generation
        new_population = best_individuals.copy()
        while len(new_population) < population_size:
            parent1, parent2 = random.choices(best_individuals, k=2)
            child = (
                random.choice([parent1[0], parent2[0]]),  # num_vertebrae
                random.choice([parent1[1], parent2[1]]),  # num_legs
                random.choice([parent1[2], parent2[2]]),  # num_leg_segments
                random.choice([parent1[3], parent2[3]])   # leg_length
            )
            new_population.append(child)

        population = new_population

    # Return the best individual
    best_fitness = min(fitness)
    best_individual = population[fitness.index(best_fitness)]
    return best_individual, best_fitness


# Run the evolutionary algorithm
best_individual, best_fitness = evolutionary_algorithm(population_size=10, generations=20)
print(f"Best Individual: {best_individual}, Best Fitness: {best_fitness}")


def plot_losses(losses):
    plt.plot(losses)
    plt.title("Loss Over Iterations")
    plt.xlabel("Iteration")
    plt.ylabel("Loss")
    plt.show()


# # Plot
# losses = main(num_vertebrae=4, num_legs=3, num_leg_segments=2, leg_length=0.025)
# plot_losses(losses)
