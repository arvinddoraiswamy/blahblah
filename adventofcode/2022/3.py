import utils
import sys
import string

def main():
    input_data = utils.read_input('3.txt')
    #input_data = utils.read_input('dump.txt')
    common_part1 = find_common_item_part1(input_data)
    total_part1 = get_score(common_part1)
    #print(f"Part 1: {total_part1}")
    groups = get_groups(input_data)
    common_part2 = find_common_item_part2(groups)
    total_part2 = get_score(common_part2)
    print(f"Part 2: {total_part2}")
    

def get_score(common):
    scores = {}
    count = 1
    for letter in string.ascii_lowercase:
        scores[letter] = count
        count += 1
    for letter in string.ascii_uppercase:
        scores[letter] = count
        count += 1
    
    total = 0
    for entry in common:
        total += scores[entry]

    return total

def find_common_item_part2(groups):
    common = []
    for subgroup in groups:
        l1 = list(subgroup[0])
        l2 = list(subgroup[1])
        l3 = list(subgroup[2])
        for item in l1:
            if item in l2 and item in l3:
                common.append(item)
                break

    return common

def get_groups(input_data):
    groups = []
    subgroup = []
    count = 0
    for count in range(0, len(input_data)):
        if count % 3 == 0 and count != 0:
            groups.append(subgroup)
            subgroup = []
        subgroup.append(input_data[count])
        count += 1

        if count == len(input_data) - 1:
            groups.append(subgroup)
    return groups
    
def find_common_item_part1(input_data):
    items = []
    common = []
    for rucksack in input_data:
        items = list(rucksack)
        half_size = int(len(items)/2)
        comp1 = items[0:half_size]
        comp2 = items[half_size:]
        final = set(comp1).intersection(comp2)
        for v in final:
            common.append(v)

    return common

if __name__ == "__main__":
    main()
