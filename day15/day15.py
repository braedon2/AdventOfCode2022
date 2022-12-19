import re

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))


f = open("puzzle_input", "r")
raw_data = f.read()
f.close()

sensor_beacons = []
coverage = set()
row_to_test = 2000000
beacons_at_row = set()

for line in raw_data.strip().split("\n"):
    parsed_coords = list(map(int, re.findall(r"-?\d+", line)))
    sensor = Point(*parsed_coords[:2])
    beacon = Point(*parsed_coords[2:])
    distance = abs(sensor.x - beacon.x) + abs(sensor.y - beacon.y)
    sensor_beacons.append({
        "sensor": sensor, 
        "beacon": beacon, 
        "distance": distance})

for sensor_beacon in sensor_beacons:
    if sensor_beacon["beacon"].y == row_to_test:
        beacons_at_row.add(sensor_beacon["beacon"])

for sensor_beacon in sensor_beacons:
    sensor = sensor_beacon["sensor"]
    coverage_distance = sensor_beacon["distance"]
    distance_from_row = abs(sensor.y - row_to_test)
    difference = coverage_distance - distance_from_row
    for i in range(sensor.x, sensor.x + difference + 1):
        coverage.add(Point(i, row_to_test))
    for i in range(sensor.x - difference, sensor.x):
        coverage.add(Point(i, row_to_test))

print(len(coverage - beacons_at_row))