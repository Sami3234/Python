from collections import deque
import heapq
import tracemalloc

graph = {
    'Arad': [('Zerind', 75), ('Timisoara', 118), ('Sibiu', 140)],
    'Zerind': [('Arad', 75), ('Oradea', 71)],
    'Oradea': [('Zerind', 71), ('Sibiu', 151)],
    'Timisoara': [('Arad', 118), ('Lugoj', 111)],
    'Lugoj': [('Timisoara', 111), ('Mehadia', 70)],
    'Mehadia': [('Lugoj', 70), ('Drobeta', 75)],
    'Drobeta': [('Mehadia', 75), ('Craiova', 120)],
    'Craiova': [('Drobeta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
    'Sibiu': [('Arad', 140), ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
    'Rimnicu Vilcea': [('Sibiu', 80), ('Craiova', 146), ('Pitesti', 97)],
    'Fagaras': [('Sibiu', 99), ('Bucharest', 211)],
    'Pitesti': [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucharest', 101)],
    'Bucharest': [('Fagaras', 211), ('Pitesti', 101)]
}

def bfs(start, goal):
    visited = set()
    queue = deque([(start, [start])])

    while queue:
        node, path = queue.popleft()

        if node == goal:
            return path

        if node not in visited:
            visited.add(node)

            for neighbor, _ in graph[node]:
                queue.append((neighbor, path + [neighbor]))

def dfs(start, goal):
    visited = set()
    stack = [(start, [start])]

    while stack:
        node, path = stack.pop()

        if node == goal:
            return path

        if node not in visited:
            visited.add(node)

            for neighbor, _ in graph[node]:
                stack.append((neighbor, path + [neighbor]))

def ucs(start, goal):
    visited = set()
    queue = [(0, start, [start])]

    while queue:
        cost, node, path = heapq.heappop(queue)

        if node == goal:
            return path, cost

        if node not in visited:
            visited.add(node)

            for neighbor, weight in graph[node]:
                heapq.heappush(queue, (cost + weight, neighbor, path + [neighbor]))

def memory_test(function, name):
    tracemalloc.start()

    function('Arad', 'Bucharest')

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"{name} Peak Memory Usage: {peak / 1024:.2f} KB")

memory_test(bfs, "BFS")
memory_test(dfs, "DFS")
memory_test(ucs, "UCS")