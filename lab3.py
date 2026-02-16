Dict = {1:'Geeks', 2:'for',3:'Geeks' }
print("\nDistionary with the use of interger keys")
print(Dict)


#Mixed keys
Dict = {'Name':'Geeks',1:[1,2,3,4]}
print("\Dicionary with the use of Mixed Keys")
print(Dict)

#empty dictionary

Dict ={}
print ("Empty Dictonary:")
print(Dict)

#Creating a Dictionary with dict method
Dict = dict({1:'Geeks',2:'For',3:'Geeks'})
print("\n dictionary with the use of dict():")
print (Dict)

#with each item as a pair
Dict = dict({1:'Geeks',2:'For',})
print("\n Dictionary with the use of dict():")
print(Dict)

#with each item as a pair
Dict= dict ([(1,'Geeks'),(2, 'For')])
print("\nDictionary with each item as a pair:")
print(Dict)

#Nested Dictionary
Dict ={1:'Geeks',2:'For',
       3:{'A':'Welcome','B':'To','C':'Geeks'}}
print(Dict)


#adding elements one at a time
Dict[0] ='Geeks'
Dict[2]='For'
Dict[3]=1
print("\nDictionary after adding 3 element:")
print(Dict)

#to single key

Dict ['Value_set']=2,3,4
print ("\n Dictionary after adding 3 elements")
print(Dict)

#updateing existing keys  values

Dict[2]= 'Welcome'
print ("\nUpdated key values:")
print (Dict)

#Adding Nested key values to dictionary
Dict[5] ={'Nested':{'1':'Life','2':'Geeks'}}
print("\nAdding a Nested key:")


#assessing a element from a Dictionary
#Creating a Dictionary
Dict = {1:'Geeks','Name':'For',3:'Geeks'}

#accessing a element using key
print ("Accessing a element using key:")
print (Dict[1])

#Creatin a Dictionay
Dict ={1:'Geeks','name':'For',3:'Geeks'}

#method
print("Accessing a element using get")
print(Dict.get(3))

#Creating a Dictionary
Dict = {'Dict1':{1:'Geeks'},'Dict2':{'Name':'For'}}

print (Dict['Dict1'])
print (Dict['Dict1'][1])
print(Dict['Dict2']['Name'])

#intial Dictionary
Dict = {5:'Welcome',6:'To',7:'Geeks',
'A':{1:'Geeks',2:'For',3:'Geeks'},'B':{1:'Geeks',2:'Life'}}
print("Initial Dictionay")
print(Dict)

#Deleting a key value
del Dict[6]
print("\nDelecting a key from Nested Dictionary:")
print(Dict)

#Creating a Dictionary
Dict={1:'Geeks','Name':'For',3:'Geeks'}

#Deleting a key
pop_ele = Dict.pop(1)
print("\nDictionary after delection:"+str(Dict))
print('Value associated to poped key is:'+str(pop_ele))


#using popitem() method
Dict = {1:'Geeks','name':'for',3:'Geeks'}
pop_ele = Dict.popitem()
print("\nDictionary after deletion:"+str(Dict))
print("\nDictionary after delection "+str(Dict))
print("\nThe aritary pair returned is:"+str(pop_ele))

#using clear()method
Dict = {1:'Geeks','name':'For',3:'Geeks'}
Dict.clear()
print("\nDeleting entire Dictionary")
print(Dict)






