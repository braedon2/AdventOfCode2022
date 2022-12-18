from collections import deque

# state
cycle_history = []

f = open("puzzle_input", "r")
raw_instructions = f.read()
f.close()

# parse instructions
instructions = []
for line in raw_instructions.strip().split("\n"):
	tokens = line.split(" ")
	if tokens[0] == "addx":
		instruction, value = line.split(" ")
		instructions.append((instruction, int(value)))
	else:
		instructions.append(tuple())

# compute instructions, build cycle history
x = 1
cycle = 0
for instruction in instructions:
	if instruction:
		cycle += 1
		cycle_history.append({"cycle": cycle, "x": x})
		cycle += 1
		cycle_history.append({"cycle": cycle, "x": x})
		x += instruction[1]
	else:
		cycle += 1
		cycle_history.append({"cycle": cycle, "x": x})

# render CRT image
current_cycle = 0
for row in range(6):
	line = ""
	for screen_pos in range(40):
		x = cycle_history[current_cycle]["x"]
		if screen_pos in range(x-1, x+2):
			line += "#"
		else:
			line += "."
		current_cycle += 1
	print(line)

