import sys
import binascii


def read_input(input_file):
    with open(input_file, 'r') as f:
        data = f.read().splitlines()
    return data


def analyse_input_2(data):
    pass


def analyse_input_1(data):
    counter = {}
    gamma = epsilon = power = result = 0
    len_entry = len(data[0])
    for num in range(0, len_entry):
        counter[num] = {}

    for line in data:
        split_line = list(line)
        for num, entry in enumerate(split_line):
            if entry not in counter[num].keys():
                counter[num][entry] = 1
            else:
                counter[num][entry] += 1

    gamma_bin = epsilon_bin = ''
    for key, value in counter.items():
        gamma_bin += str(max(value, key=value.get))
        epsilon_bin += str(min(value, key=value.get))

    gamma = int(gamma_bin, 2)
    epsilon = int(epsilon_bin, 2)
    result = gamma * epsilon
    return result


def main():
    input_file = 'sample.txt'
    data = read_input(input_file)
    # result = analyse_input_1(data)
    result = analyse_input_2(data)
    # print(result)


main()
