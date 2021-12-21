from aocd import submit, data
import re
import numpy as np
from helper_functions import *


def parse(input):
    scanners = input.split('\n\n')
    scan_data = {}
    for scanner_block in scanners:
        scanner = scanner_block.splitlines()
        # print(scanner)
        scanner_id = int(re.findall('\d+', scanner[0])[0])
        scan_data[scanner_id] = np.array([list(map(int, re.findall('-?\d+', coor))) for coor in scanner[1:]])
    return scan_data


def translate(locations, translation_vector):
    # if len(translation_vector) != 3:
    #     return f'Cannot translate points, the translation vector has {len(translation_vector)} coordinates, but it ' \
    #            f'should have 3 entries. Received translation vector: {translation_vector}'
    return [point + translation_vector for point in locations]


def rotate(locations, axis, steps):
    """ Rotate scanner around axis 90 degrees {steps} times in the clockwise direction"""
    rotation_matrix = {
        'z': np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]),
        'y': np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]]),
        'x': np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
    }
    total_rotation = np.linalg.matrix_power(rotation_matrix[axis], steps)
    return np.stack(list(map(lambda x: np.matmul(total_rotation, x), locations)))


def get_all_rotations(locations):
    for step_z, step_x in [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (0, 3)]:
        for step_y in range(4):
            yield rotate(rotate(rotate(locations, 'x', step_x), 'z', step_z), 'y', step_y)
    # rotations = [rotate(rotate(rotate(locations, 'x', step_x), 'z', step_z), 'y', step_y)
    #              for step_x in [0, 2]
    #              for step_z in range(4)
    #              for step_y in range(4)]
    # return rotations


def is_ndarray_in_list(array_list, array):
    return np.any([np.all(point == array) for point in array_list])


def overlapping_points(left, right):
    overlapping = 0
    new_points = []
    for point in right:
        if tuple(point) in left:
            overlapping += [point]
        else:
            new_points += [point]
    return overlapping, new_points


def solve(input, should_submit=False):
    scan_data = parse(input)
    absolute_field = {tuple(point) for point in scan_data[0]}
    scanner_locations = {0: np.array((0, 0, 0))}
    # print_list_on_lines(absolute_field)
    scanner = 1
    # for scanner in range(1, len(scan_data)):
    while len(scanner_locations) != len(scan_data):
        # print(scanner_locations.keys())
        if scanner in scanner_locations.keys():
            scanner = (scanner + 1) % len(scan_data)
            continue
        found_match = False
        for rotated_locations in get_all_rotations(scan_data[scanner]):
            # print('Rotated locations:')
            # print_list_on_lines(rotated_locations)
            for point_abs in absolute_field:
                for new_point in rotated_locations:
                    translation_vector = np.array(point_abs) - new_point
                    # print(f'Translation vector (location scanner): {translation_vector}')
                    # translated_locations = translate(rotated_locations, translation_vector)
                    translated_locations = {tuple(point) for point in rotated_locations + translation_vector}
                    if len(absolute_field.intersection(translated_locations)) >= 12:
                        absolute_field = absolute_field.union(translated_locations)
                        scanner_locations[scanner] = translation_vector
                    # print('Translated locations')
                    # print_list_on_lines(translated_locations)
                    # overlapping, new_points = overlapping_points(absolute_field, translated_locations)
                    # if len(overlapping) >= 12:
                    #     # print(f'the new points are: {new_points}')
                    #     # print(f'the absolute points are: {absolute_field}')
                    #     absolute_field += new_points
                    #     # print(f'the absolute points are: {absolute_field}')
                    #     scanner_locations[scanner] = translation_vector
                        found_match = True
                        break
                if found_match:
                    break
            if found_match:
                break
        scanner = (scanner + 1) % len(scan_data)

    # print(f'The beacon locations are:')
    # print_list_on_lines(sorted(absolute_field, key=lambda x: x[0]))
    print(f'The scanner locations are: {scanner_locations}')
    answer_a = len(absolute_field)
    print(f'The number of unique beacons in the ocean field are: {answer_a}')
    if should_submit:
        submit(answer_a, part='a')
    solve_b(scanner_locations, should_submit)


def solve_b(input, should_submit):
    max_distance = 0
    for scanner_id, loc in input.items():
        for scanner_id2, loc2 in input.items():
            if scanner_id2 == scanner_id:
                continue
            max_distance = max(max_distance, np.sum(np.abs(loc - loc2)))
    print(f'The largest Manhattan distance between any two scanners is: {max_distance}')
    if should_submit:
        submit(max_distance, part='b')


with open('test19.txt', 'r') as f:
    example2 = f.read()


scanner_locations = {0: (0, 0, 0), 4: (-161, -27, -1255), 7: (-1217, 84, -164), 10: (1073, 116, -1282), 12: (-62, -1041, -158), 15: (1151, -1207, -50), 16: (-153, -28, 1079), 22: (-128, 1223, -1233), 23: (2416, 119, -1371), 25: (2380, -1060, -1261), 27: (-1223, 1198, -168), 30: (-87, 39, -2421), 31: (-136, 1288, 1131), 1: (-78, 1197, -2568), 9: (-1172, -1188, -1244), 24: (-1322, 65, -2438), 29: (-14, -1099, -2429), 37: (-1291, 1361, -2440), 2: (-1307, -1070, -2457), 3: (-2392, 97, -2533), 6: (-14, -1069, -3784), 13: (-112, -2253, -2491), 19: (-1340, -1153, -3781), 20: (1168, -1164, -3614), 26: (-37, -1183, -4924), 28: (2, -2239, -4871), 33: (1051, 79, -3767), 35: (-1217, -1202, -4928), 36: (-2372, -1078, -2397), 14: (-1331, -2263, -4980), 17: (2241, -1171, -3739), 21: (1124, 1277, -3616), 32: (-2499, -2399, -4977), 34: (-1240, -2335, -6023), 5: (2389, 1338, -3708), 8: (-2421, -2343, -3660), 11: (-1304, -3455, -4933), 18: (1043, 2369, -3730)}

example1 = '''--- scanner 0 ---
-1,-1,1
-2,-2,2
-3,-3,3
-2,-3,1
5,6,-4
8,0,7'''

example3 = '''--- scanner 0 ---
0,2,0
4,1,0
3,3,0

--- scanner 1 ---
-1,-1,0
-5,0,0
-2,1,0'''
solve(data, True)
# solve(example2)
# scan_data = parse(example1)
# for idx, loc in enumerate(get_all_rotations(scan_data[0])):
#     print(f'locations for rotation {idx}')
#     print_list_on_lines(loc)
# print(scan_data[0])
# print(translate(scan_data[0], [1, 2, 3]))
# print_list_on_lines(get_all_rotations(scan_data[0]))
# print(get_all_rotations(scan_data[0]))
# for steps in range(0, 5):
#     print(rotate(scan_data[0], 'y', steps))