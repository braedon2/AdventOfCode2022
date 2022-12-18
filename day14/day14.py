

class CaveScan:
	def __init__(self, raw_paths):
		self.paths = self._parse_paths(raw_paths)
		self.xrange = self._compute_x_range()
		self.xstart = self.xrange[0]
		self.yrange = self._compute_y_range()
		self.grid = [
			["air" for x in range(*self.xrange)] 
			for y in range(*self.yrange)]
		self._add_rocks_to_grid()

	def is_rock(self, x, y):
		if x not in range(*self.xrange):
			return False
		if y not in range(*self.yrange):
			return False
		return self.grid[y][x - self.xstart] == "rock"

	def _parse_paths(self, raw_paths):
		return[
			[eval(point) for point in line.split(" -> ")]
			for line in raw_paths.strip().split("\n")
		]

	def _compute_x_range(self):
		corners = [point for path in self.paths for point in path]
		return (
			min([point[0] for point in corners]),
			max([point[0] for point in corners]) + 1)

	def _compute_y_range(self):
		corners = [point for path in self.paths for point in path]
		return (
			0,
			max([point[1] for point in corners]) + 1)

	def _add_rocks_to_grid(self):
		for path in self.paths:
			start = path[0]
			for point in path[1:]:
				end = point
				if start[0] == end[0]:
					yoffset = min(start[1], end[1])
					self._add_rocks_to_x(start[0], start[1], end[1])
				if start[1] == end[1]:
					self._add_rocks_y(start[1], start[0], end[0])
				start = end

	def _add_rocks_y(self, y, xstart, xend):
		offset = min(xstart, xend)
		for i in range(abs(xstart - xend) + 1):
			self.grid[y][i + offset - self.xstart] = "rock"

	def _add_rocks_to_x(self, x, ystart, yend):
		offset = min(ystart, yend)
		for i in range(abs(ystart - yend) + 1):
			self.grid[i + offset][x - self.xstart] = "rock"


class SandSimulator:
	def __init__(self, scan):
		self.scan = scan
		self.abyss_reached = False
		self.sand_locations = []
		self.sand_start_x = 500
		self.sand_start_y = 0

	def print(self):
		for y in range(*self.scan.yrange):
			rowstr = f"{y} "
			for x in range(*self.scan.xrange):
				if (x, y) == (self.sand_start_x, self.sand_start_y):
					rowstr += "+"
				elif self.scan.is_rock(x, y):
					rowstr += "#"
				elif (x, y) in self.sand_locations:
					rowstr += "O"
				else:
					rowstr += "."
			print(rowstr)

	def simulate_grain_of_sand(self):
		self._find_resting_place(self.sand_start_x, self.sand_start_y)

	def _find_resting_place(self, x, y):
		if self.abyss_reached == True:
			return
		
		next_x, next_y = self._get_next_point(x, y)
		if next_x == None:
			self.sand_locations.append((x, y))
		elif next_x not in range(*self.scan.xrange) or next_y not in range(*self.scan.yrange):
			self.abyss_reached = True
		else:
			self._find_resting_place(next_x, next_y)

	def _get_next_point(self, x, y):
		test_order = [(x, y+1), (x-1, y+1), (x+1, y+1)]
		for point in test_order:
			px, py = point
			if (not self.scan.is_rock(px, py)) and (not (px, py) in self.sand_locations):
				return (px, py)
		return None, None

f = open("puzzle_input", "r")
raw_data = f.read()
f.close()
scan = CaveScan(raw_data)
SandSimulator(scan).print()

