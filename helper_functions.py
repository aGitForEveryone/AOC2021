from timeit import default_timer as timer
from dataclasses import dataclass


def time_function(f, args, repetitions=3):
    start = timer()
    for _ in range(repetitions):
        f(*args)
    end = timer()
    print(f'Elapsed time: {(end - start) / repetitions:.3f} seconds')


def print_list_on_lines(list_to_print):
    if not isinstance(list_to_print, list):
        raise ValueError(f'You did not supply a list while attempting to custom print lists. You supplied type '
                         f'{type(list_to_print)}')
    for elem in list_to_print:
        print(f'{elem}')


# class CustomVars:
#     black_pixel = '\u2591'
#     white_pixel = '\u2588'
#
#     def replace_black_white_pixels(self, string, old_black, old_white):
#         return string.replace(old_black, self.black_pixel).replace(old_white, self.white_pixel)

black_pixel = '\u2591'
white_pixel = '\u2588'


def replace_black_white_pixels(string, old_black=black_pixel, old_white=white_pixel,
                               new_black=black_pixel, new_white=white_pixel):
    return string.replace(old_black, new_black).replace(old_white, new_white)
