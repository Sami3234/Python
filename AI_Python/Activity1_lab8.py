from random import randint, choice
import numpy
import copy

countCities = 20
cities = numpy.zeros((20, 20))

hypothesis = list(range(countCities))
visitedCities = []
saveState = []

threshold = 5
lastFitness = 0
trials = 0
cityIndex = 1


def getDistance(cities, hypothesis):
    distance = 0
    for i in range(countCities - 1):
        distance += cities[hypothesis[i]][hypothesis[i + 1]]
    return distance


def getFitness(fitness, hypothesis, saveState, cities):
    oldDistance = getDistance(cities, saveState)
    newDistance = getDistance(cities, hypothesis)

    if oldDistance > newDistance:
        fitness += 1
    elif oldDistance < newDistance:
        fitness -= 1

    return fitness


def doRandomStep():
    global visitedCities, saveState, hypothesis

    if len(visitedCities) >= countCities:
        visitedCities.clear()
        visitedCities.append(0)

    randomNumbers = list(set(saveState) - set(visitedCities))
    if not randomNumbers:
        return

    randomStep = choice(randomNumbers)
    visitedCities.append(randomStep)

    hypothesis.remove(randomStep)
    hypothesis.insert(cityIndex, randomStep)


def increment():
    global cityIndex, visitedCities

    if cityIndex < countCities - 2:
        cityIndex += 1
    else:
        visitedCities.clear()
        cityIndex = 1


if __name__ == '__main__':

    for i in range(countCities):
        for j in range(countCities):
            if j > i:
                cities[i][j] = randint(1, 100)
            elif j < i:
                cities[i][j] = cities[j][i]

    iterations = 0

    while lastFitness < threshold and iterations < 100:
        saveState = copy.deepcopy(hypothesis)

        doRandomStep()

        currentFitness = getFitness(lastFitness, hypothesis, saveState, cities)

        if currentFitness > lastFitness:
            lastFitness = currentFitness
        elif currentFitness < lastFitness:
            hypothesis = copy.deepcopy(saveState)

            if trials < 3:
                increment()
            else:
                trials = 0
                visitedCities.append(saveState[cityIndex])

        print("Iteration:", iterations, "Fitness:", lastFitness)

        iterations += 1