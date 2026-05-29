def print_board(board):
    for row in board:
        print(" ".join(row))
    print()


def is_safe(board, row, col, n):
    for i in range(row):
        if board[i][col] == "Q":
            return False

    i = row - 1
    j = col - 1
    while i >= 0 and j >= 0:
        if board[i][j] == "Q":
            return False
        i -= 1
        j -= 1

    i = row - 1
    j = col + 1
    while i >= 0 and j < n:
        if board[i][j] == "Q":
            return False
        i -= 1
        j += 1

    return True


def solve_nqueen(board, row, n, solutions):
    if row == n:
        solutions.append([r[:] for r in board])
        return

    for col in range(n):
        if is_safe(board, row, col, n):
            board[row][col] = "Q"
            solve_nqueen(board, row + 1, n, solutions)
            board[row][col] = "_"


n = 8
board = [["_" for _ in range(n)] for _ in range(n)]
solutions = []

solve_nqueen(board, 0, n, solutions)

print("Total solutions:", len(solutions))

for index, solution in enumerate(solutions[:5], start=1):
    print("Solution", index)
    print_board(solution)