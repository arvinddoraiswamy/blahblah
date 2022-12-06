import utils
import re

def main():
    global input_data
    input_data = utils.read_input('5.txt')
    #input_data = utils.read_input('dump.txt')
    stacks, instruction_offset = arrange_stacks(input_data)
    answer = move_crates(stacks, instruction_offset)
    print(f"Answer: {answer}")

def move_crates(stacks, instruction_offset):
    global input_data
    pattern = re.compile('move (\d*) from (\d*) to (\d*)')
    for i in range(instruction_offset, len(input_data)):
        groups = re.search(pattern, input_data[i])
        num,src,dest = int(groups[1]), int(groups[2])-1, int(groups[3])-1
        pop_num = 0
        i1 = []
        while pop_num < num:
            i1.append(stacks[src].pop())
            pop_num += 1
        
        """
        #Uncomment for Part 2
        i1 = i1[::-1]
        """
        for elem in i1:
            stacks[dest].append(elem)

    answer = ''
    for k,v in stacks.items():
        answer += v[-1]
    return answer

def arrange_stacks(input_data):
    stacks = {}
    pattern = '.*\d.*'
    for count,line in enumerate(input_data):
        match = re.match(pattern, line)
        if match:
            line = line.replace(' ','')
            stacks = {index:[] for index,entry in enumerate(list(line))}
            break

    row_size = (len(stacks) * 4) - 1
    
    #Get original stack order
    for i in range(0, count):#Vertical
        offset = 0
        stack_count = 0
        line = input_data[i]
        while offset <= row_size:#Horizontal
            if line[offset] == ' ':
                #stacks[stack_count].append(' ')
                offset += 4
            else:
                offset += 1
                stacks[stack_count].append(line[offset])
                offset += 3
            stack_count += 1
   
    for k, v in stacks.items():
        stacks[k] = v[::-1] 
    instruction_offset = count + 2
    return stacks, instruction_offset


if __name__ == "__main__":
    input_data = []
    main()
