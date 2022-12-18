import inspect
from collections import deque

reducer = 17 * 7 * 13 * 2 * 19 * 5 * 11 * 3

def make_operation(operator, value):
	if operator == "*":
		if value != "old":
			return lambda old: old * int(value)
		else:
			return lambda old: old * old
	elif operator == "+":
		if value != "old":
			return lambda old: old + int(value)
		else:
			return lambda old: old + old

def make_test(divisor, true_monkey_id, false_monkey_id):
	return lambda item: true_monkey_id if item % divisor == 0 else false_monkey_id

class Monkey:
	def __init__(self, m_id, items, operation, test, divisor):
		self.m_id = m_id
		self.items = deque(items)
		self.operation = operation
		self.test = test
		self.inspection_history = 0
		self.divisor = divisor

# read raw data
f = open("puzzle_input", "r")
raw_data = f.read()
f.close()

# parse raw data into list of raw monkey data
raw_monkeys = [[]]
current_raw_monkey = 0
for line in raw_data.strip().split("\n"):
	if line.strip().split(" ") != [""]:
		raw_monkeys[current_raw_monkey].append(line)
	else:
		raw_monkeys.append([])
		current_raw_monkey += 1

# parse raw monkey data into Monkey objects
monkeys = []
for rm in raw_monkeys:
	tokens = [line.strip().split(" ") for line in rm]
	m_id = int(tokens[0][1][0])
	items = [int(raw_item.strip(",")) for raw_item in tokens[1][2:]]
	operation = make_operation(tokens[2][4], tokens[2][5])
	test = make_test(int(tokens[3][3]), int(tokens[4][5]), int(tokens[5][5]))
	divisor = int(tokens[3][3])
	monkeys.append(Monkey(m_id, items, operation, test, divisor))

# compute rounds
for i in range(10000):
	print("round ", i + 1)
	for monkey in monkeys:
		while monkey.items:
			item = monkey.items.popleft()
			item = monkey.operation(item)
			monkey.inspection_history += 1
			item = item % reducer
			destination = monkey.test(item)
			monkeys[destination].items.append(item)

	print([m.inspection_history for m in monkeys])

# compute monkey business
sorted_monkeys = sorted(monkeys, key=lambda m: m.inspection_history)
print (sorted_monkeys[-1].inspection_history * sorted_monkeys[-2].inspection_history)

