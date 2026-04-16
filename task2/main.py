import sys


def print_pyramid(n: int) -> None:
    """Print a right-aligned number pyramid of height n."""
    print(f"\n  Pyramid (height={n}):\n")
    for i in range(1, n + 1):
        spaces = " " * (n - i)
        nums = " ".join(str(j) for j in range(1, i + 1))
        print(f"  {spaces}{nums}")
    print()


def print_inverted_pyramid(n: int) -> None:
    """Print an inverted right-aligned number pyramid of height n."""
    print(f"\n  Inverted Pyramid (height={n}):\n")
    for i in range(n, 0, -1):
        spaces = " " * (n - i)
        nums = " ".join(str(j) for j in range(1, i + 1))
        print(f"  {spaces}{nums}")
    print()


def print_diamond(n: int) -> None:
    """Print a number diamond. n controls the half-height (must be >= 1)."""
    print(f"\n  Diamond (half-height={n}):\n")
    # Upper half (including middle)
    for i in range(1, n + 1):
        spaces = " " * (n - i)
        nums = " ".join(str(j) for j in range(1, i + 1))
        print(f"  {spaces}{nums}")
    # Lower half
    for i in range(n - 1, 0, -1):
        spaces = " " * (n - i)
        nums = " ".join(str(j) for j in range(1, i + 1))
        print(f"  {spaces}{nums}")
    print()


def print_pascals_triangle(n: int) -> None:
    """Print Pascal's triangle with n rows."""
    print(f"\n  Pascal's Triangle ({n} rows):\n")
    row = [1]
    max_width = len(" ".join(str(x) for x in _pascal_row(n - 1)))

    for i in range(n):
        row_str = " ".join(str(x) for x in row)
        padding = " " * ((max_width - len(row_str)) // 2)
        print(f"  {padding}{row_str}")
        row = _next_pascal_row(row)
    print()


def _pascal_row(n: int) -> list[int]:
    """Return the n-th row of Pascal's triangle (0-indexed)."""
    row = [1]
    for i in range(1, n + 1):
        row = _next_pascal_row(row)
    return row


def _next_pascal_row(row: list[int]) -> list[int]:
    """Compute the next row of Pascal's triangle from the current row."""
    return [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + [1]


def get_height(prompt: str, min_val: int = 1, max_val: int = 20) -> int:
    """Prompt user for a height/rows value with validation."""
    while True:
        raw = input(prompt).strip()
        if raw.isdigit():
            val = int(raw)
            if min_val <= val <= max_val:
                return val
        print(f"  ✗ Please enter an integer between {min_val} and {max_val}.\n")


MENU = """
╔══════════════════════════════╗
║     Number Pattern Generator ║
╠══════════════════════════════╣
║  1. Pyramid                  ║
║  2. Inverted Pyramid         ║
║  3. Diamond                  ║
║  4. Pascal's Triangle        ║
║  5. Exit                     ║
╚══════════════════════════════╝
"""


def main() -> None:
    print(MENU)
    while True:
        choice = input("Select pattern (1-5): ").strip()

        if choice == "1":
            n = get_height("  Height (1-20): ")
            print_pyramid(n)
        elif choice == "2":
            n = get_height("  Height (1-20): ")
            print_inverted_pyramid(n)
        elif choice == "3":
            n = get_height("  Half-height (1-15): ", max_val=15)
            print_diamond(n)
        elif choice == "4":
            n = get_height("  Rows (1-15): ", max_val=15)
            print_pascals_triangle(n)
        elif choice == "5":
            print("\nGoodbye!")
            sys.exit(0)
        else:
            print("  ✗ Invalid choice. Enter 1-5.\n")
            continue

        input("Press Enter to return to menu...")
        print(MENU)


if __name__ == "__main__":
    main()
