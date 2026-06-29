import json
import os
import random
from datetime import datetime

from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


DIFFICULTIES = {
    "1": ("Easy", 10),
    "2": ("Medium", 7),
    "3": ("Hard", 5),
}


def choose_difficulty():
    print("\n[#ffffcc]Select difficulty:[/#ffffcc]")
    print("  1. Easy   (10 attempts)")
    print("  2. Medium  (7 attempts)")
    print("  3. Hard    (5 attempts)")
    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice in DIFFICULTIES:
            name, attempts = DIFFICULTIES[choice]
            print(f"{name} selected.")
            return name, attempts
        print("Please enter 1, 2, or 3.")


def play_game(max_attempts, secret):
    print(f"\nI've picked a number between 1 and 100. You have {max_attempts} attempts.")

    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        try:
            print(f"[#ffffcc]Attempt {attempt}/{max_attempts}:[/#ffffcc] ", end="")
            guess = int(input())
        except ValueError:
            print("Please enter a valid number.")
            attempt -= 1
            continue

        if guess < secret:
            print("[#87ceeb]Too low![/#87ceeb]", end="")
        elif guess > secret:
            print("[#ff6b6b]Too high![/#ff6b6b]", end="")
        else:
            print(f"[green]Correct! You got it in {attempt} guess{'es' if attempt != 1 else ''}.[/green]")
            return True, attempt

        remaining = max_attempts - attempt
        if remaining > 0:
            print(f" [white]{remaining}[/white] attempt{'s' if remaining != 1 else ''} remaining.")
        else:
            print(f"\n[bold red]Out of attempts! The number was {secret}.[/bold red]")

    return False, max_attempts


def load_stats(path="stats.json"):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return json.load(f)


def save_result(record, path="stats.json"):
    stats = load_stats(path)
    stats.append(record)
    with open(path, "w") as f:
        json.dump(stats, f, indent=2)


def display_stats(stats):
    if not stats:
        print("\nNo games played yet. Good luck!\n")
        return

    total = len(stats)
    wins = [s for s in stats if s["won"]]
    win_rate = round(len(wins) / total * 100)
    avg_guesses = round(sum(s["guesses_used"] for s in wins) / len(wins), 1) if wins else 0

    table = Table(title="All-Time Stats")
    table.add_column("Difficulty")
    table.add_column("Games", justify="right")
    table.add_column("Win Rate", justify="right")
    table.add_column("Avg Guesses on Wins", justify="right")

    for name, _ in DIFFICULTIES.values():
        games = [s for s in stats if s["difficulty"] == name]
        if not games:
            continue
        diff_wins = [s for s in games if s["won"]]
        diff_win_rate = round(len(diff_wins) / len(games) * 100)
        diff_avg = round(sum(s["guesses_used"] for s in diff_wins) / len(diff_wins), 1) if diff_wins else 0
        table.add_row(name, str(len(games)), f"{diff_win_rate}%", str(diff_avg))

    table.add_section()
    table.add_row("Total", str(total), f"{win_rate}%", str(avg_guesses), style="bold")

    Console().print(table)
    print()


def display_stats_brief(stats):
    if not stats:
        return
    total = len(stats)
    wins = [s for s in stats if s["won"]]
    win_rate = round(len(wins) / total * 100)
    avg_guesses = round(sum(s["guesses_used"] for s in wins) / len(wins), 1) if wins else 0
    print(f"\n[dim]{total} game{'s' if total != 1 else ''} played  —  {win_rate}% wins  —  avg {avg_guesses} guesses on wins[/dim]")


def main():
    Console().print(Panel("[bold cyan]Number Guessing Game[/bold cyan]", expand=False))
    display_stats(load_stats())
    while True:
        difficulty, max_attempts = choose_difficulty()
        secret = random.randint(1, 100)
        won, guesses_used = play_game(max_attempts, secret)
        save_result({
            "datetime": datetime.now().isoformat(timespec="seconds"),
            "difficulty": difficulty,
            "guesses_used": guesses_used,
            "won": won,
        })
        print("\n[#ffffcc]Play again? (y/n):[/#ffffcc] ", end="")
        again = input().strip().lower()
        if again != "y":
            display_stats(load_stats())
            print("Thanks for playing!")
            break
        display_stats_brief(load_stats())


if __name__ == "__main__":
    main()
