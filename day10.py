from aocd import submit, lines

# with open('test10.txt', 'r') as f:
#     lines = f.read().splitlines()

matching_closing = {'(': ')', '[': ']', '<': '>', '{': '}'}
matching_open = {')': '(', ']': '[', '>': '<', '}': '{'}
scoring = {')': 3, ']': 57, '>': 25137, '}': 1197}
open_brackets = ['(', '[', '<', '{']
closing_brackets = [')', ']', '>', '}']


def find_closing_bracket(target, start, line, closing_sequence):
    closing_sequence.append(target)
    if start >= len(line):
        return 'eol', closing_sequence
    # print(''.join(closing_sequence[::-1]))
    cur_idx = start
    while True:
        if line[cur_idx] == target:
            closing_sequence = closing_sequence[:-1]
            # print(''.join(closing_sequence[::-1]))
            return 'ok', (cur_idx, closing_sequence)
        elif line[cur_idx] in open_brackets:
            status, value = find_closing_bracket(matching_closing[line[cur_idx]], cur_idx + 1, line, closing_sequence)
            if status == 'ok':
                cur_idx = value[0] + 1
                closing_sequence = value[1]
                if cur_idx >= len(line):
                    return 'eol', value[1]
            elif status == 'eol':
                return status, value
            elif status == 'error':
                return status, value
        else:
            return 'error', scoring[line[cur_idx]]


syntax_score = 0
incomplete_lines = []
closing_lines = []
for line in lines:
    print(line)
    line_status = ''
    cur_idx = 0
    while line_status not in ['eol', 'error']:
        line_status, response = find_closing_bracket(matching_closing[line[cur_idx]], cur_idx + 1, line, [])
        if line_status == 'error':
            print('error: ', response, '\n')
            syntax_score += response
        elif line_status == 'eol':
            print('incomplete line: ', line, ''.join(response[::-1]), '\n')
            incomplete_lines += [line]
            closing_lines += [''.join(response[::-1])]
        elif line_status == 'ok':
            cur_idx = response[0] + 1

print(f'The syntax error score is: {syntax_score}')
submit(syntax_score, part='a')

auto_complete_scores = []
auto_complete_scoring = {bracket: idx + 1 for idx, bracket in enumerate([')', ']', '}', '>'])}
for line in closing_lines:
    auto_complete_score = 0
    for char in line:
        auto_complete_score *= 5
        auto_complete_score += auto_complete_scoring[char]
    auto_complete_scores += [auto_complete_score]

auto_complete_scores.sort()
print(auto_complete_scores)
final_score = auto_complete_scores[len(auto_complete_scores) // 2]
print(f'The autocomplete score is: {final_score}')
submit(final_score, part='b')