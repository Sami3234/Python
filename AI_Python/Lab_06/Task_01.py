# Lab 06 Task: 2D sorted matrix mein binary search karta hai.
# Matrix ko virtual 1D array ki tarah treat kiya gaya hai.
# Target value ki row/column position return hoti hai.

def binarySearch2D(matrix, target):
    if not matrix or not matrix[0]:
        return -1, -1

    rows = len(matrix)
    cols = len(matrix[0])

    left = 0
    right = rows * cols - 1

    while left <= right:
        mid = (left + right) // 2

        row = mid // cols
        col = mid % cols

        if matrix[row][col] == target:
            return row, col

        elif matrix[row][col] < target:
            left = mid + 1

        else:
            right = mid - 1

    return -1, -1


matrix = [
    [1, 3, 5, 7],
    [10, 11, 16, 20],
    [23, 30, 34, 60]
]

target = 3

result = binarySearch2D(matrix, target)

if result != (-1, -1):
    print("Element found at position:", result)
else:
    print("Element not found")