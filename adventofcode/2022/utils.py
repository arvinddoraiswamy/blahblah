def read_input(input_file):
    with open(input_file, 'r') as f:
        data = f.read().split("\n")[:-1]
    return data
