def read_input(input_file):
    with open(input_file, 'r') as f:
        data = f.readlines()
    return data


def analyse_input(data):
    results = [0]
    for num in range(1, len(data)):
        x = int(data[num])
        y = int(data[num-1])
        difference = x - y
        if difference > 0:
            results.append(1)
        elif difference < 0:
            results.append(0)
        else:
            results.append(0)

    print(sum(results))


def main():
    input_file = '1.txt'
    data = read_input(input_file)
    analyse_input(data)


main()
