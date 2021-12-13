from aocd import submit, data

example_1 = '''6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5'''


def parse(input):
    dots, fold_instructions = input.split('\n\n')
    return [[int(coor) for coor in dot.split(',')] for dot in dots.split('\n')], \
           [(instruction[11], int(instruction[13:])) for instruction in fold_instructions.split('\n')]


def fold_paper(instruction, dots):
    axis = 0 if instruction[0] == 'x' else 1
    pivot = instruction[1]
    for dot in dots:
        if dot[axis] > pivot:
            diff = dot[axis] - pivot
            new_coor = pivot - diff
            dot[axis] = new_coor
    # print(dots)
    for idx in range(len(dots) - 1, -1, -1):
        # print(idx, dots[idx])
        if dots[idx] in dots[:idx]:
            dots.pop(idx)
    return dots


def solve(input, should_submit=False):
    dots, instructions = parse(input)
    print(dots)
    answer1 = len(fold_paper(instructions[0], dots))
    print(f'The number of dots after folding is: {answer1}')
    if should_submit:
        submit(answer1, part='a')

    # Part b
    for instruction in instructions[1:]:
        dots = fold_paper(instruction, dots)
        # print(dots)

    max_x = max([dot[0] for dot in dots]) + 1
    max_y = max([dot[1] for dot in dots]) + 1
    grid = [[' '] * max_x for _ in range(max_y)]
    for dot in dots:
        grid[dot[1]][dot[0]] = 'O'

    for line in grid:
        print(''.join(line))


solve(example_1)
solve(data, True)



