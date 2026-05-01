# FlashCardQuizzer

FlashCardQuizzer is a Python CLI application for practicing flashcards from JSON files. It focuses on reliable data validation, multiple quiz strategies, and a smooth terminal experience.

## Current Project Status (May 1, 2026)

- ✅ Core quiz flow implemented and stable.
- ✅ Supports `sequential`, `random`, and `adaptive` quiz modes.
- ✅ JSON validation for both supported flashcard formats.
- ✅ Friendly domain-specific errors (`FlashcardDataError`) for invalid input files.
- ✅ Automated test suite passing (`6 passed`).
- ✅ Coverage artifact available in `pytest_coverage_report.html` (83% total at generation time).

## Features

- Load flashcards from JSON.
- Validate `front`/`back` required fields.
- Run quizzes interactively in the terminal.
- Show color-coded feedback for correct/incorrect answers.
- Gracefully exit with `exit` or `Ctrl+C`.
- Optionally show session statistics using `--stats`.

## Supported Flashcard JSON Formats

`utils/file_handler.py` supports both:

1. **Array format**

```json
[
  {"front": "Question 1", "back": "Answer 1"},
  {"front": "Question 2", "back": "Answer 2"}
]
```

2. **Object wrapper format**

```json
{
  "cards": [
    {"front": "Question 1", "back": "Answer 1"},
    {"front": "Question 2", "back": "Answer 2"}
  ]
}
```

## Quiz Modes (Strategy Pattern)

The quiz engine uses a `QuizMode` abstract class with three concrete strategies:

- `SequentialMode`: serves cards in original order.
- `RandomMode`: shuffles a copy of the cards and serves once.
- `AdaptiveMode`: re-queues missed cards near the front for quicker review.

Mode instances are selected via `QuizModeFactory.create_mode(mode_name, cards)`.

## New: Architecture & Flow Explanation

This section explains how the application is organized and why.

### 1) Data Boundary Layer (`utils/file_handler.py`)

- Reads JSON from disk.
- Accepts two input structures and normalizes them into one internal list.
- Validates each card strictly:
  - card must be an object
  - `front` must be a non-empty string
  - `back` must be a non-empty string
- Raises `FlashcardDataError` with user-friendly messages.

**Why this matters:** by enforcing data quality early, the quiz engine can stay simple and avoid repetitive defensive checks.

### 2) Quiz Engine Layer (`utils/quiz_engine.py`)

- Contains mode behavior only (no CLI concerns).
- `QuizMode` defines the common interface:
  - `get_next_question()`
  - `record_result(card, is_correct)`
- Each mode encapsulates its own sequencing strategy.

**Why this matters:** adding a future mode (e.g., timed mode) only requires a new strategy class plus one factory mapping entry.

### 3) CLI Layer (`main.py`)

- Parses command-line arguments with `argparse`.
- Loads cards and mode.
- Runs interaction loop and checks answers.
- Handles `KeyboardInterrupt` and typed exit.
- Prints stats when `--stats` is enabled.

**Why this matters:** user interaction remains isolated, so core logic can be tested independently.

## Error Handling

If a file is missing, malformed, or contains invalid cards, the app prints a clear message instead of a raw traceback.

## Run

```bash
python main.py
```

Common options:

```bash
python main.py -f data/python_basics.json -m random --stats
```

## Tests

Run all tests:

```bash
pytest -q
```

## Project Structure

```text
.
├── main.py
├── data/
│   ├── sample_flashcards.json
│   └── python_basics.json
├── utils/
│   ├── file_handler.py
│   └── quiz_engine.py
├── tests/
│   ├── test_flashcard_loader.py
│   ├── test_quiz_modes.py
│   └── test_integration.py
└── docs/
    ├── ai_edit_log.md
    └── report_template.md
```
