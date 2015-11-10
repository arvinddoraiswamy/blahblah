def openfile(filename):
    list_of_strings=[]
    with open(filename) as f:
        t1= f.readlines()

    for string in t1:
        list_of_strings.append(string)

    return list_of_strings
