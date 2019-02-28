import matplotlib.pyplot as plt
import numpy as np
import operator
import random
import copy


# Class defining cities coordinates

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, city):
        xd = abs(self.x - city.x)
        yd = abs(self.y - city.y)
        dist = np.sqrt((xd ** 2) + (yd ** 2))
        return dist

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"


# Class defining individual (chromosome), storing route between cities and distance to be travelled by following it

class Individual:
    def __init__(self, city_list):
        self.route = random.sample(city_list, len(city_list))
        self.distance = self.route_distance()

    def route_distance(self):
        distance = 0
        for i in range(len(self.route)-1):
            distance += City.distance(self.route[i], self.route[i+1])
        if (len(self.route)-1) > 0:
            distance += City.distance(self.route[0], self.route[len(self.route)-1])
        self.distance = distance
        return distance

    def fitness(self):
        return 1 / self.route_distance()

    def __repr__(self):
        return "(" + str(self.route_distance()) + "," + str(self.route) + ")"


# Initialization of the population

def init_population(pop_size, city_list):
    population = []
    for i in range(0, pop_size):
        population.append(Individual(city_list))
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
        mating_pool.append(population[p-1])

    # crossover

    mating_pool = random.sample(mating_pool, len(mating_pool))

    for i in range(len(population) - elite_size):
        kid = breed(mating_pool[i], mating_pool[len(mating_pool)-i-1])
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


cityList = [City(x=1, y=1), City(x=1, y=5), City(x=1, y=10), City(x=2, y=3), City(x=2, y=7), City(x=3, y=2),
            City(x=3, y=9), City(x=4, y=7), City(x=5, y=1), City(x=5, y=3), City(x=5, y=5), City(x=6, y=9),
            City(x=8, y=2), City(x=8, y=7), City(x=10, y=4)]


print(genetic_algorithm_tsp(cityList, 200, 40, 0.01, 300))
