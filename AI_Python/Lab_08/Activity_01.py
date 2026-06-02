# Lab 08 Activity: Heuristic distance calculation ka example hai.
# math functions se nodes ke beech estimated distance nikalti hai.
# Search algorithms mein heuristic guide ke liye use ho sakti hai.

import math
import pandas as pd
import numpy as np

def manhattan_distance(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)

def diagonal_distance(x1, y1, x2, y2):
    return max(abs(x2 - x1), abs(y2 - y1))

def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

print("Manhattan Distance:", manhattan_distance(1, 2, 3, 3))
print("Diagonal Distance:", diagonal_distance(1, 2, 3, 3))
print("Euclidean Distance:", euclidean_distance(1, 2, 3, 3))

x = pd.Series([1, 2, 3, 4, 5])
y = pd.Series([6, 7, 8, 9, 10])

dist = np.sqrt(np.sum((x - y) ** 2))

print("Series 1:")
print(x)
print("Series 2:")
print(y)
print("Euclidean distance between two series is:", dist)