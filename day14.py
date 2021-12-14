from aocd import submit, lines
from collections import Counter

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
    insertion_rules = {rule.split(' -> ')[0]: rule.split(' -> ')[1] for rule in input[2:]}
    return list(template), insertion_rules


def solve(input, should_submit=False):
    polymer, insertion_rules = parse(input)
    steps = 10
    for _ in range(steps):
        idx = 0
        while idx < len(polymer) - 1:
            pair = ''.join(polymer[idx:idx + 2])
            new_molecule = insertion_rules[pair]
            polymer.insert(idx + 1, new_molecule)
            idx += 2
        print(''.join(polymer))
        # print(Counter(polymer))
    counts = Counter(polymer)
    answer_a = max(counts.values()) - min(counts.values())
    print(f'The difference between the most occurring and least occurring element is: {answer_a}')
    if should_submit:
        submit(answer_a, part='a')


solve(example_1.splitlines())
solve(lines, True)