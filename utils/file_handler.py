"""Utility helpers for reading and writing JSON files and flashcard data."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class FlashcardDataError(Exception):
    """Raised when flashcard data is malformed or missing required fields."""


def load_json(file_path: str | Path) -> Any:
    """Load JSON data from a file path."""
    path = Path(file_path)
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_flashcards(file_path: str | Path) -> list[dict[str, str]]:
    """Load and validate flashcards from either array or object-wrapper JSON formats."""
    path = Path(file_path)

    try:
        data = load_json(path)
    except FileNotFoundError as exc:
        raise FlashcardDataError(f"Flashcard file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise FlashcardDataError(
            f"The flashcard file '{path}' is not valid JSON. "
            f"Please fix the JSON syntax and try again."
        ) from exc

    if isinstance(data, dict):
        if "cards" not in data:
            raise FlashcardDataError(
                "Invalid flashcard format: object input must contain a 'cards' field."
            )
        cards = data["cards"]
    elif isinstance(data, list):
        cards = data
    else:
        raise FlashcardDataError(
            "Invalid flashcard format: expected either a list of cards or an object with a 'cards' list."
        )

    if not isinstance(cards, list):
        raise FlashcardDataError("Invalid flashcard format: 'cards' must be a list.")

    validated_cards: list[dict[str, str]] = []
    for index, card in enumerate(cards, start=1):
        if not isinstance(card, dict):
            raise FlashcardDataError(f"Card #{index} is invalid: each card must be an object.")

        front = card.get("front")
        back = card.get("back")
        if not isinstance(front, str) or not front.strip():
            raise FlashcardDataError(
                f"Card #{index} is missing a valid 'front' field (non-empty string required)."
            )
        if not isinstance(back, str) or not back.strip():
            raise FlashcardDataError(
                f"Card #{index} is missing a valid 'back' field (non-empty string required)."
            )

        validated_cards.append({"front": front.strip(), "back": back.strip()})

    return validated_cards


def save_json(data: Any, file_path: str | Path) -> None:
    """Save JSON-serializable data to a file path."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)
