# Lab 04 Activity: Recursive Depth First Search example hai.
# Graph dictionary se represent hota hai aur visited set repeat visits rokta hai.
# Start node 5 se DFS traversal print hoti hai.

graph = {
    '5': ['3', '7'],
    '3': ['2', '4'],
    '7': ['8'],
    '2': [],
    '4': ['8'],
    '8': []
}

visited = set()

def dfs(visited, graph, node):
    if node not in visited:
        print(node, end=" ")
        visited.add(node)

        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)

print("Following is the Depth-First Search")
dfs(visited, graph, '5')