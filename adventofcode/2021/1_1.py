def read_input(input_file):
    int_data = []
    with open(input_file, 'r') as f:
        data = f.readlines()
    for entry in data:
        int_data.append(int(entry))
    return int_data


def analyse_input(int_data):
    num = 0
    result = 0
    while num < len(int_data) - 3:
        result_1 = int_data[num] + int_data[num+1] + int_data[num+2]
        num += 1
        result_2 = int_data[num] + int_data[num + 1] + int_data[num + 2]

        if result_2 > result_1:
            result += 1

    return result


def main():
    input_file = '1.txt'
    data = read_input(input_file)
    result = analyse_input(data)
    print(result)


main()