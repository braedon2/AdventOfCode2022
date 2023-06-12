def puzzle_data_as_lines(filename: str) -> list[str]:
    with open(filename, 'r') as f:
        return f.read().strip().split('\n')

