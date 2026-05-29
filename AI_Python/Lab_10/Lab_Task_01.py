import random
import heapq

graph = {
    "o1": {"n1": 1, "n2": 4},
    "n1": {"o1": 1, "o2": 2, "o3": 3},
    "n2": {"o1": 4, "o2": 1, "o6": 1, "o8": 1},
    "o2": {"n1": 2, "n2": 1, "o3": 7, "o7": 3},
    "o3": {"n1": 3, "o2": 7, "n3": 1},
    "n3": {"o3": 1, "n4": 1},
    "n4": {"n3": 1, "o7": 2, "o4": 1, "o5": 2},
    "o7": {"o2": 3, "n4": 2, "o8": 5, "o9": 1},
    "o6": {"n2": 1, "o8": 4},
    "o8": {"n2": 1, "o6": 4, "o7": 5, "o9": 3, "o11": 6},
    "o9": {"o8": 3, "o7": 1, "o5": 1, "n5": 1},
    "o5": {"n4": 2, "o9": 1},
    "o4": {"n4": 1, "o10": 4},
    "o10": {"o4": 4, "n5": 2},
    "n5": {"o9": 1, "o10": 2, "o11": 1},
    "o11": {"o8": 6, "n5": 1}
}

cities = list(graph.keys())

def dijkstra(start):
    distances = {city: float("inf") for city in cities}
    distances[start] = 0
    pq = [(0, start)]

    while pq:
        current_distance, current_city = heapq.heappop(pq)

        if current_distance > distances[current_city]:
            continue

        for neighbor, weight in graph[current_city].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances

shortest_paths = {city: dijkstra(city) for city in cities}

def route_distance(route):
    total = 0

    for i in range(len(route) - 1):
        total += shortest_paths[route[i]][route[i + 1]]

    total += shortest_paths[route[-1]][route[0]]
    return total

def create_route():
    route = cities[:]
    random.shuffle(route)
    return route

def initial_population(size):
    return [create_route() for _ in range(size)]

def fitness(route):
    return 1 / route_distance(route)

def selection(population):
    selected = random.sample(population, 3)
    selected.sort(key=lambda route: route_distance(route))
    return selected[0]

def crossover(parent1, parent2):
    start = random.randint(0, len(parent1) - 2)
    end = random.randint(start + 1, len(parent1) - 1)

    child = [None] * len(parent1)
    child[start:end] = parent1[start:end]

    pointer = 0

    for city in parent2:
        if city not in child:
            while child[pointer] is not None:
                pointer += 1
            child[pointer] = city

    return child

def mutate(route, mutation_rate):
    for i in range(len(route)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(route) - 1)
            route[i], route[j] = route[j], route[i]

def genetic_algorithm(pop_size, generations, mutation_rate):
    population = initial_population(pop_size)
    best_route = min(population, key=route_distance)
    best_distance = route_distance(best_route)

    for gen in range(generations):
        new_population = []

        for _ in range(pop_size):
            parent1 = selection(population)
            parent2 = selection(population)
            child = crossover(parent1, parent2)
            mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population
        current_best = min(population, key=route_distance)
        current_distance = route_distance(current_best)

        if current_distance < best_distance:
            best_route = current_best
            best_distance = current_distance
            print("Generation:", gen, "Best Distance:", best_distance)

    return best_route, best_distance

best_route, best_distance = genetic_algorithm(
    pop_size=200,
    generations=500,
    mutation_rate=0.02
)

print("Best Route:")
print(best_route)
print("Best Distance:")
print(best_distance)