def parse_grid(raw_grid):
	grid = []
	for line in raw_grid.strip().split('\n'):
		grid.append([int(n) for n in list(line)])
	return grid


def get_sorrounding_trees(grid, row, col):
	def get_left_trees():
		return grid[row][:col]

	def get_right_trees():
		return grid[row][col+1:]

	def get_top_trees():
		return [r[col] for r in grid[:row]]

	def get_bottom_trees():
		return [r[col] for r in grid[row+1:]]

	return [
		get_left_trees(),
		get_right_trees(),
		get_top_trees(),
		get_bottom_trees()
	]


def is_visible(grid, row, col):
	sorrounding_trees = get_sorrounding_trees(grid, row, col)
	tree_to_test = grid[row][col]
	return any(all(tree < tree_to_test for tree in trees) for trees in sorrounding_trees)


def count_visible_trees(grid):
	return sum([
		1
		for r in range(len(grid))
		for c in range(len(grid[r]))
		if is_visible(grid, r, c)
	])


def get_scenic_score(grid, row, col):
	tree_to_test = grid[row][col]
	sorrounding_trees = get_sorrounding_trees(grid, row, col)

	def get_view_distance(trees):
		d = 0
		for tree in trees:
			d += 1
			if tree >= tree_to_test:
				break
		return d

	return (
		get_view_distance(reversed(sorrounding_trees[0])) * \
		get_view_distance(sorrounding_trees[1]) * \
		get_view_distance(reversed(sorrounding_trees[2])) * \
		get_view_distance(sorrounding_trees[3])
	)


def get_highest_scenic_score(grid):
	return max([
		get_scenic_score(grid,r,c) 
		for r in range(len(grid)) 
		for c in range(len(grid[r]))
	])


if __name__ == "__main__":
	f = open("puzzle_input", "r")
	raw_grid = f.read()
	f.close()

	grid = parse_grid(raw_grid)
	print (count_visible_trees(grid))
	print(get_highest_scenic_score(grid))