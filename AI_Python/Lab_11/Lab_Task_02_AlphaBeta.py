# Lab 11 Task: N-Queen backtracking aur alpha-beta style pruning compare karta hai.
# normal_nodes aur pruned_nodes search effort count karte hain.
# Output solutions aur checked nodes ka comparison print karta hai.

normal_nodes = 0
pruned_nodes = 0


def is_safe(positions, row, col):
    for r in range(row):
        c = positions[r]

        if c == col:
            return False

        if abs(c - col) == abs(r - row):
            return False

    return True


def normal_backtracking(n, row, positions):
    global normal_nodes
    normal_nodes += 1

    if row == n:
        return 1

    total = 0

    for col in range(n):
        if is_safe(positions, row, col):
            positions[row] = col
            total += normal_backtracking(n, row + 1, positions)
            positions[row] = -1

    return total


def alpha_beta_pruning(n, row, positions, alpha, beta):
    global pruned_nodes
    pruned_nodes += 1

    if row == n:
        return 1

    best = 0

    for col in range(n):
        if is_safe(positions, row, col):
            positions[row] = col
            value = alpha_beta_pruning(n, row + 1, positions, alpha, beta)
            positions[row] = -1

            best += value
            alpha = max(alpha, best)

            if beta <= alpha:
                break

    return best


n = 8

positions1 = [-1] * n
solutions1 = normal_backtracking(n, 0, positions1)

positions2 = [-1] * n
solutions2 = alpha_beta_pruning(n, 0, positions2, -1000, 92)

print("N Queen Size:", n)
print("Normal Backtracking Solutions:", solutions1)
print("Alpha Beta Style Solutions:", solutions2)
print("Normal Nodes Checked:", normal_nodes)
print("Pruned Nodes Checked:", pruned_nodes)

if pruned_nodes < normal_nodes:
    print("Optimization proved: Alpha-Beta checked fewer nodes.")
else:
    print("Optimization not visible for this configuration.")