import utils
import sys

def main():
    input_data = utils.read_input('4.txt')
    #input_data = utils.read_input('dump.txt')
    matches_part1, matches_part2 = get_lists_sections(input_data)
    print(f"Part 1: {matches_part1}")
    print(f"Part 2: {matches_part2}")

def get_lists_sections(input_data):
    common = []
    matches1 = 0
    matches2 = 0
    for pairs in input_data:
        sections = pairs.split(',')
        for section in sections:
            numbers = section.split('-')
            start = int(numbers[0])
            end = int(numbers[1])+1
            l1 = list(range(start,end))
            common.append(l1)
        
        if set(common[0]).issubset(set(common[1])) or set(common[1]).issubset(set(common[0])):
            matches1 += 1
        if set(common[0]).intersection(set(common[1])):
            matches2 += 1
        common = []
    return matches1, matches2

if __name__ == "__main__":
    main()
