from functools import reduce

def parse_raw_inventory(raw_inventory):
    raw_inventory = raw_inventory.strip()
    lines = raw_inventory.split('\n')
    current_sub_list = 0
    parsed_inventory = [[]]

    for line in lines:
        if line == '':
            current_sub_list += 1
            parsed_inventory.append([])
        else:    
            parsed_inventory[current_sub_list].append(int(line))

    return parsed_inventory

def map_to_total_calories(inventory):
    return [
        sum(calorie_list)
        for calorie_list in inventory
    ]

def find_elf_with_most_calories(raw_inventory):
    parsed_inventory = parse_raw_inventory(raw_inventory)
    total_calories = map_to_total_calories(parsed_inventory)
    return max(total_calories)


def find_top_three_elves_with_most_calories(raw_inventory):
    parsed_inventory = parse_raw_inventory(raw_inventory)
    total_calories = map_to_total_calories(parsed_inventory)

    top_three = []

    for i in range(3):
        top_three.append(max(total_calories))
        total_calories.remove(top_three[i])

    return sum(top_three)



if __name__ == "__main__":
    f = open("test_input", "r")
    raw_inventory = f.read()
    f.close()
    print(find_elf_with_most_calories(raw_inventory))
    print(find_top_three_elves_with_most_calories(raw_inventory))
    print(find_top_three_elves_with_most_calories
