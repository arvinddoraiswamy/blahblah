import utils

def main():
    global input_data
    #input_data = utils.read_input('7.txt')
    input_data = utils.read_input('dump.txt')
    contents = create_tree()
    for k,v in contents.items():
        print(k,v)
    print('-' * 10)
    answer = get_sizes(contents)
    print(f"Answer: {answer}")


def get_sizes(contents):
    sizes = {}
    for k,v in contents.items():
        size = 0
        for entry in v.values():
            if not isinstance(entry, dict):
                size += entry    
        sizes[k] = size

    for k,v in sizes.items():
        print(k,v)
    print('-' * 10)
    for k,v in contents.items():
        size = 0
        for k1,v1 in v.items():
            if isinstance(v1, dict):
                size += sizes[k1]
        sizes[k] += size
    answer = 0
    for k,v in sizes.items():
        if v <= 100000:
            answer += v

    return answer


def create_tree():
    contents = {}
    i = 0
    pwd = []
    while i < len(input_data):
        line = input_data[i].split(' ')
        if line[0] == '$':
            if line[1] == 'cd':
                if line[2] == '..':
                    pwd.pop() 
                else:
                    pwd.append(line[2])
                    if len(pwd) >= 2:
                        if pwd[-1] not in contents:
                            contents[pwd[-1]] = {}
                    else:
                        contents[pwd[-1]] = {}
            elif line[0] == 'ls':
                i += 1
        elif line[0] == 'dir':
            contents[pwd[-1]][line[1]] = {}
        elif line[0].isnumeric():
            contents[pwd[-1]][line[1]] = int(line[0])
        i += 1

    return contents

input_data = []
if __name__ == "__main__":
    main()
