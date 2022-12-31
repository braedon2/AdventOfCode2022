from common import puzzle_data_as_lines
from itertools import permutations


def adjacent_points(x, y, z):
    return (
        (x+dx, y+dy, z+dz) for dx, dy, dz
        in set(permutations((1, 0, 0))) | set(permutations((-1, 0, 0)))
    )


def part_a(lava_points):
    return sum(
        sum(1 for ap in adjacent_points(*p) if ap not in lava_points)
        for p in lava_points
    )


def part_b(puzzle_data):
    pass


if __name__ == '__main__':
    point_set = set(eval(line) for line in puzzle_data_as_lines('puzzle_input'))
    print(part_a(point_set))
