from collections.abc import Generator
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Rock:
    def __init__(self, shape: int, left: int, bottom: int):
        self.shape = shape
        self.left = left
        self.bottom = bottom
        self.points: set = self._init_from_shape(shape)

    def _init_from_shape(self, shape: int):
        if shape == 0:
            return {Point(self.left + i, self.bottom) for i in range(4)}
        elif shape == 1:
            return {*(Point(self.left + i, self.bottom + 1) for i in range(3)),
                    *(Point(self.left + 1, self.bottom + i) for i in [0, 2])}
        elif shape == 2:
            return {*(Point(self.left + i, self.bottom) for i in range(2)),
                    *(Point(self.left + 2, self.bottom + i) for i in range(3))}
        elif shape == 3:
            return {Point(self.left, self.bottom + i) for i in range(4)}
        elif shape == 4:
            return {Point(self.left + i, self.bottom + j)
                    for i in range(2) for j in range(2)}

    def translate(self, delta: Point):
        return Rock(self.shape, self.left + delta.x, self.bottom + delta.y)

    def get_top(self):
        return max([p.y for p in self.points])

    def __repr__(self):
        return str(self.points)


def rock_shapes():
    i = 0
    while True:
        yield i % 5
        i += 1


def wind_directions(deltas: list[Point]):
    length = len(deltas)
    i = 0
    while True:
        yield deltas[i % length]
        i += 1


def map_char_to_delta(c):
    return Point(-1, 0) if c == '<' else Point(1, 0)


def is_valid_rock_position(rock, rock_pile):
    within_walls = all(p.x in range(0, 7) for p in rock.points)
    above_ground = rock.bottom >= 0
    does_not_intersect_pile = not (rock.points & rock_pile)
    return within_walls and above_ground and does_not_intersect_pile


def compute_resting_place(rock: Rock, rock_pile: set[Point], winds: Generator):
    current_rock = rock
    found_resting_place = False

    while not found_resting_place:
        wind_delta = next(winds)
        tmp = current_rock.translate(wind_delta)
        if is_valid_rock_position(tmp, rock_pile):
            current_rock = tmp

        tmp = current_rock.translate(Point(0, -1))
        if is_valid_rock_position(tmp, rock_pile):
            current_rock = tmp
        else:
            found_resting_place = True

    return current_rock


def print_rock_pile(rock_pile, height):
    for y in reversed(range(height)):
        line = ''
        for x in range(7):
            if Point(x, y) in rock_pile:
                line += '#'
            else:
                line += '.'
        print(line)


f = open('puzzle_input', 'r')
data = f.read()
f.close()

rock_shape_generator = rock_shapes()
wind_generator = wind_directions([
    map_char_to_delta(c)
    for line in data.strip().split('\n')
    for c in line
])

height = 0
rock_pile = set()

for _ in range(1000000000000):
    rock = Rock(next(rock_shape_generator), 2, height + 3)
    rock = compute_resting_place(rock, rock_pile, wind_generator)
    height = max(height, rock.get_top() + 1)
    rock_pile |= rock.points

print(height)
