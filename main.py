from genetic import get_initial_population, roulette_selection, crossover_population, mutate_population
from plot import plot_solution, plot_best_distances
from utils import parse_data


def run(population_size: int, crossover_probability: float, mutation_probability: float, generations: int):
    problems = [
        "A-n32-k5.data",
        "A-n39-k5.data",
        "E-n22-k4.data",
        "F-n45-k4.data",
        "P-n22-k8.data",
        "tai75b.data",
        "P-n22-k2.data",
        "B-n31-k5.data",
        "CMT1.data",
        "P-n16-k8.data"
    ]

    for problem in problems:
        problem_data = parse_data("data/" + problem)
        print(problem_data)
        best_solutions = []

        population = get_initial_population(population_size=population_size, data=problem_data)

        for i in range(generations):
            # sort chromosomes
            population.sort(key=lambda x: x.fitness_score, reverse=True)

            # best route at that generation
            best_solutions.append(population[0])
            print(f"Generation {i + 1} best route: {best_solutions[-1].distance}")

            # stop criteria
            if (i + 1) / generations >= 0.2:
                # calculate last n generations average distance
                last_n_scores = min(int(generations * 0.05), 50)
                last_scores_num = sum([route.distance for route in best_solutions[-last_n_scores:]]) / last_n_scores
                if last_scores_num - best_solutions[-1].distance < 0.0001:
                    print(f"Last {last_n_scores} generations average distance: {last_scores_num}")
                    break

            # remove chromosomes with bad fitness from population to fit population size
            population = population[:POPULATION_SIZE]

            roulette_selection(population)

            # make new chromosomes from selected with best fitness
            crossover_population(population, probability=crossover_probability, data=problem_data)

            # mutate chromosomes
            mutate_population(population, probability=mutation_probability, data=problem_data)

        best_distances = [route.distance for route in best_solutions]
        plot_best_distances(best_distances, problem_data)

        best_solution = sorted(best_solutions, key=lambda x: x.fitness_score, reverse=True)[0]
        plot_solution(best_solution, problem_data)


if __name__ == '__main__':
    CROSSOVER_PROB = 0.8
    MUTATION_PROB = 0.03
    POPULATION_SIZE = 1000
    GENERATIONS = 500

    run(population_size=POPULATION_SIZE,
        crossover_probability=CROSSOVER_PROB,
        mutation_probability=MUTATION_PROB,
        generations=GENERATIONS)
