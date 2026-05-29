class Node:
    def __init__(self, position, parent):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

def draw_grid(map_data, width, height, spacing=1, **kwargs):
    for y in range(height):
        for x in range(width):
            print(("%-" + str(spacing) + "s") % draw_tile(map_data, (x, y), kwargs), end="")
        print()

def draw_tile(map_data, position, kwargs):
    value = map_data.get(position)

    if "path" in kwargs and position in kwargs["path"]:
        value = "+"

    if "start" in kwargs and position == kwargs["start"]:
        value = "@"

    if "goal" in kwargs and position == kwargs["goal"]:
        value = "$"

    return value

def add_to_open(open_list, neighbor):
    for node in open_list:
        if neighbor == node and neighbor.f >= node.f:
            return False
    return True

def best_first_search(map_data, start, end):
    open_list = []
    closed = []

    start_node = Node(start, None)
    goal_node = Node(end, None)

    open_list.append(start_node)

    while len(open_list) > 0:
        open_list.sort()
        current_node = open_list.pop(0)
        closed.append(current_node)

        if current_node == goal_node:
            path = []
            while current_node != start_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        x, y = current_node.position
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

        for next_position in neighbors:
            map_value = map_data.get(next_position)

            if map_value is None or map_value == "#":
                continue

            neighbor = Node(next_position, current_node)

            if neighbor in closed:
                continue

            neighbor.g = abs(neighbor.position[0] - start_node.position[0]) + abs(neighbor.position[1] - start_node.position[1])
            neighbor.h = abs(neighbor.position[0] - goal_node.position[0]) + abs(neighbor.position[1] - goal_node.position[1])
            neighbor.f = neighbor.h

            if add_to_open(open_list, neighbor):
                open_list.append(neighbor)

    return None

maze_lines = [
    "##########",
    "#@       #",
    "# ###### #",
    "#      # #",
    "###### # #",
    "#      #$#",
    "##########"
]

map_data = {}
start = None
end = None
height = len(maze_lines)
width = len(maze_lines[0])

for y, line in enumerate(maze_lines):
    for x, char in enumerate(line):
        map_data[(x, y)] = char

        if char == "@":
            start = (x, y)
        elif char == "$":
            end = (x, y)

path = best_first_search(map_data, start, end)

print("Path:")
print(path)
print()

draw_grid(map_data, width, height, path=path, start=start, goal=end)
print()
print("Steps to goal:", len(path))