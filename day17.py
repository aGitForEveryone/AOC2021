from aocd import submit, data
import re
import numpy as np
import math
from helper_functions import time_function

example1 = 'target area: x=20..30, y=-10..-5'
re_string = '^target area: x=(\d+)..(\d+), y=(-?\d+)..(-?\d+)$'


def parse(input):
    return [int(x) for x in re.findall(re_string, input)[0]]


def find_possible_velocities(low, high, axis, peak_y_velocity=0):
    possible_velocities = []
    range_start = 0 if axis == 'x' else low
    range_stop = high + 1 if axis == 'x' else peak_y_velocity + 1
    for velocity in range(range_start, range_stop):
        cur_pos = 0
        cur_vel = velocity
        condition_checker = cur_vel if axis == 'x' else cur_vel
        while condition_checker >= range_start:
            cur_pos += cur_vel
            if low <= cur_pos <= high:
                possible_velocities += [velocity]
                break
            cur_vel -= 1
            condition_checker = cur_vel if axis == 'x' else cur_vel
    return possible_velocities


def simulate_trajectory(initial_x_velocity, initial_y_velocity, x_low, x_high, y_low, y_high):
    cur_coor = np.array([0, 0])
    velocity = np.array([initial_x_velocity, initial_y_velocity])
    # print(f'Current location: {cur_coor}')
    # print(f'Current velocity: {velocity}\n')
    while True:
        cur_coor += velocity
        if cur_coor[1] < y_low or cur_coor[0] > x_high:
            # print(f'Oh no, we missed the target area, or probe went to far!')
            return None
        if x_low <= cur_coor[0] <= x_high and y_low <= cur_coor[1] <= y_high:
            # print(f'Target area reached at location {cur_coor}!')
            return initial_x_velocity, initial_y_velocity
        velocity[0] = velocity[0] - np.sign(velocity[0])
        velocity[1] -= 1
        # print(f'Current location: {cur_coor}')
        # print(f'Current velocity: {velocity}\n')


def solve(input, should_submit=False):
    x_low, x_high, y_low, y_high = parse(input)
    x_velocity = math.ceil(-0.5 + math.sqrt(0.25 + 2 * x_low))
    y_velocity = -(y_low + 1)
    print(f'\nThe required initial velocity to get to the greatest possible height is ({x_velocity}, {y_velocity}).')
    if should_submit:
        highest_y_point = int(y_velocity * (y_velocity + 1) / 2)
        submit(highest_y_point, part='a')

    possible_x_velocities = find_possible_velocities(x_low, x_high, 'x')
    # print('Possible x velocities: ', possible_x_velocities)

    possible_y_velocities = find_possible_velocities(y_low, y_high, 'y', y_velocity)
    # print('Possible y velocities: ', possible_y_velocities)

    possible_velocities = set()
    for x_velocity in possible_x_velocities:
        for y_velocity in possible_y_velocities:
            # print(f'Trying initial velocity: ({x_velocity}, {y_velocity})')
            possible_velocity = simulate_trajectory(x_velocity, y_velocity, x_low, x_high, y_low, y_high)
            if possible_velocity is not None:
                possible_velocities.add(possible_velocity)

    # print(possible_velocities)
    answer_b = len(possible_velocities)
    print(f'The number of possible initial velocities is: {answer_b}')
    if should_submit:
        submit(answer_b, part='b')


# solve(example1)
# solve(data, True)

time_function(solve, [data])
# print(simulate_trajectory(23, -10, *parse(example1)))