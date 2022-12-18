class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return f"(x: {self.x}, y: {self.y})"

class RopeGrid:
	def __init__(self, num_knots):
		self.tail_history = set([(0, 0)])
		self.knots = [Point(0, 0) for n in range(num_knots)]
		self.head = self.knots[0]
		self.tail = self.knots[-1]

	def move_head(self, direction):
		#print([str(knot) for knot in self.knots])
		if direction == "R":
			self.head.x += 1
		if direction == "U":
			self.head.y += 1
		if direction == "L":
			self.head.x -= 1
		if direction == "D":
			self.head.y -= 1
		self._update_trailing_knots()

	def _update_trailing_knots(self):
		i = 1
		for knot in self.knots[1:]:
			self._update_knot(
				leading=self.knots[i-1], 
				trailing=knot)
			i += 1
		self.tail_history |= {(self.tail.x, self.tail.y)}

	def _one_closer_to_zero(self, n):
		if n < 0:
			return n + 1
		elif n > 0:
			return n - 1
		else:
			return 0

	def _update_knot(self, leading, trailing):
		x_diff = leading.x - trailing.x
		y_diff = leading.y - trailing.y 

		if abs(x_diff) == 2 or abs(y_diff) == 2:
			trailing.x += self._one_closer_to_zero(x_diff)
			trailing.y += self._one_closer_to_zero(y_diff)

			if abs(x_diff) == 1:
				trailing.x += x_diff
			if abs(y_diff) == 1:
				trailing.y += y_diff


f = open("puzzle_input", "r")
raw_motions = f.read()
f.close()

grid = RopeGrid(10)
motions = []

for motion in raw_motions.strip().split("\n"):
	d, s = motion.split(" ")
	motions.append((d, int(s)))

for motion in motions:
	direction, steps = motion
	for _ in range(steps):
		grid.move_head(direction)

print(len(grid.tail_history))