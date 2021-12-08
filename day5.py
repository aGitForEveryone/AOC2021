from aocd import lines, submit
import re
import numpy as np
#
# with open('test.txt', 'r') as f:
#     lines = f.readlines()


def get_points_on_line(x1, y1, x2, y2):
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    return [(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)]


def get_points_on_diagonal(x1, y1, x2, y2):
    step_y = -1 if y1 > y2 else 1
    step_x = -1 if x1 > x2 else 1
    return [(x1 + idx * step_x, y1 + idx * step_y) for idx in range(abs(x2 - x1) + 1)]


re_string = '^(\d+),(\d+) -> (\d+),(\d+)$'
# print(lines)
points = {}
points_part_b = {}
for line in lines:
    # print(re.findall(re_string, line)[0])
    x1, y1, x2, y2 = [int(num) for num in re.findall(re_string, line)[0]]
    if x1 == x2 or y1 == y2:
        points_on_line = get_points_on_line(x1, y1, x2, y2)
        for point in points_on_line:
            if point in points:
                points[point] += 1
            else:
                points[point] = 1
    else:
        points_on_line = get_points_on_diagonal(x1, y1, x2, y2)

    # print(f'Point 1: ({x1}, {y1}). Point 2: ({x2}, {y2}).')
    # print(f'Points on line: {points_on_line}')
    for point in points_on_line:
        if point in points_part_b:
            points_part_b[point] += 1
        else:
            points_part_b[point] = 1
# print(np.array(points.values()))
answer1 = np.sum(np.array(list(points.values())) > 1)
submit(answer1, part='a')
print(f'The number of points that have 2 or more horizontal or vertical lines crossing them is {answer1}')
answer2 = np.sum(np.array(list(points_part_b.values())) > 1)
submit(answer2, part='b')
print(f'The number of points that have 2 or more horizontal, vertical or diagonal lines crossing them is {answer2}')
