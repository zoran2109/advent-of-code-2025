# https://adventofcode.com/2025/day/1
# Day 1: Secret Entrance

with open("sample.txt", "r") as file:
    input = file.readlines()

MIN = 0
MAX = 99

ZERO = 0


# Brute-force solution
def get_pointer_and_zero_count_brute(initial_pointer, movement, direction):
    step = 1 # Since we 'walk' through the whole sequence
    zero_count = 0
    pointer = initial_pointer
    for _ in range(movement):
        if direction == "R":
            pointer = pointer + step
        else:
            pointer = pointer - step

        if pointer < MIN:
            pointer = MAX
        elif pointer > MAX:
            pointer = MIN

        if pointer == ZERO:
            zero_count += 1

    return pointer, zero_count

# Revised solution
def get_pointer_and_zero_count(initial_pointer, movement, direction):
    if direction == "R":
        result = initial_pointer + movement
    else:
        result = initial_pointer - movement

    # The circulating movement has 100 positions (0-99)
    circulation_range = 100

    # Remainder of division with this range will be the new pointer
    pointer = result % circulation_range

    # Part two
    # Calculate number of zeros encountered during circulating movement
    zero_count = 0

    # If the movement touches zero or goes outside of the range (0,99), zero_count grows
    if result <= MIN or result > MAX:
        # Calculate how many circulating ranges is the movement long
        # Since we start inside the range, this will determine how many times we encounter zero
        zero_count = abs(result) // circulation_range

    # If the result is negative, we add 1 to the zero_count since additional circular movement is needed for the result to be in the range (and this means 0 is encountered once more)
    # Cover edge case, when rotation starts with zero - in this case we don't count the zero'
    if (result <= MIN and initial_pointer != ZERO):
        zero_count += 1

    return pointer, zero_count


# Initial state
pointer = 50

# Totals
# Part one
point_at_zero = 0
# Part two
zero_count = 0

for command in input:
    # Command examples: L68, R48
    # We split the command to direction (R,L) and movement (68, 48)
    direction = command[0]
    movement = int(command.strip()[1:])

    pointer, zeros_encountered = get_pointer_and_zero_count(pointer, movement, direction)

    # Part one
    if pointer == ZERO:
        point_at_zero += 1

    # Part two
    zero_count += zeros_encountered

print("Part 1:", point_at_zero)
print("Part 2:", zero_count)
