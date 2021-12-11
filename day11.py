from aocd import lines, submit
import numpy as np

# with open('test11.txt', 'r') as f:
#     lines = f.read().splitlines()

possible_points = {(x, y) for x in range(len(lines[0])) for y in range(len(lines))}


def get_adj(x0, y0, has_flashed):
    adj_points = {(x, y) for x in range(x0 - 1, x0 + 2) for y in range(y0 - 1, y0 + 2)}.intersection(possible_points)
    return [point for point in adj_points if not has_flashed[point]]


data = np.array([[int(num) for num in line] for line in lines])

step = 0
flash_count = 0
print(data)
while True:
    data += 1
    # print(data)
    # check=0
    has_flashed = np.zeros_like(data, dtype=bool)
    while np.any(data > 9):
        flash_locations = np.transpose((data > 9).nonzero())
        for x, y in flash_locations:
            has_flashed[x, y] = True
            data[x, y] = 0
            for adj in get_adj(x, y, has_flashed):
                data[adj] += 1
            # print(data)
            # check=0
    if step < 100:
        flash_count += np.sum(has_flashed)
    elif step == 100:
        print(flash_count)
        submit(flash_count, part='a')
    step += 1
    if np.all(has_flashed):
        print(step)
        submit(step, part='b')
        break

    # print(data)