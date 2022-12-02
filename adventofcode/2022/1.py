import utils
import operator

def main():
    input_data = utils.read_input('1.txt')
    #input_data = utils.read_input('dump.txt')
    calories_per_elf = get_elf_calories(input_data)
    max_calories, sum_top3_calories = get_max_cals(calories_per_elf)
    print(f"Top max calories: {max_calories}")
    print(f"Top 3 calories total: {sum_top3_calories}")


def get_max_cals(calories_per_elf):
    sorted_max_calories = sorted(calories_per_elf.items(), key=operator.itemgetter(1), reverse=True)
    sum_top3_calories = sorted_max_calories[0][1] + sorted_max_calories[1][1] + sorted_max_calories[2][1]
    return sorted_max_calories[0][1], sum_top3_calories


def get_elf_calories(input_data):
    elf_num = 1
    elf_calories = 0
    calories_per_elf = {}
    for item in input_data:
        if item:
            elf_calories += int(item)
        else:
            calories_per_elf[elf_num] = elf_calories
            elf_num += 1
            elf_calories = 0

    return calories_per_elf

    
if __name__ == "__main__":
    main()
