from heapq import heappush, heappop

graph = {
    "Arad": {"Zerind": 75, "Timisoara": 118, "Sibiu": 140},
    "Zerind": {"Arad": 75, "Oradea": 71},
    "Oradea": {"Zerind": 71, "Sibiu": 151},
    "Timisoara": {"Arad": 118, "Lugoj": 111},
    "Lugoj": {"Timisoara": 111, "Mehadia": 70},
    "Mehadia": {"Lugoj": 70, "Drobeta": 75},
    "Drobeta": {"Mehadia": 75, "Craiova": 120},
    "Craiova": {"Drobeta": 120, "Rimnicu Vilcea": 146, "Pitesti": 138},
    "Sibiu": {"Arad": 140, "Oradea": 151, "Fagaras": 99, "Rimnicu Vilcea": 80},
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
    "Neamt": {"Iasi": 87},
}

def path_cost(path):
    cost = 0
    for i in range(len(path) - 1):
        cost += graph[path[i]][path[i + 1]]
    return cost

def dfs(start, goal):
    stack = [(start, [start])]
    visited = set()
    expanded = 0

    while stack:
        node, path = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        expanded += 1
        if node == goal:
            return path, path_cost(path), expanded
        for nxt in sorted(graph[node].keys(), reverse=True):
            if nxt not in visited:
                stack.append((nxt, path + [nxt]))
    return None, float("inf"), expanded
def ucs(start, goal):
    pq = []
    heappush(pq, (0, start, [start]))
    best_cost = {start: 0}
    expanded = 0
    while pq:
        cost, node, path = heappop(pq)
        if cost > best_cost.get(node, float("inf")):
            continue
        expanded += 1
        if node == goal:
            return path, cost, expanded
        for nxt, w in graph[node].items():
            new_cost = cost + w
            if new_cost < best_cost.get(nxt, float("inf")):
                best_cost[nxt] = new_cost
                heappush(pq, (new_cost, nxt, path + [nxt]))
    return None, float("inf"), expanded
if __name__ == "__main__":
    start, goal = "Arad", "Hirsova"
    dfs_path, dfs_cost, dfs_expanded = dfs(start, goal)
    ucs_path, ucs_cost, ucs_expanded = ucs(start, goal)
    print("DFS Path:", " -> ".join(dfs_path))
    print("DFS Cost:", dfs_cost)
    print("DFS Expanded:", dfs_expanded)

    print("\nUCS Path:", " -> ".join(ucs_path))
    print("UCS Cost:", ucs_cost)
    print("UCS Expanded:", ucs_expanded)