import re
from dataclasses import dataclass

max_x = 4000000
max_y = 4000000

@dataclass
class Point:
    x: int
    y: int


def get_ranges(sensor_beacons, row):
    ranges = set()
    for sensor_beacon in sensor_beacons:
        sensor = sensor_beacon["sensor"]
        coverage_distance = sensor_beacon["distance"]
        distance_from_row = abs(sensor.y - row)
        difference = coverage_distance - distance_from_row
        if difference >= 0:
            ranges.add((sensor.x - difference, sensor.x + difference))

    return sorted(ranges)


def compress_ranges(ranges):
    new_ranges = []
    current_start = ranges[0][0]
    current_end = ranges[0][1]

    for r in ranges[1:]:
        start, end = r[0], r[1]
        if start > current_end + 1:
            new_ranges.append([current_start, current_end])
            current_start = start
            current_end = end
        current_end = max([end, current_end])
    new_ranges.append([current_start, current_end])

    new_ranges[0][0] = max(new_ranges[0][0], 0)
    new_ranges[-1][1] = min(new_ranges[-1][1], max_x)
    return new_ranges


f = open("puzzle_input", "r")
raw_data = f.read()
f.close()

sensor_beacons = []

for line in raw_data.strip().split("\n"):
    parsed_coords = list(map(int, re.findall(r"-?\d+", line)))
    sensor = Point(*parsed_coords[:2])
    beacon = Point(*parsed_coords[2:])
    distance = abs(sensor.x - beacon.x) + abs(sensor.y - beacon.y)
    sensor_beacons.append({
        "sensor": sensor, 
        "beacon": beacon, 
        "distance": distance})

for row in range(max_y):
    ranges = get_ranges(sensor_beacons, row)
    ranges = compress_ranges(ranges)
    if len(ranges) > 1:
        print("found gap")
        x = ranges[0][1] + 1
        print(x * 4000000 + row)

    

