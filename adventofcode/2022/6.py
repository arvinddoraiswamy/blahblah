import utils

def main():
    input_data = utils.read_input('6.txt')
    #input_data = utils.read_input('dump.txt')
    answer1 = group_input(input_data, 4)
    answer2 = group_input(input_data, 14)
    print(f"Part 1: {answer1}")
    print(f"Part 2: {answer2}")

def group_input(input_data, expected_len):
    signals = [x for x in ''.join(input_data)]
    for i in range(0, len(signals) - expected_len -1):
        group = signals[i:i+expected_len]
        if len(set(group)) == expected_len:
            break
    return i+expected_len

def test():
    assert(group_input('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 4)) == 7
    assert(group_input('bvwbjplbgvbhsrlpgdmjqwftvncz', 4)) == 5
    assert(group_input('nppdvjthqldpwncqszvftbrmjlhg', 4)) == 6
    assert(group_input('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 4)) == 10
    assert(group_input('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 4)) == 11

    assert(group_input('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 14)) == 19
    assert(group_input('bvwbjplbgvbhsrlpgdmjqwftvncz', 14)) == 23
    assert(group_input('nppdvjthqldpwncqszvftbrmjlhg', 14)) == 23
    assert(group_input('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 14)) == 29
    assert(group_input('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 14)) == 26

if __name__ == "__main__":
    main()
    test()
