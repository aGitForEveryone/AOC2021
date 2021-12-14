from aocd import submit, lines
import collections
import helper_functions

example_1 = '''NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C'''


def parse(input):
    template = input[0]
    insertion_rules = {}
    for rule in input[2:]:
        pair, new_molecule = rule.split(' -> ')
        insertion_rules[pair] = [new_molecule, [pair[0] + new_molecule, new_molecule + pair[1]]]
    # insertion_rules = {rule.split(' -> ')[0]: rule.split(' -> ')[1] for rule in input[2:]}
    return template, insertion_rules, set([char for pair in insertion_rules.keys() for char in pair])


def generate_full_string(input):
    polymer, insertion_rules, _ = parse(input)
    polymer = list(polymer)
    insertion_rules = {key: val[0] for key, val in insertion_rules.items()}
    print(''.join(polymer))
    steps = 10
    for _ in range(steps):
        idx = 0
        while idx < len(polymer) - 1:
            pair = ''.join(polymer[idx:idx + 2])
            new_molecule = insertion_rules[pair]
            polymer.insert(idx + 1, new_molecule)
            idx += 2
        print(''.join(polymer))


def solve(input, should_submit=False):
    polymer, insertion_rules, unique_letters = parse(input)
    # print(polymer)
    # print(insertion_rules)
    # print(unique_letters)
    pair_counts = {pair: polymer.count(pair) for pair in insertion_rules.keys()}
    letter_counts = {letter: polymer.count(letter) for letter in unique_letters}
    # print(pair_counts)
    # print(letter_counts)
    # print()
    steps = 40
    for step in range(steps):
        if step == 10:
            answer = max(letter_counts.values()) - min(letter_counts.values())
            print(f'The difference between the most occurring and least occurring element is for part a: {answer}')
            if should_submit:
                submit(answer, part='a')
        new_pair_counts = collections.defaultdict(int)
        for pair, count in pair_counts.items():
            if count > 0:
                # print(pair, count)
                letter_counts[insertion_rules[pair][0]] += count
                for new_pair in insertion_rules[pair][1]:
                    new_pair_counts[new_pair] += count
        pair_counts = new_pair_counts
        # print(letter_counts)
        # print(pair_counts)
    answer = max(letter_counts.values()) - min(letter_counts.values())
    print(f'The difference between the most occurring and least occurring element is for part b: {answer}')
    if should_submit:
        submit(answer, part='b')


# generate_full_string(example_1.splitlines())
# generate_full_string(lines)
# solve(example_1.splitlines())
solve(lines, True)

# helper_functions.time_function(solve, [lines])
