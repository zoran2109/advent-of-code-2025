# Day 2: Gift Shop
# https://adventofcode.com/2025/day/2


def get_divisors(number):
    divisors = []
    # Divide the number with two since the range of dividers needed doesn't include the number itself
    for d in range (1, number // 2 + 1):
        if number % d == 0:
            divisors.append(d)
    return divisors

# The range is split into odd-digit and even-digit part since they require different handling
# There are 4 cases:
# 1. odd-digit range only - e.g. 123-234 - return value: [123, 234], []
# 2. even-digit range only - e.g. 22-33 - return value: [], [22, 33]
# 3. odd-digit start, even-digit end - e.g. 1-20 - return value: [1,9], [11, 20]
# 4. even-digit start, odd-digit end - e.g. 90-110 - return value: [100, 110], [90, 99]
def get_odd_and_even_digit_range(range_arr):
    start, stop = range_arr
    odd, even = [], []

    if len(start) % 2 == 1:
        odd.append(start)
    else:
        even.append(start)

    if len(stop) % 2 == 1:
        odd.append(stop)
        # Split the odd and even-digit part of the range
        if len(odd) == 1:
            odd_start = 10 ** (len(stop) - 1)
            odd.insert(0, str(odd_start))
            even.append(str(odd_start - 1))
    else:
        even.append(stop)
        # Split the even and odd-digit part of the range
        if len(even) == 1:
            even_start = 10 ** (len(stop) - 1)
            even.insert(0, str(even_start))
            odd.append(str(even_start - 1))

    return odd, even


def part_two(range_pairs):
    # Find all numbers with digit sequences that repeat at least twice.
    # Example: 12341234 (1234 two times), 123123123 (123 three times), 1212121212 (12 five times), and 1111111 (1 seven times)
    invalid_sequences = []
    for pair in range_pairs:
        # Exclude empty list from ranges
        ranges = [digit_range for digit_range in get_odd_and_even_digit_range(pair) if len(digit_range) != 0]
        for digit_range in ranges:
            start, stop = digit_range
            divisors = get_divisors(len(start))
            # Check each divisor to form pattern of different length
            for d in divisors:
                first, last = start[:d], stop[:d]
                # Validation - check if constructed number falls within the range
                for i in range(int(first), int(last)+1):
                    pattern = int(str(i) * (int(len(start) / d)))
                    if pattern >= int(start) and pattern <= int(stop):
                        invalid_sequences.append(pattern)
    return invalid_sequences


def part_one(range_arr):
    # Find numbers that are made of sequence of digits repeated twice (e.g. 55, 6464, 1188511885) in given range
    invalid_pairs = []
    for pair in range_arr:
        _, even_digit_range = get_odd_and_even_digit_range(pair)
        # Only even-digit range is applicable since the digit must be even (and consist of pattern repeated twice)
        if not even_digit_range:
            continue

        # We start with string values, and we'll convert the to int when iteration or comparison is needed
        start, stop = even_digit_range

        # Take into account only first half of the sequence since it limits available range for repeating pattern
        first_half_range = [start[:len(start)//2], stop[:len(stop)//2]]
        first, last = first_half_range

        # Iterate through the 'first-half' range and check if pattern exists within the whole range
        for i in range(int(first), int(last)+1):
            pattern = int(str(i)*2)
            if pattern >= int(start) and pattern <= int(stop):
                invalid_pairs.append(pattern)

    return invalid_pairs


def solve(range_pairs):
    first = sum(part_one(range_pairs))
    second  = sum(set(part_two(range_pairs))) # Patterns may repeat, set removes duplicates
    return first, second


def main():
    with open("input.txt") as file:
        puzzle_input = file.read().strip()

    # Every sub-array represents starting and ending value for the range
    # Example: [['11', '22'], ['95', '115'], ...]
    range_pairs = [string_range.split("-") for string_range in puzzle_input.split(",")]

    part_one, part_two = solve(range_pairs)

    print("Part one:", part_one)
    print("Part two:", part_two)

if __name__ == "__main__":
    main()
