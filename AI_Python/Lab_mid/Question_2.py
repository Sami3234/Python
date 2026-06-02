# Mid Lab Question: Sorted 2D matrix mein binary search karta hai.
# Matrix ko virtual 1D list ki tarah index kiya jata hai.
# Target milay to row/column print, warna not found message.

matrix = [
    [1, 3, 5],
    [7, 9, 11],
    [13, 14, 17]
]
def binary_search_2d(matrix, target):
    rows = len(matrix)
    cols = len(matrix[0])
    left = 0
    right = rows * cols - 1
    while left <= right:
        mid = (left + right) //2
        row = mid // cols
        col = mid % cols
        if matrix[row][col] == target:
            return row, col
        elif matrix[row][col] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1, -1
target = 9
row, col = binary_search_2d(matrix, target)
if row != -1:
    print(f"Target {target} found at row {row}, column {col}")
else:
    print(f"Target {target} not found")