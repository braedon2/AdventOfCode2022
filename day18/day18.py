from common import puzzle_data_as_lines
from itertools import permutations
from dataclasses import dataclass, field
from collections import deque


@dataclass
class AirNode:
    point: tuple
    adjecency_list: list = field(default_factory=list)
    visited: bool = False

    def __hash__(self):
        return hash(self.point)


class AirGraph:
    def __init__(self, lava_points):
        self.min_x = min(x for x, _, _ in lava_points)
        self.max_x = max(x for x, _, _ in lava_points)
        self.min_y = min(y for _, y, _ in lava_points)
        self.max_y = max(y for _, y, _ in lava_points)
        self.min_z = min(z for _, _, z in lava_points)
        self.max_z = max(z for _, _, z in lava_points)

        self.air_dict = dict([((x, y, z), AirNode((x, y, z)))
                              for x in range(self.min_x - 1, self.max_x + 2)
                              for y in range(self.min_y - 1, self.max_y + 2)
                              for z in range(self.min_z - 1, self.max_z + 2)
                              if (x, y, z) not in lava_points])

        self._compute_adjacencies()
        self._bfs()

    def _compute_adjacencies(self):
        for node in self.air_dict.values():
            node.adjecency_list = [
                self.air_dict[p] for p in adjacent_points(*node.point)
                if p in self.air_dict
            ]

    def _bfs(self):
        root = self.air_dict[(self.min_x, self.min_y, self.min_z)]
        root.visited = True
        q = deque([root])

        while q:
            v = q.popleft()
            for w in v.adjecency_list:
                if not w.visited:
                    w.visited = True
                    q.append(w)

    def is_reachable(self, air_coord):
        return self.air_dict[air_coord].visited


def adjacent_points(x, y, z):
    return (
        (x + dx, y + dy, z + dz) for dx, dy, dz
        in set(permutations((1, 0, 0))) | set(permutations((-1, 0, 0))))


def part_a(lava_points):
    return sum(
        sum(1 for ap in adjacent_points(*p) if ap not in lava_points)
        for p in lava_points)


def part_b(lava_points):
    airgraph = AirGraph(lava_points)
    return sum(
        sum(
            1 for ap in adjacent_points(*p)
            if ap not in lava_points and airgraph.is_reachable(ap))
        for p in lava_points)


if __name__ == '__main__':
    point_set = set(eval(line) for line in puzzle_data_as_lines('puzzle_input'))
    print(part_a(point_set))
    print(part_b(point_set))
