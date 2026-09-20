# Day 1 - Secret Entrance

The puzzle is about movement inside the given number range. If the movement goes outside one of the edges, it continues in the same direction from the other edge, circulating (MIN or MAX, depending on direction). We are given startimg position of 50, directions to move are left (L - subtract the movement) or right (R - add the movement) and the range is from 0 to 99.

Example of directions:

`L68`
`L30`
`R48`

If starting with 50, L68 means that we subtract 68. This would be -18, but in this case the subtraction would go outside of MIN (zero) and therefore continue the movement from 99, and the end result would be 82.

Example from the puzzle explanation:
```
The dial starts by pointing at 50.
The dial is rotated L68 to point at 82.
The dial is rotated L30 to point at 52.
```

Possible but inefficient way to solve this would be iteration through each direction. We can simulate the whole movement:

```
def get_pointer(initial_pointer, movement, direction):
    pointer = initial_pointer
    for _ in range(movement):
        if direction == "R":
            pointer = pointer + 1
        else:
            pointer = pointer - 1

        if pointer < MIN:
            pointer = MAX
        elif pointer > MAX:
            pointer = MIN

    return pointer
```

And then we count all cases when pointer was 0. I initially started with some kind of loop, although more efficient then the one above. But I noticed that there is more elegant solution with modulo operator. We only need the remainder of division of the movement result with the circular movement (0-99 gives range of 100):

```
def get_pointer(initial_pointer, movement, direction):
    if direction == "R":
        result = initial_pointer + movement
    else:
        result = initial_pointer - movement

    # The circulating movement has 100 positions (0-99)
    circulation_range = 100

    # Remainder of division with this range will be the new pointer
    pointer = result % circulation_range
    
    return pointer
```

The second part changed the goal to count every time when the zero is encountered during the movement. 

Example:
```
The dial starts by pointing at 50.
The dial is rotated L68 to point at 82; during this rotation, it points at 0 once.
The dial is rotated L30 to point at 52.
The dial is rotated R48 to point at 0.
```

This proved to be tricky for me because I didn't handle corner cases correctly. Initially I settled for the brute force solution by iterating through the whole sequence and by counting zeros:

```
def zero_count_brute(initial_pointer, movement, direction):
    zero_count = 0
    pointer = initial_pointer
    for _ in range(movement):
        if direction == "R":
            pointer = pointer + 1
        else:
            pointer = pointer - 1

        if pointer < MIN:
            pointer = MAX
        elif pointer > MAX:
            pointer = MIN

        if pointer == ZERO:
            zero_count += 1

    return zero_count
```

But I wanted to find more efficient solution using division. The example in the puzzle proved informative enough - I only needed to find a way to omit counting the situations when movement starts from zero:

```
def get_zero_count(initial_pointer, movement, direction):
    circulation_range = 100
    
    if direction == "R":
        result = initial_pointer + movement
    else:
        result = initial_pointer - movement

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

    return zero_count
