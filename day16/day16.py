from dataclasses import dataclass, field
from collections import deque
import re

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


def build_solutions(valves: list[Valve], prev: Valve, minute=1) -> list[list]:
	if minute > 30 or not valves:
		return []

	solutions = []
	distances = [prev.paths[v.name] for v in valves]
	for valve, d in zip(valves, distances):
		sublist = [v for v in valves if v != valve]
		sub_solutions = build_solutions(sublist, valve, minute+d+1)
		if sub_solutions:
			solutions.extend([[valve] + ss for ss in sub_solutions])
		else:
			solutions.extend([[valve]])

	return solutions	


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
non_zero_valves = [v for _, v in valves.items() if v.flow_rate]
solutions = build_solutions(non_zero_valves, valves['AA'])
print(len(solutions))

solution_pressures = []
for solution in solutions:
	total_pressure = 0
	#pressure = 0
	minute = 30
	current_valve = valves['AA']
	for valve in solution:
		distance = current_valve.paths[valve.name]
		minute -= distance + 1
		if minute > 0:
			total_pressure += valve.flow_rate * minute
		current_valve = valve
	solution_pressures.append(total_pressure)

print(max(solution_pressures))

