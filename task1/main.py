import random
import sys


def play_game() -> None:
    """Run one round of the number guessing game."""
    secret = random.randint(1, 100)
    attempts = 0
    max_attempts = 10

    print("=" * 40)
    print("   Welcome to the Number Guessing Game!")
    print("=" * 40)
    print(f"I'm thinking of a number between 1 and 100.")
    print(f"You have {max_attempts} attempts. Good luck!\n")

    while attempts < max_attempts:
        remaining = max_attempts - attempts
        print(f"Attempts remaining: {remaining}")

        raw = input("Enter your guess: ").strip()

        if not raw.isdigit() and not (raw.startswith("-") and raw[1:].isdigit()):
            print("  ✗ Please enter a valid integer.\n")
            continue

        guess = int(raw)

        if guess < 1 or guess > 100:
            print("  ✗ Your guess must be between 1 and 100.\n")
            continue

        attempts += 1

        if guess == secret:
            print(f"\n  ✓ Correct! The number was {secret}.")
            print(f"  You guessed it in {attempts} attempt(s).\n")
            return
        elif guess < secret:
            print("  ↑ Too low! Try a higher number.\n")
        else:
            print("  ↓ Too high! Try a lower number.\n")

    print(f"\n  ✗ Out of attempts! The number was {secret}.\n")


def main() -> None:
    while True:
        play_game()
        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("\nThanks for playing! Goodbye.")
            sys.exit(0)
        print()


if __name__ == "__main__":
    main()
