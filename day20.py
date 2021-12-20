from aocd import submit, data
from helper_functions import *


def enlarge_grid(image, empty_line_pixel=black_pixel, num_lines=1):
    image = [f'{num_lines * empty_line_pixel + line + num_lines * empty_line_pixel}' for line in image]
    empty_line = empty_line_pixel * (len(image[0]))
    return num_lines * [empty_line] + image + num_lines * [empty_line]


def parse(input):
    enhancement_protocol, image = input.split('\n\n')
    image = enlarge_grid(replace_black_white_pixels(image, '.', '#').splitlines(), num_lines=2)
    return replace_black_white_pixels(enhancement_protocol, '.', '#'), image


def construct_enhancement_index(input_pixels):
    """ input_pixels is a list of three lists with each three characters. Those lists should be appended into one
    string, then converted to a binary number, and then converted to an integer that serves as index for the image
    enhancement protocol"""
    return int(replace_black_white_pixels(f'{"".join(input_pixels)}', new_black='0', new_white='1'), 2)


def solve(input, image_enhancement_iterations, should_submit=False):
    enhancement_protocol, image = parse(input)
    # print_list_on_lines(image)
    for iteration in range(image_enhancement_iterations):
        new_grid = []
        for line_idx, line in enumerate(image[1:-1]):
            # In this for loop we start iteration at the second line. Therefore, the line_idx is shifted by one when
            # accessing the full image.
            new_line = []
            for char_pos in range(1, len(line) - 1):
                enhancement_index = construct_enhancement_index([image[row][char_pos - 1: char_pos + 2]
                                                                 for row in range(line_idx, line_idx + 3)])
                new_line += [enhancement_protocol[enhancement_index]]
            new_grid += [''.join(new_line)]
        image = enlarge_grid(new_grid,
                             enhancement_protocol[0] if image[0][0] == black_pixel else enhancement_protocol[-1], 2)
        # print_list_on_lines(image)
    answer = ''.join(image).count(white_pixel)
    print(f'The number of lit pixels after {image_enhancement_iterations} iterations is {answer}')
    if should_submit:
        if image_enhancement_iterations == 2:
            submit(answer, part='a')
        elif image_enhancement_iterations == 50:
            submit(answer, part='b')
        else:
            print(f'The number of iterations is not 2 or 50, cannot submit answer.')


with open('input20.txt', 'r') as f:
    example1 = f.read()

# solve(example1)
solve(data, 2, True)
solve(data, 50, True)
