from unittest.mock import patch
from game import play_game, choose_difficulty


# --- play_game tests ---

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


# --- choose_difficulty tests ---

def test_choose_difficulty_easy():
    with patch("builtins.input", return_value="1"):
        assert choose_difficulty() == 10


def test_choose_difficulty_medium():
    with patch("builtins.input", return_value="2"):
        assert choose_difficulty() == 7


def test_choose_difficulty_hard():
    with patch("builtins.input", return_value="3"):
        assert choose_difficulty() == 5


def test_choose_difficulty_invalid_then_valid(capsys):
    with patch("builtins.input", side_effect=["0", "abc", "2"]):
        result = choose_difficulty()
    assert result == 7
    assert "Please enter 1, 2, or 3." in capsys.readouterr().out
