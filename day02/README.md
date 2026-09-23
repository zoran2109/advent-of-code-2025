# Day 2 - Gift Shop

The puzzle input is a sequence of ranges:

```
11-22,95-115,998-1012, etc
```

And first part of the puzzle demands identifying all numbers within a range that are made only of some sequence of digits repeated twice:

```
11-22 has two sequences, 11 and 22.
95-115 has one, 99.
998-1012 has one, 1010.
```

We can notice that a number is treated both as a _value_ and as a _sequence of digits_. My first thought was that I can iterate through every number in the range and then convert the number to string and check if both halves of the string are the same:

```
double_sequence_digit_numbers = []
for number in the range:
    digit_sequnce = str(number)
    if (both_halves_are_the same(digit_sequence)):
        double_sequence_digit_numbers.append(number)
```

But I wanted to go beyond brute force approach and to see how to make the solution a bit more effective. I noticed two things:

1. If the digit sequence must have two identical halves, _we can rule out sequences (or part of them) that have odd number of digits_. For example, range `222-999` can be skipped because we can't split it to two halves with same number of digits. On the other hand, range `950-1150` can be adjusted to take into account only 4-digit sequences - `1000-1150`, while the `950-999` part can be ignored.
2. _First halves of the sequence start and stop value limit the actual number of sequence possibilies_. If we have range `1234-2345`, first halves of start and stop values are `12` and `23`. They actually present the limited range what the first two digits of the number can be. We can then use this limited `12-23` range to generate possible double digit sequences, e.g. `1212, 1313, 1414, ...`, and check if they fall within the original `1234-2345` range.

My solution tried to limit cases using these insights:

```
double_sequence_digit_numbers = []
for pair in range_pairs:
    # If it can't be divided in two identical digit sequences, ignore
    if range_contains_odd_numbers(pair):
        continue
    
    # Remove part of the range that has odd number of digits
    range_to_check = get_applicable_range(pair)
    
    # We start with string values, and we'll convert the to int when iteration or comparison is needed
    start, stop = range_to_check

    # Take into account only first half of the sequence
    first_half_range = [start[:len(start)//2], stop[:len(stop)//2]]
    first, last = first_half_range

    # Iterate through the 'first-half' range and check if pattern exists within the whole range
    for i in range(int(first), int(last)+1):
        pattern = int(str(i)*2)
        if pattern >= int(start) and pattern <= int(stop):
            double_sequence_digit_numbers.append(pattern)
```

Part two introduced additional complications - we need to take into account every possible repeating pattern that repeats _at least twice_. So, there are lots of possible patterns, for example:

```
12341234 (1234 two times), 123123123 (123 three times), 1212121212 (12 five times), and 1111111 (1 seven times)
```

This demanded adaptation of initial observations:

1. Both odd and even digit sequences must be taken into account, since the patterns are possible in both cases (`12341234` is even, `123123123` is odd).
2. Splitting the digit sequence into halves is applicable only for patterns that are repeated twice. The reasoning behind taking only part of the number and verifying if repeated pattern is within the range stands. But now we need to find all possible pattern lengths and slice digits according to pattern length. If the pattern consists of 2 digits (`12`), we'll take first two digits of range endpoints (start, stop), if it has 3, we'll slice 3, and so on.

But the main problem was to determine possible patterns. This is directly connected to the number of digits in a number and it quickly becomes obvious that the digit length must be divisible with the pattern length. So we should find divisors of the number excluding the number itself, since the pattern needs to be repeated:

```
def get_divisors(number):
    divisors = []
    # Divide the number with two since the range of dividers needed doesn't include the number itself
    for d in range (1, number // 2 + 1):
        if number % d == 0:
            divisors.append(d)
    return divisors
```

Another thing that comes to mind is that patterns/divisors for odd and even digit numbers will differ. This is because different numbers will have different divisors. We need to take into account the whole range, but since they will have different patterns, I have decided to split the range (if needed) into odd-digit part and even-digit part. To revisit part one example - `950-1150` - here the odd digit sequence won't be ignored. The range will be split into `950-999` and `1000-1150` and patterns for both ranges will be checked separately.

Adapted to this findings, my solution was:

```
digits_with_repeating_patterns = []
for pair in range_pairs:
    ranges = get_odd_and_even_digit_range(pair) # Returns odd and even digit array that should be filtered to include non-empty arrays
    for digit_range in ranges:
        start, stop = digit_range
        divisors = get_divisors(len(start))
        
        # We will check each divisor to form patterns of different length
        for d in divisor:
            # Take into account only 'divisor/pattern' length of the sequence
            first, last = start[:d], stop[:d]
            
            # Now the real validation - check if constructed number falls within the range
            for i in range(int(first), int(last)+1):
                pattern = int(str(i) * (int(len(start) / d)))
                if pattern >= int(start) and pattern <= int(stop):
                    digits_with_repeating_patterns.append(pattern)
```

But, wait! The solution was wrong for the sample input. Solution was the sum of all found numbers and the result was a bit high. Upon inspecting the values in digits_with_repeating_patterns I saw that the value `222222` repeated three times. I didn't add the guard to avoid possible duplicates generated by patterns of different length. This edge case was primarily limited to the number that is made of single repeated digit. In this example, patterns `2`, `22`, and `22` have generated the same number. This time I didn't chase optimization. I simply converted the final list to a set to get unique values and this time the solution was correct.
