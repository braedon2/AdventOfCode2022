class Directory:
    def __init__(self, name):
        self.name = name 
        self.sub_directories = []
        self.files = []

    def size(self):
        size = sum([file.size for file in self.files])
        for sub_dir in self.sub_directories:
            size += sub_dir.size()
        return size 


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size


def parse_terminal_output(raw_terminal_output):
    commands = []
    for line in raw_terminal_output.strip().split('\n'):
        if line[0] == '$':
            commands.append(parse_command(line))
        else:
            add_output_to_command(commands[-1], line)
    return commands


def parse_command(command):
    tokens = command.split()
    command = {}
    command["command"] = tokens[1]
    if len(tokens) == 3:
        command["arg"] = tokens[2]
    return command


def add_output_to_command(command, output):
    if "output" not in command:
        command["output"] = [parse_command_output(output)]
    else:
        command["output"].append(parse_command_output(output))


def parse_command_output(output):
    tokens = output.split()
    if tokens[0] == "dir":
        return {"type": "dir", "name": tokens[1]}
    else:
        return {"type": "file", "name": tokens[1], "size": int(tokens[0])}


def build_dir_tree(commands):
    root = Directory("/")
    dir_stack = [root]

    for command in commands[1:]:
        current_dir = dir_stack[-1]

        if command["command"] == "ls":
            [current_dir.files.append(File(file["name"], file["size"])) 
                for file in command["output"] if file["type"] == "file"]

        elif command["command"] == "cd" and command["arg"] != "..":
            new_dir = Directory(command["arg"])
            current_dir.sub_directories.append(new_dir)
            dir_stack.append(new_dir)

        elif command["command"] == "cd" and command["arg"] == "..":
            dir_stack.pop()

    return root


def find_smallest_dir(root, min_size):
    smallest_size = root.size() # start with largest size

    def traverse(directory):
        nonlocal smallest_size
        if directory.size() >= min_size and directory.size() < smallest_size:
            smallest_size = directory.size()
        for sub_dir in directory.sub_directories:
            traverse(sub_dir)

    traverse(root)
    return smallest_size

if __name__ == "__main__":
    f = open("puzzle_input", "r")
    raw_terminal_output = f.read()
    f.close()

    commands = parse_terminal_output(raw_terminal_output)
    root = build_dir_tree(commands)
    free_space = 70000000 - root.size()
    required_space = 30000000 - free_space 
    print(find_smallest_dir(root, required_space))
