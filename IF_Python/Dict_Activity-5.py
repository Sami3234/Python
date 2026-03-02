def symmDiff(a,b):
    e=set() 
    for i in a: 
        if i not in b:
            e.add(i)
    for i in b: 
        if i not in a:
            e.add(i)
    return e

set1={0,1,2,4,5}
set2={4,5,7,8,9}
print(symmDiff(set1,set2))
print(set1.symmetric_difference(set2))
print(set2.symmetric_difference(set1))
print(set1^set2)
print(set2^set1)
