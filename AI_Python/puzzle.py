from collections import deque

# 0 = wall
# 1 = empty path

maze = [
    [0,0,0,0,0,1,0,0],
    [0,1,1,1,1,1,1,0],
    [0,1,0,0,0,0,1,0],
    [0,1,0,1,1,0,1,0],
    [0,1,0,1,0,0,1,0],
    [0,1,0,1,0,1,1,0],
    [0,1,1,1,0,1,1,0],
    [0,0,0,0,0,0,0,0]
]

# Start and Goal positions
start = (3,2)
goal = (0,5)

rows = len(maze)
cols = len(maze[0])

def bfs(start, goal):
    queue = deque([start])
    visited = set()
    parent = {}

    visited.add(start)

    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    while queue:
        r,c = queue.popleft()

        if (r,c) == goal:
            break

        for dr,dc in directions:
            nr = r + dr
            nc = c + dc

            if 0 <= nr < rows and 0 <= nc < cols:
                if maze[nr][nc] == 1 and (nr,nc) not in visited:
                    queue.append((nr,nc))
                    visited.add((nr,nc))
                    parent[(nr,nc)] = (r,c)

    if goal not in parent and goal != start:
        return "No path found"

    path = []
    current = goal

    while current != start:
        path.append(current)
        current = parent[current]

    path.append(start)
    path.reverse()

    return path

result = bfs(start, goal)
print("Shortest Path:")
print(result)
