from aocd import submit, lines
import re
from collections import Counter
from functools import lru_cache


def parse(input):
    starting_position = [
        int(re.findall('Player 1 starting position: (\d+)', input[0])[0]) - 1,
        int(re.findall('Player 2 starting position: (\d+)', input[1])[0]) - 1
    ]
    return starting_position


def deterministic_die():
    start = 1
    while True:
        if start > 100:
            start -= 100
        yield list(range(start, start + 3))
        start += 3


def solve_a(input, should_submit=False):
    current_position = parse(input)
    die = deterministic_die()
    die_throw_counter = 0
    player_scores = [0, 0]
    cur_player = 0
    while all([score < 1000 for score in player_scores]):
        next_moves = next(die)
        current_position[cur_player] += sum(next_moves)
        current_position[cur_player] %= 10
        player_scores[cur_player] += current_position[cur_player] + 1
        cur_player = 1 - cur_player
        die_throw_counter += 3

    winning_score_idx = 0 if player_scores[0] >= 1000 else 1
    losing_score_idx = 1 - winning_score_idx
    answer_a = die_throw_counter * player_scores[losing_score_idx]
    print(f'The final losing score:    {player_scores[losing_score_idx]}\n'
          f'The number of die throws:  {die_throw_counter}\n'
          f'The product of the two:    {answer_a}')
    if should_submit:
        submit(answer_a, part='a')


example1 = ['Player 1 starting position: 4', 'Player 2 starting position: 8']
# solve(example1)
# solve_a(lines, True)


def solve_b(input, should_submit=False):
    current_position = parse(input)
    possible_steps = Counter([sum([die_1, die_2, die_3])
                             for die_1 in range(1, 4)
                             for die_2 in range(1, 4)
                             for die_3 in range(1, 4)])
    print(possible_steps)

    @lru_cache(maxsize=None)
    def execute_turn(player_data, cur_player):
        win_count = [0, 0]
        for steps, num_occurrences in possible_steps.items():
            new_position = (player_data[2 * cur_player] + steps) % 10
            new_score = player_data[2 * cur_player + 1] + new_position + 1
            if new_score >= 21:
                win_count[cur_player] += num_occurrences
            else:
                if cur_player == 0:
                    new_player_data = (new_position, new_score, player_data[2], player_data[3])
                else:
                    new_player_data = (player_data[0], player_data[1], new_position, new_score)
                new_wins = execute_turn(new_player_data, 1 - cur_player)
                win_count = [win_count[idx] + num_occurrences * new_count for idx, new_count in enumerate(new_wins)]
        return win_count

    number_of_wins = execute_turn((current_position[0], 0, current_position[1], 0), 0)
    print(f'The number of wins for player 1: {number_of_wins[0]}, the number of wins for player 2: {number_of_wins[1]}')
    if should_submit:
        submit(number_of_wins[0], part='b')


# solve_b(example1)
solve_b(lines, True)