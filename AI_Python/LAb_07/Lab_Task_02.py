class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.edges = []
        self.adj = [[] for _ in range(vertices)]

    def addEdge(self, u, v, w):
        self.edges.append([u, v, w])

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)

        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def kruskalMST(self):
        result = []
        self.edges = sorted(self.edges, key=lambda item: item[2])

        parent = []
        rank = []

        for node in range(self.V):
            parent.append(node)
            rank.append(0)

        e = 0
        i = 0

        while e < self.V - 1:
            u, v, w = self.edges[i]
            i += 1

            x = self.find(parent, u)
            y = self.find(parent, v)

            if x != y:
                e += 1
                result.append([u, v, w])
                self.union(parent, rank, x, y)

        return result

def preorder(node, visited, mst_adj, tour):
    visited[node] = True
    tour.append(node)

    for neighbor in mst_adj[node]:
        if not visited[neighbor]:
            preorder(neighbor, visited, mst_adj, tour)

g = Graph(4)

g.addEdge(0, 1, 10)
g.addEdge(0, 2, 15)
g.addEdge(0, 3, 20)
g.addEdge(1, 2, 35)
g.addEdge(1, 3, 25)
g.addEdge(2, 3, 30)

mst = g.kruskalMST()

mst_adj = [[] for _ in range(g.V)]
mst_cost = 0

print("MST Edges:")

for u, v, w in mst:
    print(u + 1, "-", v + 1, "=", w)
    mst_adj[u].append(v)
    mst_adj[v].append(u)
    mst_cost += w

visited = [False] * g.V
tour = []

preorder(0, visited, mst_adj, tour)
tour.append(0)

print("MST Cost:", mst_cost)
print("Approx TSP Route:", [city + 1 for city in tour])

print("\nDifference:")
print("Hamiltonian Path visits every city exactly once, but it does not need to return to start.")
print("TSP visits every city exactly once and must return to starting city with minimum total cost.")