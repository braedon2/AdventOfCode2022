from dataclasses import dataclass
from collections import deque
import math

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


class WindGenerator:
    def __init__(self, directions):
        self.directions = directions
        self.length = len(directions)
        self.i = 0

    def next(self):
        d = self.directions[self.i % self.length]
        self.i += 1
        return d


def map_char_to_delta(c):
    return Point(-1, 0) if c == '<' else Point(1, 0)


def is_valid_rock_position(rock, rock_pile):
    within_walls = all(p.x in range(0, 7) for p in rock.points)
    above_ground = rock.bottom >= 0
    does_not_intersect_pile = not (rock.points & rock_pile)
    return within_walls and above_ground and does_not_intersect_pile


def compute_resting_place(rock: Rock, rock_pile: set[Point], winds: WindGenerator):
    current_rock = rock
    found_resting_place = False

    while not found_resting_place:
        wind_delta = winds.next()
        tmp = current_rock.translate(wind_delta)
        if is_valid_rock_position(tmp, rock_pile):
            current_rock = tmp

        tmp = current_rock.translate(Point(0, -1))
        if is_valid_rock_position(tmp, rock_pile):
            current_rock = tmp
        else:
            found_resting_place = True

    return current_rock


def search_for_pattern(history, pattern):
    for i in range(len(history) - len(pattern) + 1):
        window = history[i:i+len(pattern)]
        if window == pattern:
            return i


f = open('puzzle_input', 'r')
data = f.read()
f.close()

wind_generator = WindGenerator([map_char_to_delta(c) for c in data.strip()])
height = 0
rock_pile = set()
prev_height = 0
history = []
granular_history = []
granular_prev = 0
pattern_size = 7  # this is the size of the pattern found in sample
pattern_que = deque()
trillion = 1_000_000_000_000

for i in range(2022):
    if i % 5 == 0 and rock_pile:
        pattern_que.append(height - prev_height)
        prev_height = height
    if len(pattern_que) > pattern_size:
        history.append(pattern_que.popleft())
    if i % 5 == 0 and len(pattern_que) == pattern_size:
        pattern_start = search_for_pattern(history, list(pattern_que))
        if pattern_start:
            pattern_height = sum(history[pattern_start:])
            pattern_iterations = len(history[pattern_start:]) * 5
            chunks = math.floor(trillion / pattern_iterations)
            leftover = (trillion % pattern_iterations) - (len(history[:pattern_start]) * 5)
            print(chunks * pattern_height + sum(granular_history[pattern_start*5:pattern_start*5+leftover]) + sum(history[:pattern_start]))
            break

    rock = Rock(i % 5, 2, height + 3)
    rock = compute_resting_place(rock, rock_pile, wind_generator)
    height = max(height, rock.get_top() + 1)
    rock_pile |= rock.points

    granular_history.append(height - granular_prev)
    granular_prev = height
