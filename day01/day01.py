# https://adventofcode.com/2025/day/1
# Day 1: Secret Entrance

with open("sample.txt", "r") as file:
    input = file.readlines()

MIN = 0
MAX = 99
ZERO = 0

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def get_new_pointer(initial_pointer, number, operation):
    result = operation(initial_pointer, number)
    pointer = abs(result % 100)
    return pointer

# Part two
def count_all_zeros_in_rotation(initial_pointer, number, operation):
    STEP = 1
    zero_count = 0
    pointer = initial_pointer
    for i in range(number):
        pointer = operation(pointer, STEP)
        if pointer < MIN:
            pointer = MAX
        elif pointer > MAX:
            pointer = MIN
        if pointer == ZERO:
            zero_count += 1
    return zero_count

# Initial value
pointer = 50

# Totals
# Part one
point_at_zero = 0
# Part two
zero_touched = 0

for command in input:
    # Command examples: L68, R48
    number = int(command.strip()[1:])
    operation = add if command[0] == "R" else subtract

    # Part two - count all zeros during rotation in range
    zero_touched += count_all_zeros_in_rotation(pointer, number, operation)

    # Gives the pointer value
    pointer = get_new_pointer(pointer, number, operation)

    # Part one
    if pointer == ZERO:
        point_at_zero += 1

print("Part 1:", point_at_zero)
print("Part 2:", zero_touched)
