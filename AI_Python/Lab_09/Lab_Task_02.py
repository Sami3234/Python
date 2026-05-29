class Node:
    def __init__(self, position, parent):
        self.position = position
        self.parent = parent
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

def best_first_search(maze, start, goal):
    open_list = [Node(start, None)]
    closed = []

    while open_list:
        open_list.sort()
        current = open_list.pop(0)
        closed.append(current)

        if current.position == goal:
            path = []

            while current is not None:
                path.append(current.position)
                current = current.parent

            return path[::-1]

        x, y = current.position
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

        for next_position in neighbors:
            nx, ny = next_position

            if ny < 0 or ny >= len(maze) or nx < 0 or nx >= len(maze[0]):
                continue

            if maze[ny][nx] == "#":
                continue

            neighbor = Node(next_position, current)

            if neighbor in closed:
                continue

            neighbor.f = abs(nx - goal[0]) + abs(ny - goal[1])

            skip = False
            for node in open_list:
                if neighbor == node and neighbor.f >= node.f:
                    skip = True
                    break

            if not skip:
                open_list.append(neighbor)

    return None

def print_maze(maze, path):
    maze_copy = [list(row) for row in maze]

    for x, y in path:
        if maze_copy[y][x] not in ["A", "Y"]:
            maze_copy[y][x] = "+"

    for row in maze_copy:
        print("".join(row))

maze = [
    "###########",
    "#A   #    #",
    "# ## # ## #",
    "#    #    #",
    "#### ### ##",
    "#         #",
    "# ### ### #",
    "#   #   Y #",
    "###########"
]

start = None
goal = None

for y, row in enumerate(maze):
    for x, char in enumerate(row):
        if char == "A":
            start = (x, y)
        elif char == "Y":
            goal = (x, y)

path = best_first_search(maze, start, goal)

print("Path:", path)
print("Steps:", len(path) - 1)
print_maze(maze, path)