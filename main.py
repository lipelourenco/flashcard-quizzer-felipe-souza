"""CLI entry point for running interactive flashcard quizzes."""

from __future__ import annotations

import argparse
from pathlib import Path

from utils.quiz_engine import QuizModeFactory
from utils.file_handler import FlashcardDataError, load_flashcards

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for quiz execution."""
    parser = argparse.ArgumentParser(description="Run an interactive flashcard quiz.")
    parser.add_argument(
        "-f",
        "--file",
        default="data/sample_flashcards.json",
        help="Path to flashcards JSON file (default: data/sample_flashcards.json).",
    )
    parser.add_argument(
        "-m",
        "--mode",
        default="sequential",
        choices=("sequential", "random", "adaptive"),
        help="Quiz mode to use (default: sequential).",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Print final quiz statistics when session ends.",
    )
    return parser.parse_args()


def run_quiz(file_path: Path, mode_name: str, show_stats: bool) -> None:
    """Run an interactive quiz session."""
    cards = load_flashcards(file_path)
    mode = QuizModeFactory.create_mode(mode_name, cards)

    total_answered = 0
    correct_answers = 0

    print(f"Loaded {len(cards)} flashcards. Mode: {mode_name}.")
    print("Type your answer, type 'exit', or press Ctrl+C to quit.\n")

    try:
        while True:
            card = mode.get_next_question()
            if card is None:
                print("\nNo more questions in this session.")
                break

            print(f"Q: {card['front']}")
            user_answer = input("> ").strip()

            if user_answer.lower() == "exit":
                print("\nExiting quiz session.")
                break

            is_correct = user_answer.lower() == card["back"].strip().lower()
            mode.record_result(card, is_correct)

            total_answered += 1
            if is_correct:
                correct_answers += 1
                print(f"{GREEN}Correct!{RESET}\n")
            else:
                print(f"{RED}Incorrect.{RESET} Answer: {card['back']}\n")
    except KeyboardInterrupt:
        print("\n\nQuiz interrupted. Goodbye!")

    if show_stats:
        accuracy = (correct_answers / total_answered * 100) if total_answered else 0.0
        print("\nStats")
        print(f"- Answered: {total_answered}")
        print(f"- Correct: {correct_answers}")
        print(f"- Accuracy: {accuracy:.1f}%")


def main() -> None:
    args = parse_args()

    try:
        run_quiz(Path(args.file), args.mode, args.stats)
    except FlashcardDataError as error:
        print(f"Could not load flashcards: {error}")


if __name__ == "__main__":
    main()
