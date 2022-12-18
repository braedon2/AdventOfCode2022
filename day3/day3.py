priorities = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def parse_rucksacks(raw_rucksack_list):
	return [
		#split_into_compartments(list(rucksack)) 
		list(rucksack)
		for rucksack in raw_rucksack_list.strip().split('\n')
	]


def split_into_compartments(rucksack):
	middle = int(len(rucksack) / 2)
	return rucksack[:middle], rucksack[middle:]


def map_to_misplaced_items(rucksacks):
	def find_misplaced_item(first_compartment, second_compartment):
		return list(set(first_compartment) & set(second_compartment))[0]

	return [
		find_misplaced_item(rucksack[0], rucksack[1])
		for rucksack in rucksacks
	]


def get_priority(item):
	return priorities.find(item) + 1


def sum_priorities(items):
	return sum([get_priority(item) for item in items])


def get_groups(rucksacks):
	groups = []
	current_group = []

	for i in range(len(rucksacks)):
		if i != 0 and i % 3 == 0:
			groups.append(current_group)
			current_group = []
		current_group.append(rucksacks[i])
	groups.append(current_group)

	return groups


def map_to_common_items(rucksack_groups):
	def find_common_item(group):
		return list(set(group[0]) & set(group[1]) & set(group[2]))[0]

	return [find_common_item(group) for group in rucksack_groups]


if __name__ == "__main__":
	f = open("puzzle_input", "r")
	raw_data = f.read()
	f.close()

	rucksacks = parse_rucksacks(raw_data)
	#print(sum_priorities(map_to_misplaced_items(rucksacks)))
	print(sum_priorities(map_to_common_items(get_groups(rucksacks))))
	