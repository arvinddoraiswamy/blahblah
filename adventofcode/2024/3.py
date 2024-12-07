import utils
import re

def main():
    input_file = "3.txt"
    #input_file = "dump.txt"
    file_data = utils.read_input(input_file)
    matches = get_mul_patterns_1(file_data)
    result = multiply(matches)
    print(f"Part 1: {result}")
    matches = get_mul_patterns_2(file_data)
    result = multiply(matches)
    print(f"Part 2: {result}")
    

def multiply(matches):
    result = 0
    matches = [x.replace("mul(","").replace(")","") for x in matches]
    for nums in matches:
        split_nums = nums.split(',')
        split_nums = [int(x) for x in split_nums]
        result += split_nums[0] * split_nums[1]
    return result


def get_mul_patterns_2(file_data):
    all_matches = []
    data = ''.join(file_data)
    pattern1 = r"(don't\(\).*?)do\(\)"
    matches = re.findall(pattern1, data)
    for x in matches:
        data = data.replace(x,"")
    pattern2 = r"mul\(\d{1,3},\d{1,3}\)"
    matches = re.findall(pattern2, data)
    return matches


def get_mul_patterns_1(file_data):
    data = ''.join(file_data)
    pattern = r'mul\(\d{1,3},\d{1,3}\)'
    matches = re.findall(pattern, data)
    return matches


if __name__ == "__main__":
    main()
