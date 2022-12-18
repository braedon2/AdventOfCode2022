
f = open("puzzle_input", "r")
raw_assignments = f.read()
f.close()

assignments = []

for line in raw_assignments.strip().split('\n'):
	first, second = line.split(",")
	assignments.append((
		[int(n) for n in first.split("-")],
		[int(n) for n in second.split("-")]
	))


print(sum([
	1 
	for first, second in assignments
	if 
	(first[0] <= second[0] and first[1] >= second[1])
	or (second[0] <= first[0] and second[1] >= first[1])
	or (first[0] <= second[0] and first[1] >= second[0])
	or (second[0] <= first[0] and second[1] >= first[0])
]))