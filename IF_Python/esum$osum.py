# even and odd ka program
osum =0
esum =0
for i in range (10):
    num = int (input("Enter a number:"))
    if (num%2==0):
        esum +=num
    else:
        osum +=num
print ("Even sum:", esum)
print ("Odd sum:", osum)
