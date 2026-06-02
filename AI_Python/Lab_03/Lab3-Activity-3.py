# Lab 03 Activity: Graph par BFS traversal A node se start hoti hai.
# visited list duplicate visits rokne ke liye use hoti hai.
# Queue neighbors ko level-wise process karti hai.


graph = {
    'A': ['B', 'C', 'E'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F', 'G'],
    'D': ['B', 'E'],
    'E': ['A', 'B', 'D'],
    'F': ['C'],
    'G': ['C']
}

visited = [] 
queue = []    
def bfs(visited, graph, node):
    visited.append(node)
    queue.append(node)
    while queue:
        m = queue.pop(0)
        print(m, end=" ")
        for neighbour in graph[m]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)

print("Following is the Breadth-First Search starting from A:")
bfs(visited, graph, 'A')