from aocd import lines, submit

print(lines)
depth = 0
horizontal_loc = 0
depth_part2 = 0
horizontal_part2 = 0
aim = 0

for command in lines:
    direction, amount = command.split()
    amount = int(amount)
    if direction == 'forward':
        horizontal_loc += amount
        horizontal_part2 += amount
        depth_part2 += aim * amount
    elif direction == 'down':
        depth += amount
        aim += amount
    elif direction == 'up':
        depth -= amount
        aim -= amount
answer1 = depth*horizontal_loc
print(answer1)
submit(answer1, part='a')
answer2 = depth_part2*horizontal_part2
print(answer2)
submit(answer2, part='b')