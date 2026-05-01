# FlashCardQuizzer

Simple flashcard loader with JSON validation.

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

## Error Handling

If a file is missing, malformed JSON, or any card is missing a valid `front`/`back` value,
the application prints a friendly error message instead of a raw Python traceback.

## Run

```bash
python main.py
```


## Quiz Modes (Strategy Pattern)

The quiz engine exposes a `QuizMode` abstract base class with three concrete strategies:

- `SequentialMode`: serves cards in original order.
- `RandomMode`: shuffles once and serves cards in randomized order.
- `AdaptiveMode`: re-prioritizes missed cards by re-queuing them near the front.

Use `QuizModeFactory.create_mode(mode_name, cards)` to select a strategy (`sequential`, `random`, or `adaptive`) based on user input.
