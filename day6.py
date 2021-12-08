from aocd import submit, data
import datetime

# Test input
# data = '3,4,3,1,2'


def print_fish_list(fish_per_day, cur_idx):
    output = '['
    for idx in range(len(fish_per_day)):
        if idx == cur_idx:
            output += f'-{fish_per_day[idx]}, '
        else:
            output += f'{fish_per_day[idx]}, '
    else:
        output = output[:-2]
        output += ']'
    return output


fish_list = [int(x) for x in data.split(',')]
fish_per_day = [fish_list.count(day) for day in range(9)]
target_day = 256
cur_day = 0
last_week = fish_per_day[:]
idx = 0
# print(f'Currently at day 0. Number of fish born each day: {print_fish_list(fish_per_day, idx)}.')
start_time = datetime.datetime.now()
program_start_time = start_time
while cur_day < target_day:
    if idx == 0:
        print(f'Number of fish at day {cur_day}: {print_fish_list(fish_per_day, 0)}.')
        if cur_day > 0:
            print(f'Difference with last week: {print_fish_list([fish_per_day[i] - last_week[i] for i in range(len(fish_per_day))], 0)}.')
        last_week = fish_per_day[:]
    # print(f'Currently at day {cur_day + 1}.', end=' ')
    fish_per_day[(idx + 7) % 9] += fish_per_day[idx]
    cur_day += 1
    idx = (idx + 1) % 9
    # print(f'Number of fish born each day: {print_fish_list(fish_per_day, idx)}.', end=' ')
    if cur_day == 80:
        answer1 = sum(fish_per_day)
        submit(answer1, part='a')
        print(f'The number of lantern fish after {cur_day} days is: {answer1}')
    if cur_day == 128:
        print(f'Fish at day 128: {print_fish_list(fish_per_day, idx)}')
    # cur_time = datetime.datetime.now()
    # print(f'Processed day in {cur_time.timestamp() - start_time.timestamp():.3f} seconds.')
    # start_time = cur_time

print(f'Total time for program to run {target_day} days: {datetime.datetime.now().timestamp() - program_start_time.timestamp():.3f} seconds.')
answer2 = sum(fish_per_day)
submit(answer2, part='b')
# answer test input = 26984457539
print(f'The number of lantern fish after {cur_day} days is: {answer2}')
print(print_fish_list(fish_per_day, idx))


