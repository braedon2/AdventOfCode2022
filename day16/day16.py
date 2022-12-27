from dataclasses import dataclass, field
from collections import deque
import re
from itertools import chain, combinations
from functools import cache

MINUTES_ALLOTTED = 26

@dataclass
class Valve:
	name: str
	flow_rate: int
	neighbours: list = field(default_factory=list)
	paths: dict = field(default_factory=dict)

	def __repr__(self):
		return f"({self.name} {self.flow_rate})"

	def __str__(self):
		return f"({self.name} {self.flow_rate})"

	def __eq__(self, other):
		return self.name == other.name

	def __hash__(self):
		return hash(self.name)

# from https://docs.python.org/3/library/itertools.html#itertools-recipes
# hacked to only return subsets of size 8
def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(8, 9))


def bfs(root: Valve) -> dict:
	# values in dictionnary represent distance from root
	visited = {root.name: 0}
	q = deque([root])
	while q:
		v = q.popleft()
		for w in v.neighbours:
			if w.name not in visited:
				visited[w.name] = visited[v.name] + 1
				q.append(w)
	return visited


def pre_compute_paths(vavles: dict) -> None:
	for name, valve in valves.items():
		valve.paths = bfs(valve)

#@cache
def build_solutions(
	valves: tuple[Valve], 
	prev: Valve, 
	minute=1) -> list[list]:
	if minute > MINUTES_ALLOTTED or not valves:
		return []

	solutions = []
	distances = [prev.paths[v.name] for v in valves]
	for valve, d in zip(valves, distances):
		sublist = [v for v in valves if v != valve]
		sub_solutions = build_solutions(tuple(sublist), valve, minute+d+1)
		if sub_solutions:
			solutions.extend([[valve] + ss for ss in sub_solutions])
		else:
			solutions.extend([[valve]])

	return solutions			


#@cache
def get_solution_pressure(solution, start):
	total_pressure = 0
	minutes_left = MINUTES_ALLOTTED
	prev_valve = start
	for valve in solution:
		distance = prev_valve.paths[valve.name]
		minutes_left -= distance + 1
		if minutes_left > 0:
			total_pressure += valve.flow_rate * minutes_left
		prev_valve = valve
	return total_pressure


def compute_max_pressure_from_subset_pair(first, second, start):
	pressure = 0
	first_solutions = build_solutions(tuple(first), start)
	second_solutions = build_solutions(tuple(second), start)

	if first_solutions:
		pressure += max([get_solution_pressure(tuple(s), start) for s in first_solutions])

	if second_solutions:
		pressure += max([get_solution_pressure(tuple(s), start) for s in second_solutions])

	return pressure


f = open("puzzle_input", "r")
lines = f.read()
f.close

valves = {}

for line in lines.strip().split("\n"):
	tokens = line.split(" ")
	name = tokens[1]
	flow_rate = re.findall(r"\d+", tokens[4])[0]
	valves[name] = Valve(name, int(flow_rate))

for line in lines.strip().split("\n"):
	tokens = line.split(" ")
	name = tokens[1]
	neighbour_strings = tokens[9:]
	valves[name].neighbours = [valves[n[:2]] for n in neighbour_strings]

pre_compute_paths(valves)
non_zero_valves = [v for (_, v) in valves.items() if v.flow_rate]

current_max = 0
i = 0
for subset in powerset(non_zero_valves):
	print(subset)
	print(current_max)
	i += 1
	complement = set(non_zero_valves) - set(subset)
	pressure = compute_max_pressure_from_subset_pair(subset, complement, valves['AA'])
	if pressure > current_max:
		current_max = pressure

print(current_max)

