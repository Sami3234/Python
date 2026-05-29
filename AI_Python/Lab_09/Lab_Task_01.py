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
    "Arad": 366,
    "Zerind": 374,
    "Oradea": 380,
    "Sibiu": 253,
    "Timisoara": 329,
    "Lugoj": 244,
    "Mehadia": 241,
    "Drobeta": 242,
    "Craiova": 160,
    "Rimnicu Vilcea": 193,
    "Fagaras": 176,
    "Pitesti": 100,
    "Bucharest": 80,
    "Giurgiu": 90,
    "Urziceni": 20,
    "Hirsova": 77,
    "Eforie": 161,
    "Vaslui": 0,
    "Iasi": 92,
    "Neamt": 150
}

def hill_climbing(start, goal):
    current = start
    path = [current]
    cost = 0

    while current != goal:
        neighbors = graph[current]

        best_neighbor = min(neighbors, key=lambda node: heuristic[node])

        if heuristic[best_neighbor] >= heuristic[current]:
            return path, cost, False

        cost += neighbors[best_neighbor]
        current = best_neighbor
        path.append(current)

    return path, cost, True

def best_first_search(start, goal):
    visited = set()
    queue = [(heuristic[start], start, [start], 0)]

    while queue:
        h, current, path, cost = heapq.heappop(queue)

        if current == goal:
            return path, cost

        if current in visited:
            continue

        visited.add(current)

        for neighbor, distance in graph[current].items():
            if neighbor not in visited:
                heapq.heappush(queue, (heuristic[neighbor], neighbor, path + [neighbor], cost + distance))

    return None, 0

hc_path, hc_cost, found = hill_climbing("Arad", "Vaslui")
bfs_path, bfs_cost = best_first_search("Arad", "Vaslui")

print("Hill Climbing Result")
print("Path:", hc_path)
print("Cost:", hc_cost)
print("Found Goal:", found)

print("\nBest First Search Result")
print("Path:", bfs_path)
print("Cost:", bfs_cost)