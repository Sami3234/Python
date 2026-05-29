
graph = {
    0: [1, 2],
    1: [2],
    2: [0, 3],
    3: [3]
}

visited = set()


def dfs(node):
    
    visited.add(node)

    
    print(node, end=" ")

   
    for neighbor in graph[node]:
        
        if neighbor not in visited:
            dfs(neighbor)


print("DFS Traversal starting from vertex 2:")
dfs(2)