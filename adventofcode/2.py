import sys

def get_input(filename):
    with open(filename, 'r') as f:
        directions= f.read().splitlines()
    return directions

def solve(start_pos, valid_moves, directions):
    bathroom_key= ''
    for line in directions:
        l1= list(line)
        for move in l1:
            key= start_pos + move
            if key not in valid_moves.keys():
                continue
            else:
                start_pos= valid_moves[key]
        bathroom_key += start_pos

    print 'The bathroom key is', bathroom_key

if __name__ == '__main__':
    '''
    Read the input. Handle keypad directions line by line. Get key per line and store before going on to the next line.
    '''
    filename= '2.txt'
    start_pos= '5'
    valid_moves_1= {
                    '1R':'2', '1D':'4',
                    '2L':'1', '2R':'3', '2D':'5',
                    '3L':'2', '3D':'6',
                    '4R':'5', '4D':'7', '4U':'1',
                    '5L':'4', '5R':'6', '5U':'2', '5D':'8',
                    '6L':'5', '6U':'3', '6D':'9',
                    '7U':'4', '7R':'8',
                    '8L':'7', '8R':'9', '8U':'5',
                    '9L':'8', '9U':'6'
                    }

    valid_moves_2= {'1D':'3',
                    '5R':'6',
                    '9L':'8',
                    'DU':'B',
                    '2R':'3', '2D':'6',
                    '4L':'3', '4D':'8',
                    'AU':'6', 'AR':'B',
                    'CU':'8', 'CL':'B',
                    '3L':'2', '3R':'4', '3U':'1', '3D':'7',
                    'BL':'A', 'BR':'C', 'BD':'D','BU':'7',
                    '6L':'5', '6R':'7', '6U':'2', '6D':'A',
                    '7L':'6', '7R':'8', '7U':'3', '7D':'B',
                    '8L':'7', '8R':'9', '8U':'4', '8D':'C'
                    }

directions= get_input(filename)
#Solving for part 1
solve(start_pos, valid_moves_1, directions)

#Solving for part 2
solve(start_pos, valid_moves_2, directions)
