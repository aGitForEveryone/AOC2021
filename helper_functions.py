from timeit import default_timer as timer


def time_function(f, args, repetitions=3):
    start = timer()
    for _ in range(repetitions):
        f(*args)
    end = timer()
    print(f'Elapsed time: {(end - start) / repetitions:.3f} seconds')