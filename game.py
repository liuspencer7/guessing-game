import random


DIFFICULTIES = {
    "1": ("Easy", 10),
    "2": ("Medium", 7),
    "3": ("Hard", 5),
}


def choose_difficulty():
    print("\nSelect difficulty:")
    print("  1. Easy   (10 attempts)")
    print("  2. Medium  (7 attempts)")
    print("  3. Hard    (5 attempts)")
    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice in DIFFICULTIES:
            name, attempts = DIFFICULTIES[choice]
            print(f"{name} selected.")
            return attempts
        print("Please enter 1, 2, or 3.")


def play_game(max_attempts, secret):
    print(f"\nI've picked a number between 1 and 100. You have {max_attempts} attempts.")

    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        try:
            guess = int(input(f"Attempt {attempt}/{max_attempts}: "))
        except ValueError:
            print("Please enter a valid number.")
            attempt -= 1
            continue

        if guess < secret:
            print("Too low!", end="")
        elif guess > secret:
            print("Too high!", end="")
        else:
            print(f"Correct! You got it in {attempt} guess{'es' if attempt != 1 else ''}.")
            return

        remaining = max_attempts - attempt
        if remaining > 0:
            print(f" {remaining} attempt{'s' if remaining != 1 else ''} remaining.")
        else:
            print(f"\nOut of attempts! The number was {secret}.")


def main():
    print("=== Number Guessing Game ===")
    while True:
        max_attempts = choose_difficulty()
        secret = random.randint(1, 100)
        play_game(max_attempts, secret)
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
