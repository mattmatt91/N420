mylist = []

for i in range(30):
    mylist.insert(0,i)
    mylist = mylist[:10]
print(mylist)