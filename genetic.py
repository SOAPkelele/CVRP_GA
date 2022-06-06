from typing import List, Tuple

import numpy as np

from p_types import City, Route, ProblemData


def get_route(cities: List[City], data: ProblemData):
    route = [[data.depot]]
    truck_load = 0

    for city in cities:
        if truck_load + city.demand > data.truck_capacity:
            route[-1].append(data.depot)
            route.append([data.depot])
            truck_load = 0
        route[-1].append(city)
        truck_load += city.demand

    if route[-1][-1] != data.depot:
        route[-1].append(data.depot)

    return Route(cities=route, chromosome=cities)


def fix_child(child: List[City], ind_1: int, ind_2: int, data: ProblemData) -> Route:
    old_gene = child[:ind_1] + child[ind_2:]
    new_gene = child[ind_1:ind_2]

    # элементы которых нет в новом гене
    not_in_child = []
    for city in data.cities:
        if city not in new_gene:
            not_in_child.append(city)

    # из элементов которых, нет в новом гене, убираем элементы, которые есть в старом гене
    error_index = []
    for i, city in enumerate(old_gene):
        if city in not_in_child:
            not_in_child.remove(city)
        else:
            error_index.append(i)

    for i in range(len(error_index)):
        old_gene[error_index[i]] = not_in_child[i]

    child = old_gene[:ind_1] + new_gene + old_gene[ind_1:]

    return get_route(child, data)


def crossover_parents(p1: Route, p2: Route, data: ProblemData) -> Tuple[Route, Route]:
    ind_1, ind_2 = sorted(np.random.choice(len(p1.chromosome), size=2, replace=False))

    offspring_1 = p1.chromosome[:ind_1] + p2.chromosome[ind_1:ind_2] + p1.chromosome[ind_2:]

    offspring_2 = p2.chromosome[:ind_1] + p1.chromosome[ind_1:ind_2] + p2.chromosome[ind_2:]

    return fix_child(offspring_1, ind_1, ind_2, data), fix_child(offspring_2, ind_1, ind_2, data)


def crossover_population(population: List[Route], probability: float, data: ProblemData):
    half = len(population) // 2

    fathers = population[:half]
    np.random.shuffle(fathers)

    mothers = population[half:]
    np.random.shuffle(mothers)

    middle_population = []

    for i in range(half):
        if np.random.choice([True, False], p=[probability, 1 - probability]):
            middle_population.extend(crossover_parents(fathers[i], mothers[i], data))

    population[0:len(population)] = middle_population + population


def mutate_chromosome_swap(chromosome: Route, data: ProblemData) -> Route:
    # поменять местами два элемента
    ind_1, ind_2 = sorted(np.random.choice(len(chromosome.chromosome), size=2, replace=False))

    new_chromosome = chromosome.chromosome
    new_chromosome[ind_1], new_chromosome[ind_2] = new_chromosome[ind_2], new_chromosome[ind_1]

    return get_route(new_chromosome, data)


def mutate_chromosome_inversion(chromosome: Route, data: ProblemData) -> Route:
    # перевернуть часть хромосомы
    ind_1, ind_2 = sorted(np.random.choice(len(chromosome.chromosome), size=2, replace=False))

    new_chromosome = chromosome.chromosome
    new_chromosome[ind_1:ind_2] = new_chromosome[ind_1:ind_2][::-1]

    return get_route(new_chromosome, data)


def mutate_population(population: List[Route], probability: float, data: ProblemData):
    for i in range(len(population)):
        if np.random.choice([True, False], p=[probability, 1 - probability]):
            population[i] = mutate_chromosome_inversion(population[i], data)


def get_initial_population(population_size: int, data: ProblemData) -> List[Route]:
    population = []
    for _ in range(population_size):
        cities = data.cities.copy()
        np.random.shuffle(cities)
        population.append(get_route(cities, data))
    return population


def get_fitness_of_population(population: List[Route]) -> float:
    return sum([route.fitness_score for route in population])


def roulette_selection(population: List[Route]):
    # choice of 2 parents according to their fitness
    population_fitness = get_fitness_of_population(population)
    selection_probs = [route.fitness_score / population_fitness for route in population]
    population[0:len(population)] = \
        [route for route in np.random.choice(population, size=len(population), p=selection_probs)]
