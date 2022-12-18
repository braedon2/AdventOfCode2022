class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))


def get_next_point(point, rocks, sand, floor):
    test_order = [
        Point(point.x, point.y+1),
        Point(point.x-1, point.y+1),
        Point(point.x+1, point.y+1)]

    for test_point in test_order:
        if test_point not in (rocks | sand) and test_point.y < floor:
            return test_point
    return point


sample = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

f = open("puzzle_input", "r")
raw_data = f.read()
f.close()

paths = [
    [Point(*eval(point)) for point in line.split(" -> ")]
    for line in raw_data.strip().split("\n")]

rocks = set()
for path in paths:
    for first, second in zip(path, path[1:]):
        startx, endx = sorted([first.x, second.x])
        starty, endy = sorted([first.y, second.y])
        rocks |= set(([Point(i, j) 
            for i in range(startx, endx + 1)
            for j in range(starty, endy + 1)]))

floor = max([r.y for r in rocks]) + 2
print(floor)
sand = set()
while Point(500, 0) not in sand:
    current_point = Point(500, 0)
    found_new_point = True
    while found_new_point:
        next_point = get_next_point(current_point, rocks, sand, floor)
        if next_point == current_point:
            found_new_point = False
        current_point = next_point
    sand.add(current_point)
    print(len(sand), min(s.y for s in sand))


print(len(sand))