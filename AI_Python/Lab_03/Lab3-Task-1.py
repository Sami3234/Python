# Lab 03 Task: Node class ke sath BFS path search karta hai.
# Graph weighted hai, lekin BFS traversal order ke mutabiq path dhoondta hai.
# End par A se G tak path aur accumulated cost print hoti hai.

from collections import deque

class Node:
    def __init__(self, name, parent=None, actions=None, cost=0):
        self.name = name
        self.parent = parent
        self.actions = actions if actions else []
        self.cost = cost

graph = {
    'A': Node('A', None, [('B',6), ('C',9), ('E',1)], 0),
    'B': Node('B', None, [('A',6), ('D',3), ('E',4)], 0),
    'C': Node('C', None, [('A',9), ('F',3), ('E',3), ('G',3)], 0),
    'D': Node('D', None, [('B',3), ('E',5), ('F',10)], 0),
    'E': Node('E', None, [('A',1), ('B',4), ('D',5), ('F',6), ('C',3)], 0),
    'F': Node('F', None, [('C',2), ('E',6), ('D',7)], 0),
    'G': Node('G', None, [('C',3)], 0)
}

def bfs(start, goal):
    visited = set()
    queue = deque([(graph[start], 0)])  

    while queue:
        current, cost_so_far = queue.popleft()

        if current.name == goal:

            path = []
            node = current
            while node:
                path.append(node.name)
                node = node.parent
            path.reverse()
            return path, cost_so_far

        visited.add(current.name)

        for neighbor_name, edge_cost in current.actions:
            if neighbor_name not in visited:
                neighbor = graph[neighbor_name]
                neighbor.parent = current
                queue.append((neighbor, cost_so_far + edge_cost))

    return None, None

path, total_cost = bfs('A', 'G')
print("Path from A to G:", path)
print("Total Cost:", total_cost)
