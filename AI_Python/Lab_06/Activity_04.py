# Lab 06 Activity: Jump Search algorithm implement karta hai.
# Sorted array ko fixed jumps mein scan karke phir linear search karta hai.
# Target element ka index print karta hai.

import math

def getEgyptianFraction(numerator, denominator):
    result = []

    while numerator != 0:
        x = math.ceil(denominator / numerator)
        result.append(x)

        numerator = numerator * x - denominator
        denominator = denominator * x

    return result


numerator = 6
denominator = 14

fractions = getEgyptianFraction(numerator, denominator)

output = " + ".join(["1/" + str(i) for i in fractions])

print("Egyptian Fraction Representation of 6/14 is")
print(output)