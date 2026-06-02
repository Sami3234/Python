# Lab 05 Activity: Linear search example hai.
# Array ko left se right scan karke target element ka index dhoondta hai.
# Element milay to index, warna not-present message print karta hai.

def search(arr, x):
    for i in range(len(arr)):
        if arr[i] == x:
            return i
    return -1

arr = [2, 3, 4, 10, 40]
x = 10

result = search(arr, x)

if result == -1:
    print("Element is not present in array")
else:
    print("Element is present at index", result)