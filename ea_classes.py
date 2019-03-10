import numpy as np
import random

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
        for i in range(len(self.route) - 1):
            distance += City.distance(self.route[i], self.route[i + 1])
        if (len(self.route) - 1) > 0:
            distance += City.distance(self.route[0], self.route[len(self.route) - 1])
        self.distance = distance
        return distance

    def fitness(self):
        return 1 / self.route_distance()

    def __repr__(self):
        return "(" + str(self.route_distance()) + "," + str(self.route) + ")"
        # return "(" + str(self.route) + ")"


# Class representing single ant. Contains current position (city) and list of already visited cities

class Ant:
    def __init__(self, city_list):
        self.city = random.sample(city_list)
        self.visited_cities = [self.city]

    def visited(self, city):
        if city not in self.visited_cities:
            self.visited_cities.append(city)

    def next_iteration(self, city_list):
        self.city = random.sample(city_list)
        self.visited_cities = [self.city]

