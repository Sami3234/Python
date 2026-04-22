def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)
num1 = int(input("Enter first integer: "))
num2 = int(input("Enter second integer: "))
result = gcd(num1, num2)
print("GCD is:", result)