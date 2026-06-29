# Number Guessing Game

A terminal-based number guessing game written in Python. Pick a difficulty, guess a number between 1 and 100, and get hot/cold feedback until you solve it or run out of attempts. Results are persisted across sessions with a running stats table.

## Screenshot

```
╭────────────────────────╮
│   Number Guessing Game  │
╰────────────────────────╯

          All-Time Stats
┌──────────┬───────┬──────────┬─────────────────────┐
│ Difficulty│ Games │ Win Rate │ Avg Guesses on Wins │
├──────────┼───────┼──────────┼─────────────────────┤
│ Easy      │     5 │      80% │                 4.5 │
│ Medium    │     3 │      67% │                 5.0 │
│ Hard      │     2 │      50% │                 4.0 │
├──────────┼───────┼──────────┼─────────────────────┤
│ Total     │    10 │      70% │                 4.6 │
└──────────┴───────┴──────────┴─────────────────────┘
```

## Requirements

- Python 3.8+
- [Rich](https://github.com/Textualize/rich)

## Installation

```bash
git clone https://github.com/liuspencer7/guessing-game.git
cd guessing-game
pip install rich
```

## Running the Game

```bash
python game.py
```

Select a difficulty level when prompted:

| Difficulty | Attempts |
|------------|----------|
| Easy       | 10       |
| Medium     | 7        |
| Hard       | 5        |

## Running the Tests

```bash
pip install pytest
pytest
```

The test suite covers game logic, input validation, stats persistence, and display output — 30 tests in total.

## What This Demonstrates

- **Testability by design** — `play_game` accepts the secret number as a parameter rather than generating it internally, making the core loop fully unit-testable without mocking `random`.
- **I/O mocking** — `unittest.mock.patch` intercepts `input()` and `capsys` captures terminal output, enabling thorough behavioral testing of a CLI app.
- **Separation of concerns** — game logic, stats persistence, and display are split into discrete, independently testable functions.
- **Rich terminal UI** — colored feedback, a styled banner, and a formatted stats table using the [Rich](https://github.com/Textualize/rich) library.
- **JSON persistence** — game results accumulate in `stats.json` and are summarized on startup and after each session.
