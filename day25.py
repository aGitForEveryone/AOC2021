from aocd import submit, lines
from helper_functions import *


def parse(input):
    return [list(line) for line in input]


def east_move(line):
    points_to_swap = []
    for idx, char in enumerate(line):
        if char == '.' and line[idx - 1] == '>':
            points_to_swap += [(idx, idx - 1)]
    for swaps in points_to_swap:
        line[swaps[0]], line[swaps[1]] = line[swaps[1]], line[swaps[0]]
    return bool(len(points_to_swap))


def south_move(line, prev_line):
    points_to_swap = []
    for idx, char in enumerate(line):
        if char == '.' and prev_line[idx] == 'v':
            points_to_swap += [idx]
    return points_to_swap, bool(len(points_to_swap))


def solve(input, should_submit=False):
    grid = parse(input)
    step = 1
    while True:
        has_moved = False
        # Do eastbound moves first
        for idx, line in enumerate(grid):
            has_moved_east = east_move(line)
            has_moved = has_moved or has_moved_east
        # Do southbound moves second
        points_to_swap = []
        for idx, line in enumerate(grid):
            new_swaps, has_moved_south = south_move(line, grid[idx - 1])
            points_to_swap.extend([((idx, swap_idx), (idx - 1, swap_idx)) for swap_idx in new_swaps])
            has_moved = has_moved or has_moved_south
        for swaps in points_to_swap:
            line_1, char_1 = swaps[0]
            line_2, char_2 = swaps[1]
            grid[line_1][char_1], grid[line_2][char_2] = grid[line_2][char_2], grid[line_1][char_1]

        if not has_moved:
            print(f'The sea cucumbers have stopped moving after {step} steps.')
            if should_submit:
                submit(step, part='a')
            break
        step += 1


example1 = '''v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>'''

# solve(example1.splitlines())
solve(lines, True)



