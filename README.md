# Advent of code 2025

This repository contains my solutions of AoC for the previous year. After discovering it and starting in 2021, 2025 was the first year that I didn't try to follow through during the event. So this is my try to make-up what I missed.

As per request from AoC site, the full puzzle input is not included in the repo.

## Day 01 - Secret Entrance

The puzzle contains starting value (50) and directions to move inside the range of numbers, from 0 to 99. Directions contain the operation and the number, e.g.:

`
L68
R30
`

"L" means left, so the subtraction must be done with 68, while "R" means that the number must be added. When the operation is done, if the result is below 0 or over 99, the value 'resets' and continues inside the given range. If starting with 50, L68 means that we subtract 68. This would be -18, but in this case the subtraction would go to zero and then from 99, and the end result would be 82.

First part was straightforward and only trick was that there could be values that will 'rotate' through the range multiple times. The goal was to count how many times the operation ends on 0.

Second part changed the goal to count every time when the zero is 'passed' during the operation. This proved to be tricky for me because I probably missed some corner cases. Eventually I settled for the brute force solution by iterating through the whole sequence and ny counting zeros.
