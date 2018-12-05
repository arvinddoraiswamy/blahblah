input_file = '1.txt'
#input_file = 'dump'
with open(input_file, 'r') as f:
    data = f.read()

data = data[:-1].split('\n')

# Part 1
#total = 0
#for frequency in data:
#    total += int(frequency)
#print("Part 1")
#print(total)

# Part 2
total = 0
resultant_frequencies = {}
match = False
resultant_frequencies[0] = 99999
data1 = data[:]
while match is False:
    for count, freq in enumerate(data, start=1):
        total += int(freq)
        if total in resultant_frequencies.keys():
            print("Part 2")
            print(count, total)
            match = True
            break
        else:
            resultant_frequencies[total] = 99999

        if count == len(data):
            data  = data1[:]
