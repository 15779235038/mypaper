names = ['test1', 'test2', 'test3', 'test4']

def get_dynamic_list(names):
    createVar = globals()
    # createVar = locals()
    for i in range(len(names)):
        createVar[names[i]] = list()
get_dynamic_list(names)
print(globals())
print(test1)
