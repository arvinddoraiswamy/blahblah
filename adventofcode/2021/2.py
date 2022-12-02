def read_input(input_file):
    with open(input_file, 'r') as f:
        data = f.readlines()
    return data


def analyse_input_2(data):
    horiz = depth = aim = result = 0
    for line in data:
        (direction, distance) = line.split(' ')
        distance = int(distance)
        if direction == 'forward':
            horiz += distance
            depth += (aim * distance)
        elif direction == 'down':
            aim += distance
        elif direction == 'up':
            aim -= distance

    result = horiz * depth
    return result


def analyse_input_1(data):
    horiz = depth = result = 0
    for line in data:
        (direction, distance) = line.split(' ')
        distance = int(distance)
        if direction == 'forward':
            horiz += distance
        elif direction == 'down':
            depth += distance
        elif direction == 'up':
            depth -= distance

    result = horiz * depth
    return result


def main():
    input_file = '2.txt'
    data = read_input(input_file)
    # result = analyse_input_1(data)
    result = analyse_input_2(data)
    print(result)


main()