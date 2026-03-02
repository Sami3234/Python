a = [[1,2,3],[4,5,6],[7,8,9]]
b = [[9,8,7],[6,5,4],[3,2,1]]
c = []  
for inrow in range(3):
    c.append([])
    for incol in range(3):
        c[inrow].append(0)
        for indaux in range(3):
            c[inrow][incol] += a[inrow][indaux] * b[indaux][incol]

print(c)
