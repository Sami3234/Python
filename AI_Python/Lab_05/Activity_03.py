def search(arr, search_element):
    left = 0
    right = len(arr) - 1
    position = -1

    while left <= right:
        if arr[left] == search_element:
            position = left
            print("Element found in Array at", position + 1, "Position with", left + 1, "Attempt")
            return

        if arr[right] == search_element:
            position = right
            print("Element found in Array at", position + 1, "Position with", len(arr) - right, "Attempt")
            return

        left += 1
        right -= 1

    print("Not found in Array")


arr = [1, 2, 3, 4, 5]
search_element = 5

search(arr, search_element)