# Lab 06 Task: 2D grid mein police-thief matching karta hai.
# Grid ke har row/column positions scan karke catches count hota hai.
# Range k ke andar possible matches greedy style mein count hote hain.

def policeThief2D(grid, k):
    police = []
    thieves = []
    result = 0

    rows = len(grid)
    cols = len(grid[0])

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 'P':
                police.append((i, j))
            elif grid[i][j] == 'T':
                thieves.append((i, j))

    caught = set()

    for p in police:
        for t in thieves:
            if t not in caught:
                distance = abs(p[0] - t[0]) + abs(p[1] - t[1])

                if distance <= k:
                    caught.add(t)
                    result += 1
                    break

    return result


grid = [
    ['P', 'T', 'T'],
    ['T', 'P', 'T'],
    ['T', 'T', 'P']
]

k = 2

print("Maximum thieves caught:", policeThief2D(grid, k))