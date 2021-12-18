from aocd import submit, lines
import re


def find_explode_target(snail_number, start, direction):
    cur_idx = start
    while 0 < cur_idx < len(snail_number) - 1:
        if snail_number[cur_idx].isdigit():
            opposite_end_target = cur_idx
            while snail_number[opposite_end_target + direction].isdigit():
                opposite_end_target += direction
            if direction < 0:  # we went left in the snail_number
                return int(snail_number[opposite_end_target:cur_idx + 1]), opposite_end_target, cur_idx
            elif direction > 0:  # we went right in the snail_number
                return int(snail_number[cur_idx:opposite_end_target + 1]), cur_idx, opposite_end_target
        cur_idx += direction
    # if we are here then no target number is found
    return 0, -1, -1


def replace_number(snail_number, new_number, start_old_number, end_old_number):
    return snail_number[:start_old_number] + str(new_number) + snail_number[end_old_number + 1:]


def explode_snail_number(snail_number):
    explosions_detected = False
    level_counter = 0
    idx = 0
    while idx < len(snail_number):
        if snail_number[idx] == '[':
            level_counter += 1
        elif snail_number[idx] == ']':
            level_counter -= 1
        if level_counter > 4:
            explosions_detected = True
            # we are currently at an opening bracket and we need to explode a pair
            # furthermore, the rule is that the next pair is a literal pair
            closing_bracket_idx = snail_number.find(']', idx)
            left, right = re.findall('\[(\d+),(\d+)\]', snail_number[idx:closing_bracket_idx + 1])[0]
            left_target, left_start, left_end = find_explode_target(snail_number, idx, -1)
            right_target, right_start, right_end = find_explode_target(snail_number, closing_bracket_idx, 1)
            # Now we start replacing part of the snail number. We work backwards, first the right target, then the
            # current list value, then the left target. In this way we don't need to adjust the indexing after a
            # replacement.
            idx_shift = 0
            if right_start > 0:
                new_number = right_target + int(right)
                snail_number = replace_number(snail_number, new_number, right_start, right_end)
            snail_number = replace_number(snail_number, 0, idx, closing_bracket_idx)
            if left_start > 0:
                new_number = left_target + int(left)
                snail_number = replace_number(snail_number, new_number, left_start, left_end)
                # The left target adjusts the idx if the new number has more digits than the old number
                idx_shift = len(str(new_number)) - len(str(left_target))
            level_counter -= 1
            idx += idx_shift + 1
        else:
            idx += 1
    return snail_number, explosions_detected


def should_split(snail_number):
    return any(map(lambda x: len(x) > 1, re.findall('\d+', snail_number)))


def split_snail_number(snail_number):
    all_digits = re.findall('\d+', snail_number)
    split_number = next(num for num in all_digits if len(num) > 1)
    idx_split_number = snail_number.find(split_number)
    half = int(split_number) // 2
    return replace_number(snail_number, f'[{half},{half+1 if int(split_number) % 2 else half}]',
                          idx_split_number, idx_split_number + len(split_number) - 1)


def split_explode_snail_number(snail_number):
    while True:
        snail_number, explosions_detected = explode_snail_number(snail_number)
        # I believe that once we passed through the whole string once, we won't find any explosions anymore. My input
        # works.
        # while explosions_detected:
        #     snail_number, explosions_detected = explode_snail_number(snail_number)
        if should_split(snail_number):
            snail_number = split_snail_number(snail_number)
        else:
            return snail_number


def get_snail_magnitude(snail_number):
    idx_closing_bracket = snail_number.find(']')
    while idx_closing_bracket >= 0:
        idx_matching_open_bracket = snail_number.rfind('[', 0, idx_closing_bracket)
        left, right = re.findall('\[(\d+),(\d+)\]',
                                 snail_number[idx_matching_open_bracket:idx_closing_bracket + 1])[0]
        magnitude = 3 * int(left) + 2 * int(right)
        snail_number = replace_number(snail_number, magnitude, idx_matching_open_bracket, idx_closing_bracket)
        idx_closing_bracket = snail_number.find(']')
    return int(snail_number)


def solve(input, should_submit=False):
    ######################################################################################################
    # Part a: get the magnitude of the sum of all snail numbers in the input
    ######################################################################################################
    snail_number = input[0]
    for number in input[1:]:
        snail_number = f'[{snail_number},{number}]'
        snail_number = split_explode_snail_number(snail_number)

    magnitude = get_snail_magnitude(snail_number)
    print(f'The magnitude of the resulting snail number is: {magnitude}')
    if should_submit:
        submit(magnitude, part='a')

    ######################################################################################################
    # Part b: get the largest magnitude of the sum of any two snail numbers in the input
    ######################################################################################################
    max_magnitude = 0
    for num1 in input:
        for num2 in input:
            if num2 == num1:
                continue
            snail_number = split_explode_snail_number(f'[{num1},{num2}]')
            magnitude = get_snail_magnitude(snail_number)
            max_magnitude = max([magnitude, max_magnitude])
    print(f'The maximum magnitude from summing any two numbers from the input is: {max_magnitude}')
    if should_submit:
        submit(max_magnitude, part='b')


example1 = '''[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'''

example1_sum = '[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]'
example1_magnitude = 4140

example2 = '''[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]'''

example2_sum = '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'
example2_magnitude = 3488

# print(explode_snail_number('[[[[[9,8],1],2],3],4]'))
# print(explode_snail_number('[7,[6,[5,[4,[3,2]]]]]'))
# print(explode_snail_number('[[6,[5,[4,[3,2]]]],1]'))
# print(explode_snail_number('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]'))
# print(any(map(lambda x: len(x) > 1, re.findall('\d+', '[[[[0,7],4],[15,[0,13]]],[1,1]]'))))
# print(list(map(int, re.findall('\d+', '[[[[0,7],4],[15,[0,13]]],[1,1]]'))))
# print(split_snail_number(split_snail_number('[[[[0,7],4],[15,[0,13]]],[1,1]]')))
# solve(['[[[[4,3],4],4],[7,[[8,4],9]]]', '[1,1]'])
# print(get_snail_magnitude('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'))
solve(lines, True)
