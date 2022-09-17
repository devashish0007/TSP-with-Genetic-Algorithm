import heapq
import random
from random import shuffle
import time


class Graph:

    def __init__(self, n, distance):
        self.node = n
        self.distance = distance

    def fitness(self, path):
        cost = 0
        path.append(path[0])
        # calculate the cost of path
        for i in range(len(path)-1):
            cost += self.distance[path[i]][path[i+1]]
        return [cost]

    def randomPath(self, path):
        shuffle(path)
        if(len(path)>50):
            print("I am in randomPath")
            print(path)
        return self.fitness(path.copy()) + path


if __name__ == '__main__':
    # input
    t = input()
    cities = int(input())
    location, distance = [], []
    for i in range(cities):
        location.append([float(j) for j in input().split()])
    for i in range(cities):
        distance.append([float(j) for j in input().split()])
    listCities = [i for i in range(cities)]
    graph = Graph(cities, distance)
    # Generate random population
    paths = []
    permutations = 100*cities
    selectK = cities
    for i in range(permutations//2 * 2):
        paths.append(graph.randomPath(listCities.copy()))


    numberOfCross = permutations //2    # size of  s1 & s2
    # for i in range(numberOfCross):
    t_end = time.time() + 50
    t_next = time.time() + 10
    iteration = 0
    while time.time() < t_end:
        iteration += 1
        print("Reached:", iteration)
        # Generate two set N//2
        s1 = paths[:numberOfCross]
        s2 = paths[numberOfCross:]
        crossoverPaths = []

        for j in range(len(s1)):
            path1 = (s1[j][1:]).copy()
            path2 = (s2[j][1:]).copy()

            # Generate random l & r s.t. l < r
            l = random.randint(0, len(path1)-2)
            r = random.randint(l+1, len(path1)-1)
            # print(l,r,len(path1))
            map1, map2 = {}, {}

            for k in range(l, r+1):
                map1[path1[k]] = k
                map2[path2[k]] = k

            newp1, newp2 = [0]*len(path1), [0]*len(path1)
            # Cross over

            for pos in range(0, len(path1)):
                if l <= pos <= r:
                    newp1[pos] = path2[pos]
                    newp2[pos] = path1[pos]
                    continue

                tempNode = path1[pos]
                while tempNode in map2:
                    tempNode = path1[map2[tempNode]]

                newp1[pos] = tempNode

                tempNode = path2[pos]
                while tempNode in map1:
                    tempNode = path2[map1[tempNode]]

                newp2[pos] = tempNode
            # Cross end
            crossoverPaths.append(graph.fitness(newp1.copy())+newp1)
            crossoverPaths.append(graph.fitness(newp2.copy())+newp2)


        heapq.heapify(crossoverPaths)
        # select k best paths
        k, selectedPaths = 0, []
        while k < selectK:
            selectedPaths.append(heapq.heappop(crossoverPaths))
            k += 1

        # remove k highest path from paths
        paths.sort()
        # printing the best path wrt iteration number.
        # if i%100 == 0: print("Best path in :", i, "is ", paths[0])
        # paths with highest fitness value after crossover.
        paths = paths[:len(paths) - selectK] + selectedPaths
        if time.time() > t_next:
            for c in paths[0][:]:
                print(c, end=" ")
            t_next = time.time() + 10

    paths.sort()
    # print("###################################################################")
    # print("The best path is:")
    for c in paths[0][:]:
        print(c, end=" ")

    # print("###################################################################")



