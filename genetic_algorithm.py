import matplotlib.pyplot as plt
import numpy as np
import operator
import random
import copy
import ea_classes as cs


# Initialization of the population

def init_population(pop_size, city_list):
    population = []
    for i in range(0, pop_size):
        population.append(cs.Individual(city_list))
    return population


# Mutation process - for each individual order in which of two randomly selected cities (genes) are visited can be
# swapped with given probability (mutation_rate).

def mutate(population, mutate_rate):
    max_cities_index = len(population[0].route) - 1

    for i in range(len(population)):
        if random.uniform(0, 1) <= mutate_rate:
            a = random.randint(0, max_cities_index)
            b = random.randint(0, max_cities_index)
            while a == b:
                b = random.randint(0, max_cities_index)

            population[i].route[a], population[i].route[b] = population[i].route[b], population[i].route[a]

    return population


# Breeding of two individuals. Randomly selected part of first parent is complemented with missing cities
# ordered like in the second parent.

def breed(parent1, parent2):
    child_route = []

    start = int(random.random() * len(parent1.route))
    end = int(random.random() * len(parent1.route))

    gene_beg = min(start, end)
    gene_end = max(start, end)

    for i in range(gene_beg, gene_end):
        child_route.append(parent1.route[i])

    child_route = child_route + [item for item in parent2.route if item not in child_route]

    child = parent1
    child.route = child_route

    return child


# CX operator based algorithm for crossover

def breed_cx(parent1, parent2):

    child_route = [0] * 15
    p = 0
    cycling = True

    # print("p1: " + str(parent1))
    # print("p2: " + str(parent2))

    while cycling:
        child_route[p] = (parent1.route[p])
        next_step = parent2.route[p]
        p = parent1.route.index(next_step)
        if p == 0:
            cycling = False

    # print("cx1: " + str(child_route))

    p2 = [item for item in parent2.route if item not in child_route]

    x = 0
    for i in range(len(child_route)):
        if child_route[i] == 0:
            child_route[i] = p2[x]
            x += 1


    # child_route = child_route + [item for item in parent2.route if item not in child_route]

    # print("cx2: " + str(child_route))

    child = copy.copy(parent1)
    child.route = child_route

    return child


# Crossover process. Given number of elite individuals are passed to next generation as offspring.
# From whole population (including elite) mating pool of size of the (population - elite) is chosen.
# Mating pool is randomly shuffled, bred and added to the offspring.

def crossover(population, elite_size):
    mating_pool = []
    offspring = []
    # elite goes first

    sorted_pop = sorted(population, key=operator.attrgetter('distance'))
    for i in range(elite_size):
        mating_pool.append(copy.copy(sorted_pop[i]))
        offspring.append(copy.copy(sorted_pop[i]))

    # wheel of fortune

    dist_normal = 0
    for i in range(len(population)):
        dist_normal += population[i].route_distance()

    for i in range(len(population) - elite_size):
        r = random.uniform(0, 1)
        p = 0
        while r > 0:
            r -= population[p].distance / dist_normal
            p += 1
        mating_pool.append(population[p - 1])

    # crossover

    mating_pool = random.sample(mating_pool, len(mating_pool))

    for i in range(len(population) - elite_size):
        kid = breed(mating_pool[i], mating_pool[len(mating_pool) - i - 1])
        offspring.append(kid)

    return offspring


# Next generation calls.

def next_generation(population, elite_size, mutation_rate):
    population = crossover(population, elite_size)
    population = mutate(population, mutation_rate)
    for i in range(len(population)):
        population[i].route_distance()

    return population


def genetic_algorithm_tsp(cities, pop_size, elite_size, mutation_rate, generations):
    population = init_population(pop_size, cities)
    # print("Initial best route: " + str(sorted(population, key=operator.attrgetter('distance'))[0].distance))
    progress = [sorted(population, key=operator.attrgetter('distance'))[0].distance]

    for i in range(0, generations):
        population = next_generation(population, elite_size, mutation_rate)
        progress.append(sorted(population, key=operator.attrgetter('distance'))[0].distance)
        print("Iteration " + str(i) + ": " + str(sorted(population, key=operator.attrgetter('distance'))[0].distance))

    # print("Final best route: " + str(sorted(population, key=operator.attrgetter('distance'))[0].distance))
    best_route = sorted(population, key=operator.attrgetter('distance'))[0].route
    plt.subplot(1, 2, 1)
    plt.title("Distance over Time")
    plt.plot(progress)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    the_route = []
    for i in range(len(population[0].route)):
        the_route.append([population[0].route[i].x, population[0].route[i].y])
    the_route.append([population[0].route[0].x, population[0].route[0].y])
    np_route = np.array(the_route)
    plt.subplot(1, 2, 2)
    plt.title("Final Route")
    plt.plot(*np_route.T, alpha=0.5)
    plt.scatter(np_route[:, 0], np_route[:, 1], color='b')
    plt.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
    plt.xticks(range(0, 11, 1))
    plt.yticks(range(0, 11, 1))
    plt.show()
    return best_route


cityList = [cs.City(x=1, y=1), cs.City(x=1, y=5), cs.City(x=1, y=10), cs.City(x=2, y=3), cs.City(x=2, y=7), cs.City(x=3, y=2),
            cs.City(x=3, y=9), cs.City(x=4, y=7), cs.City(x=5, y=1), cs.City(x=5, y=3), cs.City(x=5, y=5), cs.City(x=6, y=9),
            cs.City(x=8, y=2), cs.City(x=8, y=7), cs.City(x=10, y=4)]

print(genetic_algorithm_tsp(cityList, 200, 40, 0.01, 300))
