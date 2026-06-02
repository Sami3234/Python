# Lab 04 Task: BFS aur DFS ko Romania graph par compare karta hai.
# Cases dikhate hain kab BFS fewer nodes visit karta hai aur kab DFS.
# Output visited order aur total visited nodes print karta hai.

# ---------------------------------------------------
# BFS and DFS Comparison on Romania Map Graph
# ---------------------------------------------------

from collections import deque


# Graph Representation
graph = {
    "Arad": ["Zerind", "Sibiu", "Timisoara"],
    "Zerind": ["Arad", "Oradea"],
    "Oradea": ["Zerind", "Sibiu"],
    "Sibiu": ["Arad", "Fagaras", "Rimnicu Vilcea"],
    "Timisoara": ["Arad", "Lugoj"],
    "Lugoj": ["Timisoara", "Mehadia"],
    "Mehadia": ["Lugoj", "Drobeta"],
    "Drobeta": ["Mehadia", "Craiova"],
    "Craiova": ["Drobeta", "Pitesti"],
    "Rimnicu Vilcea": ["Sibiu", "Pitesti"],
    "Fagaras": ["Sibiu", "Bucharest"],
    "Pitesti": ["Rimnicu Vilcea", "Craiova", "Bucharest"],
    "Bucharest": ["Fagaras", "Pitesti"]
}


# ---------------------------------------------------
# BFS Function
# ---------------------------------------------------

def bfs(graph, start, goal):

    visited = set()
    queue = deque([start])

    visited_order = []

    while queue:

        node = queue.popleft()

        if node not in visited:

            visited.add(node)
            visited_order.append(node)

            # Goal Found
            if node == goal:

                print("\nBFS Goal Found!")
                print("Visited Nodes:", visited_order)
                print("Total Nodes Visited:", len(visited_order))
                return

            # Add neighbors
            for neighbor in graph[node]:

                if neighbor not in visited:
                    queue.append(neighbor)


# ---------------------------------------------------
# DFS Function
# ---------------------------------------------------

def dfs(graph, node, goal, visited, visited_order):

    visited.add(node)
    visited_order.append(node)

    # Goal Found
    if node == goal:
        return True

    # Visit neighbors deeply
    for neighbor in graph[node]:

        if neighbor not in visited:

            if dfs(graph, neighbor, goal,
                   visited, visited_order):
                return True

    return False


# ---------------------------------------------------
# CASE 1
# BFS visits fewer nodes than DFS
# Start = Arad
# Goal  = Sibiu
# ---------------------------------------------------

print("===================================")
print("CASE 1")
print("BFS visits FEWER nodes than DFS")
print("Start = Arad")
print("Goal  = Sibiu")
print("===================================")

# BFS
print("\n--- BFS Traversal ---")
bfs(graph, "Arad", "Sibiu")

# DFS
print("\n--- DFS Traversal ---")

visited = set()
visited_order = []

dfs(graph, "Arad", "Sibiu",
    visited, visited_order)

print("\nDFS Goal Found!")
print("Visited Nodes:", visited_order)
print("Total Nodes Visited:", len(visited_order))


# ---------------------------------------------------
# CASE 2
# BFS visits more nodes than DFS
# Start = Arad
# Goal  = Drobeta
# ---------------------------------------------------

print("\n\n===================================")
print("CASE 2")
print("BFS visits MORE nodes than DFS")
print("Start = Arad")
print("Goal  = Drobeta")
print("===================================")

# BFS
print("\n--- BFS Traversal ---")
bfs(graph, "Arad", "Drobeta")

# DFS
print("\n--- DFS Traversal ---")

visited = set()
visited_order = []

dfs(graph, "Arad", "Drobeta",
    visited, visited_order)

print("\nDFS Goal Found!")
print("Visited Nodes:", visited_order)
print("Total Nodes Visited:", len(visited_order))