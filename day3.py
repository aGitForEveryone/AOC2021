from aocd import lines, submit
import numpy as np

# print(lines)
# We convert the input in a 2D array of int 1's and 0's
list_lines = np.array([list(line) for line in lines], dtype=np.int)
# print(list_lines)
# list_lines = np.array([[int(num) for num in list_line] for list_line in [list(line) for line in lines]])
ones_count = np.sum(list_lines, axis=0)
count_binary_numbers = len(lines)
gamma_rate = '0b'
epsilon_rate = '0b'
for count in ones_count:
    # Checking on count > count_binary_numbers / 2 works
    # assuming the total amount of binary numbers is odd,
    # which is implied from the question formulation.
    gamma_bit = '1' if count > count_binary_numbers / 2 else '0'
    gamma_rate += gamma_bit
    epsilon_rate += '0' if gamma_bit == '1' else '1'
print(ones_count)
gamma_rate = int(gamma_rate, 2)
epsilon_rate = int(epsilon_rate, 2)
print(f'Gamma rate = {gamma_rate}')
print(f'Epsilon rate = {epsilon_rate}')
answer1 = gamma_rate * epsilon_rate
print(f'The multiplication of both is {answer1}')
submit(answer1, part='a')


def find_rating(rating_type, start_list):
    candidates = start_list
    if rating_type == 'oxygen':
        target_bit = 1
    elif rating_type == 'CO2':
        target_bit = 0
    else:
        raise ValueError(f'Choose different rating type')
    idx = 0
    while len(candidates) > 1:
        # print(f'Finding {rating_type} candidates, checking index: {idx}')
        ones_count = np.sum(candidates, axis=0)
        if ones_count[idx] >= len(candidates) / 2:
            candidates = candidates[candidates[:, idx] == target_bit]
        else:
            candidates = candidates[candidates[:, idx] == 1 - target_bit]
        idx += 1
    print(f'Binary number for {rating_type} rating: {candidates[0]}')
    return candidates[0]


oxygen_generator_rating = int('0b' + ''.join([str(bit) for bit in find_rating('oxygen', list_lines)]), 2)
print(f'Oxygen generator rating: {oxygen_generator_rating}')
CO2_scrubber_rating = int('0b' + ''.join([str(bit) for bit in find_rating('CO2', list_lines)]), 2)
print(f'CO2 scrubber rating: {CO2_scrubber_rating}')
answer2 = oxygen_generator_rating * CO2_scrubber_rating
print(f'The multiplication of both is {answer2}')
submit(answer2, part='b')