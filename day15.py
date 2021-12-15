from aocd import submit, lines
import numpy as np
from helper_functions import *

example_1 = '''1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581'''


def parse(input):
    grid = np.array([list(map(int, line)) for line in input])
    return grid


def parse_b(input):
    base_grid = parse(input)
    grid = base_grid
    for idx in range(1, 5):
        grid = np.concatenate([grid, base_grid + idx], axis=1)
        grid[grid > 9] -= 9
    base_grid = grid
    for idx in range(1, 5):
        grid = np.concatenate([grid, base_grid + idx], axis=0)
        grid[grid > 9] -= 9
    return grid


def get_adjacent_points(point, grid):
    adj_values = []
    if point[0] > 0:
        adj_values += [(point[0] - 1, point[1])]
    if point[0] < grid.shape[0] - 1:
        adj_values += [(point[0] + 1, point[1])]
    if point[1] > 0:
        adj_values += [(point[0], point[1] - 1)]
    if point[1] < grid.shape[1] - 1:
        adj_values += [(point[0], point[1] + 1)]
    return adj_values


def sort_frontier(grid, point):
    return grid[point]


def solve(input, part='a', should_submit=False):
    grid = parse(input) if part == 'a' else parse_b(input)
    start_point = (0, 0)
    visited = {start_point}
    cur_frontier = sorted(get_adjacent_points(start_point, grid), key=lambda x: sort_frontier(grid, x))
    visited.add(point for point in cur_frontier)
    end_point = (grid.shape[0] - 1, grid.shape[1] - 1)
    while end_point not in visited:
        least_risk_point = cur_frontier.pop(0)
        # print(f'Point of least risk: {least_risk_point}, {grid[least_risk_point]}')
        # print(f'Adjacent points: {get_adjacent_points(least_risk_point, grid)}')
        for point in get_adjacent_points(least_risk_point, grid):
            if point not in visited:
                grid[point] += grid[least_risk_point]
                cur_frontier += [point]
                visited.add(point)
        cur_frontier = sorted(cur_frontier, key=lambda x: sort_frontier(grid, x))

    answer = grid[-1, -1]
    print(f'The risk value of the least risk path is: {answer}')
    if should_submit:
        submit(answer, part=part)


# solve(example_1.splitlines(), part='b')
# solve(lines, 'a', True)
# solve(lines, 'b', True)

time_function(solve, [lines, 'b'], 1)
# print(parse_b(example_1.splitlines()))
