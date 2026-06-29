import json
import pytest
from unittest.mock import patch
from game import play_game, choose_difficulty, load_stats, save_result, display_stats, display_stats_brief


# --- play_game: output ---

def test_correct_on_first_guess(capsys):
    with patch("builtins.input", return_value="50"):
        play_game(5, 50)
    assert "Correct! You got it in 1 guess." in capsys.readouterr().out


def test_correct_uses_plural_guesses(capsys):
    with patch("builtins.input", side_effect=["1", "50"]):
        play_game(5, 50)
    assert "You got it in 2 guesses." in capsys.readouterr().out


def test_too_low_feedback(capsys):
    with patch("builtins.input", side_effect=["30", "50"]):
        play_game(5, 50)
    assert "Too low!" in capsys.readouterr().out


def test_too_high_feedback(capsys):
    with patch("builtins.input", side_effect=["70", "50"]):
        play_game(5, 50)
    assert "Too high!" in capsys.readouterr().out


def test_out_of_attempts(capsys):
    with patch("builtins.input", side_effect=["1", "2", "3"]):
        play_game(3, 50)
    out = capsys.readouterr().out
    assert "Out of attempts! The number was 50." in out
    assert "Correct!" not in out


def test_correct_on_last_attempt(capsys):
    with patch("builtins.input", side_effect=["1", "2", "50"]):
        play_game(3, 50)
    out = capsys.readouterr().out
    assert "Correct! You got it in 3 guesses." in out
    assert "Out of attempts" not in out


def test_remaining_attempts_shown_plural(capsys):
    with patch("builtins.input", side_effect=["1", "50"]):
        play_game(3, 50)
    assert "2 attempts remaining." in capsys.readouterr().out


def test_remaining_attempts_shown_singular(capsys):
    with patch("builtins.input", side_effect=["1", "1", "50"]):
        play_game(3, 50)
    assert "1 attempt remaining." in capsys.readouterr().out


def test_invalid_input_does_not_consume_attempt(capsys):
    with patch("builtins.input", side_effect=["abc", "50"]):
        play_game(1, 50)
    out = capsys.readouterr().out
    assert "Please enter a valid number." in out
    assert "Correct!" in out
    assert "Out of attempts" not in out


def test_invalid_input_shows_error(capsys):
    with patch("builtins.input", side_effect=["xyz", "50"]):
        play_game(5, 50)
    assert "Please enter a valid number." in capsys.readouterr().out


# --- play_game: return values ---

def test_play_game_returns_win_on_correct_guess():
    with patch("builtins.input", return_value="50"):
        won, guesses = play_game(5, 50)
    assert won is True
    assert guesses == 1


def test_play_game_returns_correct_guess_count():
    with patch("builtins.input", side_effect=["1", "2", "50"]):
        won, guesses = play_game(5, 50)
    assert won is True
    assert guesses == 3


def test_play_game_returns_loss_when_out_of_attempts():
    with patch("builtins.input", side_effect=["1", "2", "3"]):
        won, guesses = play_game(3, 50)
    assert won is False
    assert guesses == 3


# --- choose_difficulty ---

def test_choose_difficulty_easy():
    with patch("builtins.input", return_value="1"):
        assert choose_difficulty() == ("Easy", 10)


def test_choose_difficulty_medium():
    with patch("builtins.input", return_value="2"):
        assert choose_difficulty() == ("Medium", 7)


def test_choose_difficulty_hard():
    with patch("builtins.input", return_value="3"):
        assert choose_difficulty() == ("Hard", 5)


def test_choose_difficulty_invalid_then_valid(capsys):
    with patch("builtins.input", side_effect=["0", "abc", "2"]):
        name, attempts = choose_difficulty()
    assert name == "Medium"
    assert attempts == 7
    assert "Please enter 1, 2, or 3." in capsys.readouterr().out


# --- load_stats ---

def test_load_stats_returns_empty_list_when_no_file(tmp_path):
    assert load_stats(str(tmp_path / "stats.json")) == []


def test_load_stats_returns_records_from_file(tmp_path):
    path = str(tmp_path / "stats.json")
    records = [{"difficulty": "Easy", "won": True, "guesses_used": 3, "datetime": "2026-06-29T10:00:00"}]
    with open(path, "w") as f:
        json.dump(records, f)
    assert load_stats(path) == records


# --- save_result ---

def test_save_result_creates_file_with_record(tmp_path):
    path = str(tmp_path / "stats.json")
    record = {"difficulty": "Easy", "won": True, "guesses_used": 3, "datetime": "2026-06-29T10:00:00"}
    save_result(record, path)
    assert load_stats(path) == [record]


def test_save_result_appends_to_existing(tmp_path):
    path = str(tmp_path / "stats.json")
    r1 = {"difficulty": "Easy", "won": True, "guesses_used": 3, "datetime": "2026-06-29T10:00:00"}
    r2 = {"difficulty": "Hard", "won": False, "guesses_used": 5, "datetime": "2026-06-29T11:00:00"}
    save_result(r1, path)
    save_result(r2, path)
    assert load_stats(path) == [r1, r2]


# --- display_stats ---

def test_display_stats_no_games(capsys):
    display_stats([])
    assert "No games played yet" in capsys.readouterr().out


def test_display_stats_totals(capsys):
    stats = [
        {"difficulty": "Easy",   "won": True,  "guesses_used": 4},
        {"difficulty": "Easy",   "won": False, "guesses_used": 10},
        {"difficulty": "Medium", "won": True,  "guesses_used": 6},
    ]
    display_stats(stats)
    out = capsys.readouterr().out
    assert "Total" in out
    assert "67%" in out
    assert "5.0" in out


def test_display_stats_shows_only_played_difficulties(capsys):
    stats = [
        {"difficulty": "Easy", "won": True,  "guesses_used": 4},
        {"difficulty": "Hard", "won": False, "guesses_used": 5},
    ]
    display_stats(stats)
    out = capsys.readouterr().out
    assert "Easy" in out
    assert "Hard" in out
    assert "Medium" not in out


def test_display_stats_per_difficulty_avg(capsys):
    stats = [
        {"difficulty": "Easy", "won": True, "guesses_used": 4},
        {"difficulty": "Easy", "won": True, "guesses_used": 6},
    ]
    display_stats(stats)
    assert "5.0" in capsys.readouterr().out


def test_display_stats_difficulty_with_no_wins(capsys):
    stats = [
        {"difficulty": "Hard", "won": False, "guesses_used": 5},
        {"difficulty": "Hard", "won": False, "guesses_used": 5},
    ]
    display_stats(stats)
    out = capsys.readouterr().out
    assert "Hard" in out
    assert "0%" in out


# --- display_stats_brief ---

def test_display_stats_brief_no_games(capsys):
    display_stats_brief([])
    assert capsys.readouterr().out == ""


def test_display_stats_brief_shows_totals(capsys):
    stats = [
        {"difficulty": "Easy", "won": True,  "guesses_used": 4},
        {"difficulty": "Easy", "won": False, "guesses_used": 10},
        {"difficulty": "Hard", "won": True,  "guesses_used": 6},
    ]
    display_stats_brief(stats)
    out = capsys.readouterr().out
    assert "3 games played" in out
    assert "67% wins" in out
    assert "avg 5.0 guesses on wins" in out


def test_display_stats_brief_singular_game(capsys):
    stats = [{"difficulty": "Easy", "won": True, "guesses_used": 3}]
    display_stats_brief(stats)
    out = capsys.readouterr().out
    assert "1 game played" in out
