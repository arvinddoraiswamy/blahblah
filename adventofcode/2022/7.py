import utils

def main():
    global input_data
    input_data = utils.read_input('7.txt')
    #input_data = utils.read_input('dump.txt')
    contents = create_tree()
    answer = get_size(contents)
    print(f"Answer: {answer}")


def get_size(contents):
    sizes = {}
    for dirs, dir_files in contents.items():
        for name, size in dir_files.items():
            if dirs in sizes:
                sizes[dirs] += size
            else:
                sizes[dirs] = size

    #print(sizes)
    #print('-' * 10)

    #Account for recursive directories
    for dirs, dir_files in contents.items():
        for name, size in dir_files.items():
            if size == 0 and name in sizes:
                sizes[dirs] += sizes[name]
        
    #Calculate answer
    answer = 0
    for dir_name, size in sizes.items():
        if size <= 100000:
            answer += size
            print(dir_name, size)

    return answer


def create_tree():
    contents = {}
    i = 0
    pwd = []
    while i < len(input_data):
        line = input_data [i].split(' ')
        if line[0] == '$':
            if line[1] == 'cd':
                #print(i, 'command', line)
                if line[2] == '..':
                    pwd.pop() 
                else:
                    pwd.append(line[2])
                if line[2] not in contents and line[2] != '..':
                    contents[line[2]] = {}
                print('pwd:', pwd)
            elif line[0] == 'ls':
                i += 1
        elif line[0] == 'dir':
            #print(i, 'directory', line)
            contents[pwd[-1]][line[1]] = 0
        elif line[0].isnumeric():
            #print(i, 'file', line)
            contents[pwd[-1]][line[1]] = int(line[0])
        i += 1
    print('-' * 10)
    for k,v in contents.items():
        print(k,v)

    return contents

input_data = []
if __name__ == "__main__":
    main()
