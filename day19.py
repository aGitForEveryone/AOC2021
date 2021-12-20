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
        scan_data[scanner_id] = [np.array(list(map(int, re.findall('-?\d+', coor)))) for coor in scanner[1:]]
    return scan_data


def rotate(locations, axis, steps):
    """ Rotate scanner around axis 90 degrees {steps} times in the clockwise direction"""
    rotation_matrix = {
        'z': np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]),
        'y': np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]]),
        'x': np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
    }
    total_rotation = np.linalg.matrix_power(rotation_matrix[axis], steps)
    return list(map(lambda x: np.matmul(total_rotation, x), locations))


def get_all_rotations(locations):
    rotations = [rotate(rotate(rotate(locations, 'x', step_x), 'z', step_z), 'y', step_y)
                 for step_x in [0, 2]
                 for step_z in range(4)
                 for step_y in range(4)]
    return rotations



example1 = '''--- scanner 0 ---
-1,-1,1
-2,-2,2
-3,-3,3
-2,-3,1
5,6,-4
8,0,7'''


scan_data = parse(example1)
print_list_on_lines(get_all_rotations(scan_data[0]))
# print(get_all_rotations(scan_data[0]))
# for steps in range(0, 5):
#     print(rotate(scan_data[0], 'y', steps))