# Lab 06 Activity: Police and thief greedy matching problem solve karta hai.
# Har police nearest available thief ko range k ke andar catch kar sakta hai.
# Function total caught thieves return karta hai.

def policeThief(arr, n, k):
    thi = []
    pol = []
    l = 0
    r = 0
    res = 0

    for i in range(n):
        if arr[i] == 'P':
            pol.append(i)
        elif arr[i] == 'T':
            thi.append(i)

    while l < len(thi) and r < len(pol):

        if abs(thi[l] - pol[r]) <= k:
            res += 1
            l += 1
            r += 1

        elif thi[l] < pol[r]:
            l += 1

        else:
            r += 1

    return res


arr1 = ['P', 'T', 'T', 'P', 'T']
k = 2
print("Maximum thieves caught:", policeThief(arr1, len(arr1), k))

arr2 = ['T', 'T', 'P', 'P', 'T', 'P']
k = 2
print("Maximum thieves caught:", policeThief(arr2, len(arr2), k))

arr3 = ['P', 'T', 'P', 'T', 'T', 'P']
k = 3
print("Maximum thieves caught:", policeThief(arr3, len(arr3), k))