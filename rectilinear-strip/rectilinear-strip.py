def bit_pattern(n, bit_position, fold_direction):
    """
    A function that generates a bit pattern for a given bit position and folding direction.

    Parameters:
        n: Total number of bits.
        bit_position: Position of the bit, starting from 1 (MSB).
        fold_direction: Direction of folding, either 'R2L' or 'L2R'.
    """
    pattern = ""
    repeat_count = 2 ** (bit_position - 1)

    for i in range(1, 2 ** n):
        if fold_direction == "R2L":
            pattern += "10" * repeat_count if i % 2 == 0 else "01" * repeat_count
        else:  # L2R
            pattern += "01" * repeat_count if i % 2 == 0 else "10" * repeat_count

    return pattern[: 2 ** n]

def generate_pattern(n, fold_direction):
    """
    A function that generates the complete pattern matrix for a given number of bits and folding direction.

    Parameters:
        n: Total number of bits.
        fold_direction: Direction of folding, either 'R2L' or 'L2R'.
    """
    patterns = []

    for i in range(1, n + 1):
        current_pattern = bit_pattern(n, i, fold_direction)

        if i == n:  # Reverse the bits for the last row
            reversed_pattern = "".join("1" if bit == "0" else "0" for bit in current_pattern)
            patterns.append(reversed_pattern)
        else:
            patterns.append(current_pattern)

    return patterns

def extract_numbers_from_pattern(pattern_matrix):
    """
    A function that extracts numbers from a given pattern matrix by interpreting each column as a binary number.

    Parameters:
        pattern_matrix: List of strings representing the bit patterns.
    """
    numbers = []

    for i in range(len(pattern_matrix[0])):
        binary_string = "".join(row[i] for row in pattern_matrix)
        numbers.append(int(binary_string, 2))

    return numbers

def get_numbers(n, fold_direction="R2L"):
    """
    A function that computes the list of numbers based on the generated bit pattern and folding direction.

    Parameters:
        n: Total number of bits.
        fold_direction: Direction of folding, either 'R2L' or 'L2R'.
    """
    pattern = generate_pattern(n, fold_direction)
    numbers = extract_numbers_from_pattern(pattern)
    return [number + 1 for number in numbers]  # Convert to 1-indexed

if __name__ == "__main__":
    print(f"All 'L2R' folds: {get_numbers(3, 'L2R')}")
    print(f"All 'R2L' folds: {get_numbers(3, 'R2L')}")
