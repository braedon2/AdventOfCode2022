# state
stacks = [[] for i in range(9)]
instructions = []

f = open("puzzle_input", "r")
raw_data = f.read()
f.close()

# parse stacks
raw_stacks = raw_data.strip("\n").split("\n")[:8]
for line in raw_stacks:
	for i, c in enumerate(line):
		if c not in [" ", "[", "]"]:
			stacks[int((i - 1) / 4)].append(c)
[stack.reverse() for stack in stacks]

# parse instructions
raw_instructions = raw_data.strip().split("\n")[10:]
for line in raw_instructions:
	tokens = line.split(" ")
	instructions.append({
		"move": int(tokens[1]), 
		"from": int(tokens[3]),
		"to": int(tokens[5])
	})

# compute instructions
for instruction in instructions:
	crates_to_move = []
	for _ in range(instruction["move"]):
		crates_to_move.append(stacks[instruction["from"]-1].pop())
	stacks[instruction["to"]-1].extend(reversed(crates_to_move))

# print top of stacks
tops = ""
for stack in stacks:
	tops += stack[-1]
print(tops)