from aocd import submit, lines

with open('test8.txt', 'r') as f:
    test_data = f.read().splitlines()


def parse(data):
    return [[[''.join(sorted(entry)) for entry in part.split()] for part in line.split(' | ')] for line in data]

# input_data = parse(test_data)
input_data = parse(lines)
# print(input_data)

simple_digit_count = 0
for entry in input_data:
    for digit in entry[1]:
        if len(digit) in [2, 3, 4, 7]:
            simple_digit_count += 1

print(f'The number of simple digits in the output is: {simple_digit_count}')
submit(simple_digit_count, part='a')

# digits 1, 4, 7, 8 are found by the length of the string
# digit 9 is found by checking which 6-char digit fully contains the digit 4
# digit 2 is found by checking which 5-char digit is not fully contained in digit 9
# digit 0 is found by checking which 6-char digit fully contains the digit 1
# digit 6 is the remaining 6-char digit
# digit 5 is found by checking which 5-char digit is fully contained in the digit 6
# digit 3 is the remaining digit
output_sum = 0
for entry in input_data:
    configurations = {}
    digits_5 = []
    digits_6 = []
    for digit in entry[0]:
        if len(digit) == 2:
            configurations[digit] = '1'
            one = digit
        elif len(digit) == 3:
            configurations[digit] = '7'
        elif len(digit) == 4:
            configurations[digit] = '4'
            four = digit
        elif len(digit) == 5:
            digits_5 += [digit]
        elif len(digit) == 6:
            digits_6 += [digit]
        elif len(digit) == 7:
            configurations[digit] = '8'
    nine = [digit for digit in digits_6 if all([letter in digit for letter in four])][0]
    configurations[nine] = '9'
    digits_6.remove(nine)
    two = [digit for digit in digits_5 if not all([letter in nine for letter in digit])][0]
    configurations[two] = '2'
    digits_5.remove(two)
    zero = [digit for digit in digits_6 if all([letter in digit for letter in one])][0]
    configurations[zero] = '0'
    digits_6.remove(zero)
    six = digits_6[0]
    configurations[six] = '6'
    digits_6.remove(six)
    if all([letter in six for letter in digits_5[0]]):
        configurations[digits_5[0]] = '5'
        configurations[digits_5[1]] = '3'
    else:
        configurations[digits_5[0]] = '3'
        configurations[digits_5[1]] = '5'
    # print(configurations)

    output_number = int(''.join([configurations[digit] for digit in entry[1]]))
    # print(output_number)
    output_sum += output_number

print(f'The sum of all output numbers is: {output_sum}')
submit(output_sum, part='b')


