import utils

def main():
    input_file = "1.txt"
    #input_file = "dump.txt"
    file_data = utils.read_input(input_file)
    l1,l2 = get_lists(file_data)
    #distances = calc_1(l1, l2)
    sim_score = calc_2(l1, l2)
    #print(distances)
    print(sim_score)

def calc_2(l1, l2):
    l2_count = {}
    sim_score = []
    
    for num in l2:
        if num not in l2_count:
            l2_count[num] = 1
        else:
            l2_count[num] += 1

    for num in l1:
        if num in l2_count:
            sim_score.append(num * l2_count[num])
           
    return sum(sim_score) 


def calc_1(l1, l2):
    distances = []
    for i in range(0, len(l1)):
        distances.append(abs(l1[i] - l2[i]))
    return sum(distances)


def get_lists(file_data):
    l1 = []
    l2 = []
    for line in file_data:
        line = line.replace("   ", "^")
        tmp = line.split("^")
        l1.append(int(tmp[0]))
        l2.append(int(tmp[1]))
    return sorted(l1),sorted(l2)


if __name__ == "__main__":
    main()
