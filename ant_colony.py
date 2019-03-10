import matplotlib.pyplot as plt
import numpy as np
import operator
import random
import copy
import ea_classes as cs


alpha = 1
beta = 5
ph_evaporation_rate = 0.5
ph_t0 = 0.01
t = 0
t_max = 1000
ant_nr = 10

cityList = [cs.City(x=1, y=1), cs.City(x=1, y=5), cs.City(x=1, y=10), cs.City(x=2, y=3), cs.City(x=2, y=7)]

nr_of_cities = len(cityList)

ph_on = np.zeros((nr_of_cities, nr_of_cities))
distances = np.zeros((nr_of_cities, nr_of_cities))
ants = []

for i in range(nr_of_cities):
    for j in range(nr_of_cities):
        if j != i:
            distances[i, j] = cityList[i].distance(cityList[j])


def init(ant_nr, ph_t0):

    for i in range(nr_of_cities):
        for j in range(nr_of_cities):
            if j != i:
                ph_on[i, j] = ph_t0

    for i in range(ant_nr):
        ants.append(cs.Ant(cityList))


def move_ants():
    for ant in ants:
        nonvisited = [city for city in cityList + ant.visited_cities if city not in cityList or city not in ant.visited_cities]
        ph_nv = []
        for nv_city in nonvisited:
            i = cityList.index(ant.city)
            j = cityList.index(nv_city)
            ph_nv.append(ph_on[i, j])
        for k in range(len(nonvisited)):
            r = random.uniform(0, 1)
            x = 0
            while r > 0:
                next_city = nonvisited[x]
                r -= ph_nv[x]
                x += 1




init(ant_nr, ph_t0)

while t < t_max:
    move_ants()
    update_pheromones()


print(distances)
