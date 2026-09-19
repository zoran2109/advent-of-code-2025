# https://adventofcode.com/2025/day/1
# Day 1: Secret Entrance

with open("input.txt", "r") as file:
    input = file.readlines()

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def get_new_pointer(total, number, operation):
    result = operation(total, number)
    pointer = abs(result % 100)
    return pointer

def count_zeros(total, number, operation):
    zero_count = 0
    pointer = total
    for i in range(number):
        pointer = operation(pointer, 1)
        if pointer == -1:
            pointer = 99
        elif pointer == 100:
            pointer = 0
        if pointer == 0:
            zero_count += 1
    return zero_count

# Initial value
pointer = 50
# Part one
point_at_zero = 0
# Part two
zero_touched = 0
for command in input:
    number = int(command.strip()[1:])
    operation = add if command[0] == "R" else subtract

    # Part two
    zero_touched += count_zeros(pointer, number, operation)

    # Part one - later because it overwrites the pointer value
    pointer = get_new_pointer(pointer, number, operation)
    if pointer == 0:
        point_at_zero += 1

print("Part 1:", point_at_zero)
print("Part 2:", zero_touched)

