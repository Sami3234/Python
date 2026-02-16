mylist1=[]
print("Enter objects of first list.")
for i in range(5):
    val=input("Enter a value:")
    n=int(val)
    mylist1.append(n)

mylist2=[]
print("Enter object of second list..")
for i in range(5):
    val=input("Enter a value:")
    n=int(val)
    mylist2.append(n)
list3=mylist1+mylist2
print(list3)