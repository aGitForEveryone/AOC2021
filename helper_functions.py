from timeit import default_timer as timer


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