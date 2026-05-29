import random
import numpy
import copy

countCities = 20
cities = numpy.zeros(shape=(20, 20))
hypothesis = [0] * countCities
visitedCities = []
saveState = []
threshold = 25
lastFitness = 0
cityIndex = 1
trials = 0

def getDistance(cities, hypothesis):
    distance = 0
    for i in range(countCities):
        if i < countCities - 1:
            distance += cities[hypothesis[i]][hypothesis[i + 1]]
            print("[", hypothesis[i], "]", int(distance), "km", end=" ")
        else:
            print("[", hypothesis[i], "]")
    return distance

def getFitness(fitness, hypothesis, saveState, cities):
    oldDistance = getDistance(cities, saveState)
    newDistance = getDistance(cities, hypothesis)
    print("Old Distance", int(oldDistance), "km")
    print("New Distance", int(newDistance), "km")

    if oldDistance > newDistance:
        fitness += 1
    elif oldDistance < newDistance:
        fitness -= 1

    return fitness

def doRandomStep():
    global visitedCities
    global saveState
    global hypothesis

    if len(visitedCities) >= countCities:
        visitedCities.clear()
        visitedCities.append(0)

    randomNumbers = list(set(saveState) - set(visitedCities))
    randomStep = random.choice(randomNumbers)
    visitedCities.append(randomStep)
    hypothesis.remove(randomStep)
    hypothesis.insert(cityIndex, randomStep)

def increment():
    global cityIndex
    global visitedCities

    if cityIndex < countCities - 2:
        cityIndex += 1
    else:
        visitedCities.clear()
        cityIndex = 1

for i in range(countCities):
    hypothesis[i] = i
    for j in range(countCities):
        if j > i:
            cities[i][j] = random.randint(1, 100)
        elif j < i:
            cities[i][j] = cities[j][i]

print("=== START ===")

while lastFitness < threshold:
    print("_________________________________________________________")
    saveState = copy.deepcopy(hypothesis)
    doRandomStep()
    currentFitness = getFitness(lastFitness, hypothesis, saveState, cities)
    print("Old fitness", lastFitness)
    print("Current fitness", currentFitness)

    if currentFitness > lastFitness:
        lastFitness = currentFitness
    elif currentFitness < lastFitness:
        hypothesis = copy.deepcopy(saveState)

    if trials < 3:
        increment()
        trials += 1
    else:
        trials = 0
        visitedCities.append(saveState[cityIndex])

print("Final Path:", hypothesis)
print("Final Distance:", int(getDistance(cities, hypothesis)), "km")