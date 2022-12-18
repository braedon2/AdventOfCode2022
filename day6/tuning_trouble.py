def is_marker(sequence):
    unique_characters = set(sequence)
    return len(unique_characters) == len(sequence)

def find_marker(buffer):
    for i in range(13, len(buffer)):
        sequence_to_test = buffer[i-13:i+1]
        if is_marker(sequence_to_test):
            return i + 1

if __name__ == "__main__":
    buffer = input()
    print(find_marker(buffer))

