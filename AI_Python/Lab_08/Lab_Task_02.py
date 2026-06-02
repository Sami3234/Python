# Lab 08 Task: Best-first/A* style priority queue search hai.
# heapq lowest priority node ko pehle process karta hai.
# Graph path finding ke liye cost/heuristic values use hoti hain.

import heapq

graph = {
    "Arad": {"Zerind": 75, "Sibiu": 140, "Timisoara": 118},
    "Zerind": {"Arad": 75, "Oradea": 71},
    "Oradea": {"Zerind": 71, "Sibiu": 151},
    "Sibiu": {"Arad": 140, "Oradea": 151, "Fagaras": 99, "Rimnicu Vilcea": 80},
    "Timisoara": {"Arad": 118, "Lugoj": 111},
    "Lugoj": {"Timisoara": 111, "Mehadia": 70},
    "Mehadia": {"Lugoj": 70, "Drobeta": 75},
    "Drobeta": {"Mehadia": 75, "Craiova": 120},
    "Craiova": {"Drobeta": 120, "Rimnicu Vilcea": 146, "Pitesti": 138},
    "Rimnicu Vilcea": {"Sibiu": 80, "Craiova": 146, "Pitesti": 97},
    "Fagaras": {"Sibiu": 99, "Bucharest": 211},
    "Pitesti": {"Rimnicu Vilcea": 97, "Craiova": 138, "Bucharest": 101},
    "Bucharest": {"Fagaras": 211, "Pitesti": 101, "Giurgiu": 90, "Urziceni": 85},
    "Giurgiu": {"Bucharest": 90},
    "Urziceni": {"Bucharest": 85, "Hirsova": 98, "Vaslui": 142},
    "Hirsova": {"Urziceni": 98, "Eforie": 86},
    "Eforie": {"Hirsova": 86},
    "Vaslui": {"Urziceni": 142, "Iasi": 92},
    "Iasi": {"Vaslui": 92, "Neamt": 87},
    "Neamt": {"Iasi": 87}
}

heuristic = {
    "Arad": 400,
    "Zerind": 420,
    "Oradea": 410,
    "Sibiu": 300,
    "Timisoara": 430,
    "Lugoj": 360,
    "Mehadia": 330,
    "Drobeta": 300,
    "Craiova": 250,
    "Rimnicu Vilcea": 220,
    "Fagaras": 200,
    "Pitesti": 170,
    "Bucharest": 100,
    "Giurgiu": 150,
    "Urziceni": 80,
    "Hirsova": 0,
    "Eforie": 90,
    "Vaslui": 120,
    "Iasi": 200,
    "Neamt": 280
}

def a_star(start, goal):
    open_list = []
    heapq.heappush(open_list, (heuristic[start], 0, start, [start]))

    visited = set()
    explored_nodes = 0

    while open_list:
        f, g, current, path = heapq.heappop(open_list)
        explored_nodes += 1

        if current == goal:
            return path, g, explored_nodes

        if current in visited:
            continue

        visited.add(current)

        for neighbor, cost in graph[current].items():
            if neighbor not in visited:
                new_g = g + cost
                new_f = new_g + heuristic[neighbor]
                heapq.heappush(open_list, (new_f, new_g, neighbor, path + [neighbor]))

    return None, 0, explored_nodes

def uniform_cost_search(start, goal):
    open_list = []
    heapq.heappush(open_list, (0, start, [start]))

    visited = set()
    explored_nodes = 0

    while open_list:
        cost, current, path = heapq.heappop(open_list)
        explored_nodes += 1

        if current == goal:
            return path, cost, explored_nodes

        if current in visited:
            continue

        visited.add(current)

        for neighbor, distance in graph[current].items():
            if neighbor not in visited:
                heapq.heappush(open_list, (cost + distance, neighbor, path + [neighbor]))

    return None, 0, explored_nodes

a_path, a_cost, a_nodes = a_star("Arad", "Hirsova")
u_path, u_cost, u_nodes = uniform_cost_search("Arad", "Hirsova")

print("A* Search Result")
print("Path:", a_path)
print("Cost:", a_cost)
print("Explored Nodes:", a_nodes)

print("\nUniform Cost Search Result")
print("Path:", u_path)
print("Cost:", u_cost)
print("Explored Nodes:", u_nodes)

print("\nImprovement:")
print("A* uses heuristic, so it explores fewer or more focused nodes than uninformed search.")