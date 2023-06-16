"""
puzzle input has 5000 numbers 
no number has value 4999, 5000, 5001
some numbers have absolute value greater than 5000
there is a -10000

To keep track of what number to move next, cache the original enumeration so 
you can search for the next number to move by its original index
[3, 5, 1] becomes [(0, 3), (1, 5), (2, 1)]

finding next number to move will take N time in the worst case

scenario 1: number moves forward, does not wrap
[1, 2, 3] moving 1
[2, 1, 3]

scenario 2: number moves forward, wraps behind its original position
[1, 1, 2, 3] moving 2
[1, 2, 1, 3]

scenario 3: number moves forward, wraps ahead of its original position
[1, 2, 7, 3, 4, 5] moving 7
[1, 2, 3, 7, 4, 5]

scenario 4: number moves backward, does not wrap
[3, 2, -1] moving -1
[3, -1, 2]

scenario 5: number moves backward, wraps ahead of its original position
[1, -2, 3, 4] moving -2
[1, 3, -2, 4]

scenario 6:
"""

# moves number at position pos in the list
def move(numbers, pos):
    idx, n = numbers[pos]

    if n == 0:
        return

    new_pos = pos + n
    new_pos = new_pos % len(numbers)

    # edge cases >:^|
    if n < 0 and new_pos > pos:
        new_pos -= 1
    if n < 0 and new_pos == 0:
        new_pos = len(numbers)
    if n > 0 and new_pos < pos:
        new_pos += 1

    del numbers[pos]
    numbers.insert(new_pos, (idx, n))


def find_pos_by_idx(numbers, idx_to_find):
    for pos, (idx, n) in enumerate(numbers):
        if idx == idx_to_find:
            return pos


def find_pos_by_number(numbers, number_to_find):
    for pos, (idx, n) in enumerate(numbers):
        if n == number_to_find:
            return pos


def print_numbers(numbers):
    print([n for _, n in numbers])

with open('sample') as f:
    # cache the original enumeration 
    numbers = [(idx, int(number)) for idx, number in enumerate(f.readlines())]
    
    for i in range(len(numbers)):
        # find the position of the number with the cached index value of i
        pos = find_pos_by_idx(numbers, i)
        # move number at position pos
        move(numbers, pos)
        print_numbers(numbers)

    # find position of 0 number
    pos = find_pos_by_number(numbers, 0)
    answer = sum([
        numbers[(pos+x)%len(numbers)][1] for x in [1000, 2000, 3000]
    ])
    print(answer)
