from collections import deque

class Node:
	def __init__(self):
		self.char = None
		self.height = None
		self.adjacent_nodes = []
		self.visited = False
		self.parent = None

	def __str__(self):
		return f"{self.char}: {[n.char for n in self.adjacent_nodes]}" 

def get_height(character):
	if character == "S":
		return ord("a")
	if character == "E":
		return ord("z")
	return ord(character)

def get_adjacent_nodes(r, c, heightmap, height_map_graph):
	root = height_map_graph[r][c]
	adjacent_nodes = []
	for vertical, horizontal in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
		if r + vertical not in range(len(heightmap)):
			continue
		if c + horizontal not in range(len(heightmap[0])):
			continue

		char = heightmap[r+vertical][c+horizontal]
		height = get_height(char)
		if height - root.height in range(-100, 2): # just needed a low negative bound
			adjacent_nodes.append(height_map_graph[r+vertical][c+horizontal])
	return adjacent_nodes

def clear_visited(graph):
	for r in range(len(graph)):
		for c in range(len(graph[0])):
			graph[r][c].visited = False
			graph[r][c].parent = None

def get_shortest_path(root, graph):
	clear_visited(graph)
	root.visited = True
	end_node = None
	q = deque([root])
	while q:
		v = q.popleft()
		if v.char == "E":
			end_node = v
		for w in v.adjacent_nodes:
			if not w.visited:
				w.visited = True
				w.parent = v
				q.append(w)

	if not end_node:
		return None

	current_node = end_node
	length = 0
	while current_node.parent:
		current_node = current_node.parent
		length += 1
	return length

# load heightmap
f = open("puzzle_input", "r")
heightmap = [list(line) for line in f.read().strip().split("\n")]
f.close()

# convert heightmap to Nodes
height_map_graph = [[Node() for c in r]for r in heightmap]
for i, r in enumerate(heightmap):
	for j, c in enumerate(r):
		node = height_map_graph[i][j]
		node.char = c
		node.height = get_height(c)
		node.adjacent_nodes = get_adjacent_nodes(i, j, heightmap, height_map_graph)

# find starting points
starting_nodes = []
for i, r in enumerate(heightmap):
	for j, c in enumerate(r):
		if heightmap[i][j] in ["S", "a"]:
			starting_nodes.append(height_map_graph[i][j])

# find best starting point
shortest_paths = []
for node in starting_nodes:
	length = get_shortest_path(node, height_map_graph)
	if length:
		shortest_paths.append(length)
print(min(shortest_paths))





