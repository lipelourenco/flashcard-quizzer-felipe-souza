from pathlib import Path

from main import run_quiz


def test_full_session(tmp_path, monkeypatch, capsys):
    flashcards_file = tmp_path / "cards.json"
    flashcards_file.write_text(
        """
        [
          {"front": "Capital of France", "back": "Paris"},
          {"front": "2+2", "back": "4"},
          {"front": "Color of sky", "back": "Blue"}
        ]
        """,
        encoding="utf-8",
    )

    answers = iter(["Paris", "5", "Blue"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    run_quiz(Path(flashcards_file), "sequential", show_stats=True)

    output = capsys.readouterr().out
    assert "Loaded 3 flashcards" in output
    assert "- Answered: 3" in output
    assert "- Correct: 2" in output
    assert "- Accuracy: 66.7%" in output
