# Lab 07 Task: Weighted graph par Prim MST implementation hai.
# minKey smallest unvisited edge weight choose karta hai.
# Output MST edges aur weights show karta hai.

import sys

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)] for row in range(vertices)]

    def minKey(self, key, mstSet):
        minimum = sys.maxsize
        min_index = 0

        for v in range(self.V):
            if key[v] < minimum and mstSet[v] == False:
                minimum = key[v]
                min_index = v

        return min_index

    def primMST(self):
        key = [sys.maxsize] * self.V
        parent = [None] * self.V
        key[0] = 0
        mstSet = [False] * self.V
        parent[0] = -1

        for cout in range(self.V):
            u = self.minKey(key, mstSet)
            mstSet[u] = True

            for v in range(self.V):
                if self.graph[u][v] > 0 and mstSet[v] == False and key[v] > self.graph[u][v]:
                    key[v] = self.graph[u][v]
                    parent[v] = u

        total = 0
        print("Roads to repair:")

        for i in range(1, self.V):
            print(parent[i] + 1, "-", i + 1, "Cost:", self.graph[i][parent[i]])
            total += self.graph[i][parent[i]]

        print("Minimum cost to connect all cities:", total)

g = Graph(5)

g.graph = [
    [0, 1, 2, 3, 4],
    [1, 0, 5, 0, 7],
    [2, 5, 0, 6, 0],
    [3, 0, 6, 0, 0],
    [4, 7, 0, 0, 0]
]

g.primMST()