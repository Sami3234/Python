# Lab 08 Activity: Graph representation aur traversal/helper logic use karta hai.
# defaultdict adjacency list ko easy banata hai.
# Code graph ke nodes/edges ko process karke result print karta hai.

from collections import defaultdict

def findManhattanEuclidPair(arr, n):
    X = defaultdict(lambda: 0)
    Y = defaultdict(lambda: 0)
    XY = defaultdict(lambda: 0)

    for i in range(n):
        xi = arr[i][0]
        yi = arr[i][1]

        X[xi] += 1
        Y[yi] += 1
        XY[tuple(arr[i])] += 1

    xAns = 0
    yAns = 0
    xyAns = 0

    for xCoordinatePair in X:
        xFrequency = X[xCoordinatePair]
        xAns += (xFrequency * (xFrequency - 1)) // 2

    for yCoordinatePair in Y:
        yFrequency = Y[yCoordinatePair]
        yAns += (yFrequency * (yFrequency - 1)) // 2

    for XYPair in XY:
        xyFrequency = XY[XYPair]
        xyAns += (xyFrequency * (xyFrequency - 1)) // 2

    return xAns + yAns - 2 * xyAns

arr = [[1, 2], [1, 2], [4, 3], [1, 3]]
n = len(arr)

print(findManhattanEuclidPair(arr, n))