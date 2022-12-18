def is_in_order(left, right):
	for left_item, right_item in zip(left, right):
		retval = None
		if isinstance(left_item, int) and isinstance(right_item, int):
			if left_item != right_item:
				return left_item < right_item
		else:
			retval = is_in_order(listify(left_item), listify(right_item))
		if retval != None:
			return retval

	if len(left) != len(right):
		return len(left) < len(right)

def listify(list_me_pls):
	if isinstance(list_me_pls, int):
		return [list_me_pls]
	else:
		return list_me_pls


f = open("puzzle_input", "r")
raw_data = f.read()
f.close

# parse packet pairs
packets = []
for line in raw_data.strip().split("\n"):
	if line != "":
		packets.append(eval(line.strip()))
packets.append([[2]])
packets.append([[6]])

# shitty bubble sort
swap = True
while swap:
	swap = False
	for i in range(len(packets)-1):
		packet = packets[i]
		next_packet = packets[i+1]
		if not is_in_order(packet, next_packet):
			tmp = packet
			packets[i] = next_packet
			packets[i+1] = tmp
			swap = True

key = 1
for i, p in enumerate(packets):
	if p == [[2]]:
		key *= (i + 1)
	if p == [[6]]:
		key *= (i + 1)
print(key)







