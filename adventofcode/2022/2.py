import utils
import sys

def main():
    input_data = utils.read_input('2.txt')
    #input_data = utils.read_input('dump.txt')
    my_score_part1 = calculate_score_part1(input_data)
    my_score_part2 = calculate_score_part2(input_data)
    print(f"My score: {my_score_part1}")
    print(f"My score: {my_score_part2}")


def calculate_score_part2(input_data):
    global score_win
    global score_draw
    global score_loss
    global score_rock
    global score_paper
    global score_scissors
    my_score = 0
    row_score = 0
    '''
    A for Rock, B for Paper, and C for Scissors
    Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock.
    X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win
    '''
    for entry in input_data:
        opp_move, end_result = entry.split(' ')
        if end_result == 'X':
            row_score += score_loss
            if opp_move == 'A':
                row_score += score_scissors
            if opp_move == 'B':
                row_score += score_rock
            if opp_move == 'C':
                row_score += score_paper
        if end_result == 'Y':
            row_score += score_draw
            if opp_move == 'A':
                row_score += score_rock
            if opp_move == 'B':
                row_score += score_paper
            if opp_move == 'C':
                row_score += score_scissors
        if end_result == 'Z':
            row_score += score_win
            if opp_move == 'A':
                row_score += score_paper
            if opp_move == 'B':
                row_score += score_scissors
            if opp_move == 'C':
                row_score += score_rock

        my_score += row_score
        row_score = 0

    return my_score


def calculate_score_part1(input_data):
    global score_win
    global score_draw
    global score_loss
    global score_rock
    global score_paper
    global score_scissors
    my_score = 0
    row_score = 0
    for entry in input_data:
        opp_move, my_move = entry.split(' ')
        if my_move == 'X':
            row_score += score_rock
            if opp_move == 'A':
                row_score += score_draw
            if opp_move == 'B':
                row_score += score_loss
            if opp_move == 'C':
                row_score += score_win
        elif my_move == 'Y':
            row_score += score_paper
            if opp_move == 'A':
                row_score += score_win
            if opp_move == 'B':
                row_score += score_draw
            if opp_move == 'C':
                row_score += score_loss
        elif my_move == 'Z':
            row_score += score_scissors
            if opp_move == 'A':
                row_score += score_loss
            if opp_move == 'B':
                row_score += score_win
            if opp_move == 'C':
                row_score += score_draw

        my_score += row_score
        row_score = 0

    return my_score

score_win, score_draw, score_loss = 6,3,0
score_rock, score_paper, score_scissors = 1,2,3

if __name__ == "__main__":
    main()
