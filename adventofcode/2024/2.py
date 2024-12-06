import utils

def main():
    #input_file = "2.txt"
    input_file = "dump.txt"
    file_data = utils.read_input(input_file)
    #safe, unsafe = analyze_1(file_data)
    safe, unsafe = analyze_2(file_data)
    print(f"Safe: {safe}")

def analyze_2(file_data):
    safe = 0
    unsafe = 0

    for count, line in enumerate(file_data, start=1):
        bad = False
        inc = 0
        dec = 0
        unsafe_ctr = False
        saved_index = 0

        nums = line.split(" ")
        nums = [int(x) for x in nums]
        dup_nums = nums
        print(f"Count:{count} Original numbers:,{nums}")
        #for i in range(0, len(nums) - 1):
        i = 0
        while i < len(nums) - 1:
            diff = abs(int(nums[i]) - int(nums[i+1]))
            print(nums[i], nums[i+1], diff)
            if (diff < 1 or diff > 3):
                if not unsafe_ctr:
                    unsafe_ctr = True                
                    del(dup_nums[i])
                    saved_index = i+1
                    print("First time unsafe by difference. Forgive.")
                    print(f"Duplicate numbers: {dup_nums}")
                    nums = dup_nums
                    print("Nums modified", nums)
                    i = 0
                    inc = 0
                    dec = 0
                    continue
                else:
                    unsafe += 1
                    bad = True
                    print("Unsafe by difference", diff)
                    break
            if dec == 0 and inc == 0:
                if nums[i] > nums[i+1]:
                    dec = 1
                    print("Dec:", dec)
                elif nums[i] < nums[i+1]:
                    inc = 1
                    print("Inc:", inc)
                i += 1
            elif (dec == 1 and nums[i] > nums[i+1]):
                print("Valid decrementing", diff)
                i += 1
                continue                            
            elif (inc == 1 and nums[i] < nums[i+1]):
                print("Valid incrementing", diff)
                i += 1
                continue
            else:
                if not unsafe_ctr:
                    print("First time unsafe inc/dec. Forgive.")
                    unsafe_ctr = True                
                    del(dup_nums[i])
                    saved_index = i+1
                    print(dup_nums)
                    nums = dup_nums
                    print("Nums modified", nums)
                    i = 0
                    inc = 0
                    dec = 0
                    continue
                else:
                    unsafe += 1
                    print(f"Unsafe by inc/dec inconsistency {dec} {inc} {nums[i]} {nums[i+1]}")
                    bad = True
                    break

        if not bad:
            safe += 1
        print(f"Safe: {safe}")
        print("-" * 15)
    return safe, unsafe

def analyze_1(file_data):
    safe = 0
    unsafe = 0

    for line in file_data:
        bad = False
        inc = 0
        dec = 0
        nums = line.split(" ")
        nums = [int(x) for x in nums]
        #print(nums)
        for i in range(0, len(nums) - 1):
            diff = abs(int(nums[i]) - int(nums[i+1]))
            #print(nums[i], nums[i+1], diff)
            if (diff < 1 or diff > 3):
                unsafe += 1
                bad = True
                #print("Unsafe by difference", diff)
                break
            if dec == 0 and inc == 0:
                if nums[i] > nums[i+1]:
                    dec = 1
                    #print("Dec:", dec)
                elif nums[i] < nums[i+1]:
                    inc = 1
                    #print("Inc:", inc)
            elif (dec == 1 and nums[i] > nums[i+1]):
                #print("Valid decrementing", diff)
                continue                            
            elif (inc == 1 and nums[i] < nums[i+1]):
                #print("Valid incrementing", diff)
                continue
            else:
                unsafe += 1
                #print(f"Unsafe by inc/dec inconsistency {dec} {inc} {nums[i]} {nums[i+1]}")
                bad = True
                break
        if not bad:
            safe += 1
        #print("Safe", safe)
        #print("-" * 15)
    return safe, unsafe


if __name__ == "__main__":
    main()
