def power(a,b,p):
    if b ==1:
        return a
    else:
        return pow (a,b) % p
def main():
    p =23
    print("The value of p is:",p)
    g = 9
    print("The value of g is:",g)
    a = 4
    print("The value of a:",a)
    x= power(g,a,p)
    b=3
    print("The value of b:",b)
    y = power(g,b,p)
    ka = power(y,a,p)
    kb = power(x,b,p)
    print("The value of ka is:",ka)
    print("The value of kb is:",kb)
if __name__ == "__main__":
    main()
    