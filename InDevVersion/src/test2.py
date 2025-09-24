string = "id = 0 AND name = 'test' and test = 'test'"

def tokenize(string):
    string = string.split()
    i = 0
    conditions = []
    while i < len(string):
        temp=[]
        temp.append(string[i])
        temp.append(string[i+1])
        temp.append(string[i+2])
        if not i > len(string)-4 and string[i+3].lower() in ("or","and"):
            temp.append(string[i+3].upper())
        conditions.append(temp)
        i+=4
    return conditions

def build(conditions):
    column = ""
    params = []
    for i in conditions:
        print(i)
        column+=f"{i[0]}{i[1]}? "
        if len(i) > 3:
            column+=i[3] + " "
        params.append(i[2])
    return column, params

print(build(tokenize(string)))