from aocd import numbers, submit
import numpy as np

answer1 = np.sum(np.diff(numbers)>0)
print(f'Solution day 1, part 1: {answer1}')
submit(answer1, part='a')
threeSums = [np.sum(numbers[idx:idx+3]) for idx in range(len(numbers)-2)]
answer2 = np.sum(np.diff(threeSums)>0)
print(f'Solution day 1, part 2: {answer2}')
submit(answer2, part='b')