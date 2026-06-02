# Lab 03 Activity: Simple graph par Breadth First Search chalata hai.
# Queue use hoti hai taa ke nodes level by level visit hon.
# Output BFS traversal order print karta hai.

graph = {
    '5': ['3','7'],
    '3': ['2','4'],
    '7': ['8'],
    '2': [],
    '4': ['8'],
    '8': []
}
visited = []
queue = []
def bfs (visited,graph,node):
    visited.append(node)
    queue.append(node)

    while queue:
        m = queue.pop(0)
        print(m,end =" ")

        for neighbour in graph[m]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)
print("Following is the Breadth First Search")
bfs(visited,graph, '5')
