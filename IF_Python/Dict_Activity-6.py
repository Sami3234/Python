sample = {("sohaib","ali"):"0246585468445", 
          ("aib","li"):"02465854645",
          ("sib","ai"):"0246585468445"}

firstName = input("enter first name")
lastName = input("enter last name")

searchTuple = (firstName, lastName)
if searchTuple in sample:
    print(sample[searchTuple])
else:
    print("name not found")
