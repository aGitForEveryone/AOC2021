from aocd import lines, submit

data = [[int(c) for c in line] for line in lines]


def get_adj(row, col, data):
    # Get all adjacent points in the cave grid
    adj = {}
    if row > 0:
        adj[(row - 1, col)] = data[row - 1][col]
    if row < len(data[0]) - 1:
        adj[(row + 1, col)] = data[row + 1][col]
    if col > 0:
        adj[(row, col - 1)] = data[row][col - 1]
    if col < len(data) - 1:
        adj[(row, col + 1)] = data[row][col + 1]
    return adj


def fill_basin(visited, cur_point, data):
    # Recursive function to find all the points in each basin.
    # print(f'Current point: {cur_point}')
    # print(f'Visited list: {visited}')
    adj = [point for point, val in get_adj(*cur_point, data).items() if point not in visited and val != 9]
    visited.extend(adj)
    for point in adj:
        visited = fill_basin(visited, point, data)
    return visited


low_count = 0
low_points = []
for row in range(len(data)):
    for col in range(len(data[0])):
        if all([data[row][col] < adj for adj in list(get_adj(row, col, data).values())]):
            low_count += data[row][col] + 1
            low_points += [(row, col)]

print(low_count)
submit(low_count, part='a')

basin = []
for low in low_points:
    basin += [len(fill_basin([low], low, data))]

basin.sort()
prod = 1
for val in basin[-3:]:
    prod *= val

print(prod)
submit(prod, part='b')