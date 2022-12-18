import pytest
from day7 import parse_terminal_output, build_dir_tree

output = """
$ cd /
$ ls
dir a
14848514 b.txt
$ cd a
$ ls
dir e
dir h
29116 f
2557 g
$ cd e
$ cd ..
$ cd h
"""

def test_parse_terminal_output():
    result = parse_terminal_output(output)
    assert result[0] == {"command": "cd", "arg": "/"}
    assert result[1] == {"command": "ls", "output": [
        {"type": "dir", "name": "a"}, {"type": "file", "name": "b.txt", "size": 14848514}]}


def test_build_dir_tree():
    commands = parse_terminal_output(output)
    result = build_dir_tree(commands)

    assert result.name == "/"
    assert result.files[0].name == "b.txt"
    assert result.files[0].size == 14848514
    assert result.sub_directories[0].name == "a"
    assert result.sub_directories[0].files[0].name == "f"
    assert result.sub_directories[0].files[0].size == 29116
    assert result.sub_directories[0].sub_directories[0].name == "e"
    assert result.sub_directories[0].sub_directories[1].name == "h"
