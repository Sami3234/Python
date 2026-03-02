number =[]
while True:
    user_input = int(input("Enter a number (-1 to stop):"))
    if user_input == -1:
        break
    number.append(user_input)
print("Final list:",number)