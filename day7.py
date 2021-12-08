from aocd import submit, data
import numpy as np


def fuel_calc1(numbers, pos):
    return np.sum(np.abs(numbers - pos))


def fuel_calc2(numbers, pos):
    diff = np.abs(numbers - pos)
    return [np.sum(diff * (diff + 1) / 2)]


def solve(part, numbers):
    if part == 1:
        fuel_calc = fuel_calc1
    else:
        fuel_calc = fuel_calc2
    most_left = np.min(numbers)
    most_right = np.max(numbers)
    fuel_cost = [fuel_calc(numbers, pos) for pos in range(most_left, most_right + 1)]
    least_fuel = int(np.min(fuel_cost))
    best_target_pos = most_left + np.argmin(fuel_cost)
    print(f'Part {part}:')
    print(f'The best target position that takes the least total fuel to reach is {best_target_pos} ({least_fuel} fuel)')
    if part == 1:
        submit(least_fuel, part='a')
    else:
        submit(least_fuel, part='b')


# data = '16,1,2,0,4,2,7,1,2,14'
numbers = np.array(list(map(int, data.split(','))))
solve(1, numbers)
solve(2, numbers)
