# Lab 04 Task: Romania map par DFS se Arad to Bucharest route search karta hai.
# Recursive DFS path list aur distance ko update karta rehta hai.
# Goal milne par path aur total distance print hoti hai.


graph = {
    "Arad": [("Zerind", 75), ("Sibiu", 140), ("Timisoara", 118)],

    "Zerind": [("Arad", 75), ("Oradea", 71)],

    "Oradea": [("Zerind", 71), ("Sibiu", 151)],

    "Sibiu": [("Arad", 140), ("Oradea", 151),
               ("Fagaras", 99), ("Rimnicu Vilcea", 80)],

    "Timisoara": [("Arad", 118), ("Lugoj", 111)],

    "Lugoj": [("Timisoara", 111), ("Mehadia", 70)],

    "Mehadia": [("Lugoj", 70), ("Drobeta", 75)],

    "Drobeta": [("Mehadia", 75), ("Craiova", 120)],

    "Craiova": [("Drobeta", 120),
                 ("Rimnicu Vilcea", 146),
                 ("Pitesti", 138)],

    "Rimnicu Vilcea": [("Sibiu", 80),
                        ("Craiova", 146),
                        ("Pitesti", 97)],

    "Fagaras": [("Sibiu", 99), ("Bucharest", 211)],

    "Pitesti": [("Rimnicu Vilcea", 97),
                 ("Craiova", 138),
                 ("Bucharest", 101)],

    "Bucharest": [("Fagaras", 211),
                   ("Pitesti", 101),
                   ("Giurgiu", 90),
                   ("Urziceni", 85)],

    "Giurgiu": [("Bucharest", 90)],

    "Urziceni": [("Bucharest", 85),
                  ("Hirsova", 98),
                  ("Vaslui", 142)],

    "Hirsova": [("Urziceni", 98), ("Eforie", 86)],

    "Eforie": [("Hirsova", 86)],

    "Vaslui": [("Urziceni", 142), ("Iasi", 92)],

    "Iasi": [("Vaslui", 92), ("Neamt", 87)],

    "Neamt": [("Iasi", 87)]
}



def dfs(current, goal, visited, path, distance):

    
    visited.add(current)

    
    path.append(current)

    if current == goal:
        print("Path Found:")
        print(" -> ".join(path))
        print("Total Distance:", distance, "km")
        return True

    
    for neighbor, cost in graph[current]:

        
        if neighbor not in visited:

            if dfs(neighbor,
                   goal,
                   visited,
                   path,
                   distance + cost):
                return True

    
    path.pop()
    return False


start = "Arad"
goal = "Bucharest"

visited = set()
path = []

print("DFS Search from Arad to Bucharest\n")

dfs(start, goal, visited, path, 0)