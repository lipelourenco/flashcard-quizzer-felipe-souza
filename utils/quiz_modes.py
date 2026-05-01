"""Quiz engine strategies and factory for serving flashcard questions."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
import random
from typing import Iterable


Card = dict[str, str]


class QuizMode(ABC):
    """Abstract strategy for selecting the next flashcard."""

    def __init__(self, cards: Iterable[Card]) -> None:
        cards_list = list(cards)
        if not cards_list:
            raise ValueError("QuizMode requires at least one card.")
        self._cards = cards_list

    @abstractmethod
    def get_next_question(self) -> Card | None:
        """Return the next card, or None when no cards remain for this session."""

    def record_result(self, card: Card, is_correct: bool) -> None:
        """Record whether a card was answered correctly.

        Default behavior is a no-op for modes that do not adapt.
        """


class SequentialMode(QuizMode):
    """Serve cards in original order: 1, 2, 3..."""

    def __init__(self, cards: Iterable[Card]) -> None:
        super().__init__(cards)
        self._index = 0

    def get_next_question(self) -> Card | None:
        if self._index >= len(self._cards):
            return None
        card = self._cards[self._index]
        self._index += 1
        return card


class RandomMode(QuizMode):
    """Serve cards in shuffled order."""

    def __init__(self, cards: Iterable[Card]) -> None:
        super().__init__(cards)
        self._shuffled_cards = self._cards[:]
        random.shuffle(self._shuffled_cards)
        self._index = 0

    def get_next_question(self) -> Card | None:
        if self._index >= len(self._shuffled_cards):
            return None
        card = self._shuffled_cards[self._index]
        self._index += 1
        return card


class AdaptiveMode(QuizMode):
    """Prioritize cards answered incorrectly by re-queuing them near the front."""

    def __init__(self, cards: Iterable[Card]) -> None:
        super().__init__(cards)
        self._queue: deque[Card] = deque(self._cards)
        self._in_review: list[Card] = []

    def get_next_question(self) -> Card | None:
        if not self._queue:
            return None
        card = self._queue.popleft()
        self._in_review = [card]
        return card

    def record_result(self, card: Card, is_correct: bool) -> None:
        if not self._in_review or self._in_review[0] != card:
            return

        if not is_correct:
            # Reinsert a missed card near the front so it's seen again soon.
            self._queue.appendleft(card)

        self._in_review.clear()


class QuizModeFactory:
    """Factory for constructing quiz mode strategy instances."""

    _MODES: dict[str, type[QuizMode]] = {
        "sequential": SequentialMode,
        "random": RandomMode,
        "adaptive": AdaptiveMode,
    }

    @classmethod
    def create_mode(cls, mode_name: str, cards: Iterable[Card]) -> QuizMode:
        mode_key = mode_name.strip().lower()
        mode_class = cls._MODES.get(mode_key)
        if mode_class is None:
            valid_modes = ", ".join(sorted(cls._MODES))
            raise ValueError(f"Unknown mode '{mode_name}'. Valid modes: {valid_modes}.")
        return mode_class(cards)
