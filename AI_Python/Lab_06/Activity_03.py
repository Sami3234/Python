# Lab 06 Activity: Recursive binary search example hai.
# Sorted array mein middle element compare karke search space half hoti hai.
# Target found ho to index return hota hai, warna -1.

def binarySearch(arr, l, r, x):

    if r >= l:
        mid = l + (r - l) // 2

        if arr[mid] == x:
            return mid

        elif arr[mid] > x:
            return binarySearch(arr, l, mid - 1, x)

        else:
            return binarySearch(arr, mid + 1, r, x)

    else:
        return -1


arr = [2, 3, 4, 10, 40]
x = 10

result = binarySearch(arr, 0, len(arr) - 1, x)

if result != -1:
    print("Element is present at index", result)
else:
    print("Element is not present in array")