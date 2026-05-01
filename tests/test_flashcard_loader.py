import pytest

from utils.file_handler import FlashcardDataError, load_flashcards


def test_load_valid_flashcards_array(tmp_path):
    flashcards_file = tmp_path / "cards.json"
    flashcards_file.write_text(
        '[{"front": "Q1", "back": "A1"}, {"front": "Q2", "back": "A2"}]',
        encoding="utf-8",
    )

    cards = load_flashcards(flashcards_file)

    assert cards == [
        {"front": "Q1", "back": "A1"},
        {"front": "Q2", "back": "A2"},
    ]


def test_load_invalid_json(tmp_path):
    flashcards_file = tmp_path / "bad.json"
    flashcards_file.write_text('{"front": "Q1", "back": "A1"', encoding="utf-8")

    with pytest.raises(FlashcardDataError, match="not valid JSON"):
        load_flashcards(flashcards_file)


def test_load_missing_required_field(tmp_path):
    flashcards_file = tmp_path / "missing_back.json"
    flashcards_file.write_text('[{"front": "Q1"}]', encoding="utf-8")

    with pytest.raises(FlashcardDataError, match="missing a valid 'back' field"):
        load_flashcards(flashcards_file)
