# AI Edit Log

**Instructions:** Use this document to track all your interactions with AI assistants during the project. This log will help you reflect on your AI collaboration process and demonstrate your learning journey.

## How to Use This Log

For each AI interaction, create a new entry with the following structure:

### Entry Template
```markdown
## [Date] - [Brief Description]

**Context:** What were you trying to accomplish?
**AI Tool Used:** Claude/ChatGPT/Copilot/etc.
**Prompt/Request:** What exactly did you ask the AI?
**AI Response:** Summary of what the AI generated (don't copy entire code blocks)
**Changes Made:** What modifications did you make to the AI's suggestions?
**Reasoning:** Why did you make those changes?
**Outcome:** What was the final result?
**Lessons Learned:** What did you learn from this interaction?
```

---

## Example Entry

### 2024-01-15 - Initial Task Manager Implementation

**Context:** I needed to create a basic task management system to demonstrate CRUD operations and serve as the foundation for the project.

**AI Tool Used:** Claude

**Prompt/Request:** "Help me create a Python class for managing tasks with basic CRUD operations. The class should handle task creation, retrieval, completion, and deletion. Include proper error handling and type hints."

**AI Response:** Claude generated a TaskManager class with methods for add_task, get_task, get_all_tasks, complete_task, delete_task, and to_dict. The code included type hints, proper error handling with ValueError for missing tasks, and used datetime for timestamps.

**Changes Made:** 
- Added priority field to tasks with a default value of "medium"
- Modified the task structure to include created_at timestamp
- Added validation for priority values
- Renamed some variable names for clarity

**Reasoning:** 
- Priority field will be useful for implementing sorting features later
- Timestamps help with task organization and analytics
- Input validation prevents invalid data from being stored
- Better variable names improve code readability

**Outcome:** Successfully created a robust TaskManager class that serves as the core of the application with room for future enhancements.

**Lessons Learned:** 
- AI provides good starting implementations but always needs customization
- It's important to think about future requirements when reviewing AI code
- Type hints and error handling are crucial for maintainable code

---

# Your Log Entries

## 2026-05-01 - Initial Project Structure Setup

**Context:** I needed to create the basic folder and file structure for the flashcard quiz project before implementing any logic.

**AI Tool Used:** Claude

**Prompt/Request:** I asked the AI to create the following project structure: `main.py`, `data/`, `utils/`, `tests/`, `docs/`, and configuration files for the AI tools.

**AI Response:** The AI suggested a clear project layout and created placeholder files. It also recommended adding a `README.md` and a `.gitignore`, even though those were not explicitly requested.

**Changes Made:** 
- Kept the suggested `README.md` because it helped document how to run the project.
- Added `__init__.py` files inside `utils/` and `tests/` to make imports easier during testing.
- Moved the AI interaction log template into `docs/ai_edit_log.md`.
- Removed an extra configuration folder that was not needed for the project.

**Reasoning:** 
- The original prompt focused only on structure, but the generated project needed to be import-friendly for pytest.
- The extra configuration folder added unnecessary complexity at this stage.
- Keeping the documentation in `docs/` made the project easier to navigate.

**Outcome:** The project started with a clean structure that supported future implementation, testing, and documentation.

**Lessons Learned:** 
- AI can create a useful starting structure, but the developer still needs to decide what belongs in the MVP.
- Small project organization choices can affect testing and imports later.
- It is useful to ask AI for structure, but not every suggested file or folder needs to be accepted.

---

## 2026-05-01 - Data Loader and JSON Validation

**Context:** I needed to implement the data loading layer for flashcards, supporting both a simple array format and a wrapper object format.

**AI Tool Used:** ChatGPT

**Prompt/Request:** I asked the AI to create a system that loads and validates flashcard data from JSON. The app needed to support both `[{"front": "...", "back": "..."}]` and `{"cards": [...]}` formats, and it needed to show friendly error messages for invalid files.

**AI Response:** The AI generated a `load_flashcards` function that opened the JSON file, parsed it, and returned a list of flashcards. It also included exception handling for malformed JSON and missing files.

**Changes Made:** 
- Adjusted the validation logic to check every card individually for both `front` and `back`.
- Replaced raw `KeyError` and `JSONDecodeError` messages with user-friendly messages.
- Added validation to reject empty strings for `front` or `back`.
- Made sure both supported JSON formats returned the same internal structure.
- Updated `sample_flashcards.json` to use the wrapper format with a `cards` key.

**Reasoning:** 
- The initial response handled malformed JSON but did not fully validate missing or empty fields.
- Returning the same internal structure from both input formats made the rest of the application simpler.
- Friendly error messages were important because the requirements specifically said not to show raw Python tracebacks.

**Outcome:** The app could load valid flashcards from both formats and reject invalid input with clear messages.

**Lessons Learned:** 
- Input validation needs to be more precise than just checking whether a file can be opened.
- AI often handles the most obvious errors first, but edge cases still require manual review.
- Normalizing different input formats early simplifies the rest of the program.

---

## 2026-05-01 - Quiz Engine with Strategy and Factory Patterns

**Context:** I needed to implement the core quiz logic using the Strategy Pattern and select quiz modes using a Factory Pattern.

**AI Tool Used:** Claude

**Prompt/Request:** I asked the AI to implement `SequentialMode`, `RandomMode`, and `AdaptiveMode`, all inheriting from an abstract `QuizMode` base class. I also asked it to use a factory to select the correct mode based on user input.

**AI Response:** The AI created an abstract base class and three concrete quiz mode classes. It also created a factory function that returned the correct class based on a string such as `sequential`, `random`, or `adaptive`.

**Changes Made:** 
- Renamed some methods to make their purpose clearer, such as `get_next_card`.
- Modified `RandomMode` so that it shuffled a copy of the flashcards instead of modifying the original list.
- Adjusted `AdaptiveMode` because the first version repeated wrong cards too aggressively and could feel like an infinite loop.
- Added a small counter to track incorrect answers and prioritize weaker cards without completely ignoring new cards.
- Made the factory raise a clear `ValueError` for unsupported modes.

**Reasoning:** 
- Mutating the original flashcard list made tests less predictable.
- Adaptive mode needed to balance review and progression; otherwise, a single wrong answer could dominate the whole session.
- Clear factory errors made the CLI easier to debug and test.

**Outcome:** The quiz engine supported three different strategies while keeping the mode-selection logic centralized.

**Lessons Learned:** 
- Design patterns are useful when they reduce complexity, but the implementation still needs to match the real user experience.
- Adaptive behavior requires careful rules, otherwise it can become frustrating.
- Keeping randomness isolated improves testability.

---

## 2026-05-01 - CLI Interaction and Graceful Exit

**Context:** I needed to build the command-line interface so users could run the quiz from the terminal with flags for file path, mode, and stats.

**AI Tool Used:** ChatGPT

**Prompt/Request:** I asked the AI to build a CLI using `argparse`, support flags like `-f`, `-m`, and `--stats`, display green text for correct answers and red text for incorrect answers, and allow the user to type `exit` or press Ctrl+C to quit gracefully.

**AI Response:** The AI generated a basic `argparse` setup and a quiz loop that asked questions one by one. It added colored output using ANSI escape codes and caught `KeyboardInterrupt`.

**Changes Made:** 
- Added default values for `-f` and `-m` so the app could run with minimal arguments.
- Replaced hardcoded ANSI codes with a small helper function to keep the display logic cleaner.
- Added explicit handling for the user typing `exit`, `quit`, or an empty response.
- Modified the Ctrl+C handler so it prints a short goodbye message instead of showing an exception.
- Ensured `--stats` could display session results without starting a new quiz.

**Reasoning:** 
- The first version worked, but it was not friendly enough for a user testing the game manually.
- Separating color formatting into a helper function made the CLI easier to maintain.
- Graceful exits were part of the requirements and needed to work for both typed commands and keyboard interruption.

**Outcome:** The CLI became usable for manual testing and supported the required flags and exit behavior.

**Lessons Learned:** 
- Terminal apps need small usability details to feel polished.
- Graceful error and exit handling matters even in small projects.
- Requirements like `--stats` should be clarified in behavior, not only added as a flag.

---

## 2026-05-01 - Test Suite and Coverage Improvements

**Context:** I needed to create pytest tests for the data loader, quiz modes, and one integration flow, with the goal of reaching more than 80% code coverage.

**AI Tool Used:** Claude

**Prompt/Request:** I asked the AI to create a test suite with `test_flashcard_loader.py`, `test_quiz_modes.py`, and `test_integration.py`, including tests for valid flashcards, invalid JSON, missing fields, quiz mode factory behavior, adaptive mode behavior, and a full quiz session.

**AI Response:** The AI generated several pytest tests using temporary files and simple sample flashcards. It also suggested using `pytest --cov=.` to check coverage.

**Changes Made:** 
- Fixed import paths so tests worked from the project root.
- Changed the invalid JSON test to check for a friendly error message instead of expecting a traceback.
- Added tests for both supported JSON input formats.
- Reworked the integration test to mock user input instead of requiring manual terminal interaction.
- Added a coverage configuration to exclude simple boilerplate files from the report.

**Reasoning:** 
- The first generated tests were useful but assumed a slightly different project structure.
- Integration tests should run automatically, so they cannot depend on real user typing.
- Testing both JSON formats was important because it was a core requirement from Phase 1.
- Coverage should measure meaningful application logic, not empty placeholder files.

**Outcome:** The test suite covered the main behavior of the app and reached above the required 80% coverage target.

**Lessons Learned:** 
- AI-generated tests often need adjustment because they may not match the actual folder structure.
- Mocking input is essential for testing CLI programs.
- Code coverage is useful, but it should be interpreted together with test quality.

---

## 2026-05-01- Python Basics Flashcard Dataset

**Context:** I needed to create a real sample flashcard file with at least 25 simple Python questions to serve as a Definition of Done artifact.

**AI Tool Used:** ChatGPT

**Prompt/Request:** I asked the AI to create `data/python_basics.json` with at least 25 simple Python flashcards using short answers.

**AI Response:** The AI generated a JSON file with beginner-level Python questions about variables, loops, functions, lists, dictionaries, imports, and exceptions.

**Changes Made:** 
- Rewrote some answers to make them shorter and easier to compare during a CLI quiz.
- Removed a few questions that were too broad, such as questions asking for long explanations.
- Changed some wording to avoid ambiguity, for example replacing "What is Python?" with more specific syntax questions.
- Confirmed that the JSON used the same structure expected by the loader.

**Reasoning:** 
- The quiz app works better when answers are short and objective.
- Broad questions make manual validation harder and may frustrate the player.
- The sample file was part of the Definition of Done, so it needed to be realistic and directly usable.

**Outcome:** The project had a practical `python_basics.json` file that could be used to play a complete test session.

**Lessons Learned:** 
- Test data is part of the product, not just a temporary artifact.
- Good sample data helps reveal usability issues in the application.
- For quiz apps, question design matters as much as technical implementation.

---

## 2026-05-01 - Renaming Fields from Question/Answer to Front/Back

**Context:** I needed to align the whole project with the required flashcard field names: `front` and `back`, instead of `question` and `answer`.

**AI Tool Used:** Claude

**Prompt/Request:** I asked the AI to adjust the structure so that the labels were `front` and `back`, not `question` and `answer`.

**AI Response:** The AI updated most of the data model and sample JSON files to use `front` and `back`. It also changed some loader logic and test data.

**Changes Made:** 
- Searched the codebase manually for remaining `question` and `answer` references.
- Updated test names and assertions to match `front` and `back`.
- Adjusted CLI display text so it still shows user-friendly wording while using `front` and `back` internally.
- Updated documentation comments to avoid mixing both naming conventions.
- Added one regression test to ensure cards with `question` and `answer` are rejected.

**Reasoning:** 
- The AI changed the main files but missed a few references in tests and comments.
- Mixing field names could create confusion and hidden bugs.
- Rejecting the old structure prevents the app from silently accepting inconsistent data.

**Outcome:** The project consistently used `front` and `back` across the loader, quiz engine, CLI, tests, and sample data.

**Lessons Learned:** 
- Renaming data fields across a project requires more than editing one file.
- Search tools and tests are important when making cross-cutting changes.
- Consistent terminology reduces bugs and improves maintainability.

---

## Summary Statistics

At the end of your project, fill out these statistics:

- **Total AI interactions:** 7
- **Lines of AI-generated code used:** Approximately 580
- **Lines of AI-generated code modified:** Approximately 165
- **Most helpful AI interaction:** Phase 2, because the Strategy Pattern and Factory Pattern gave the project a clean structure for adding quiz modes.
- **Most challenging AI interaction:** Phase 5, because the generated tests needed several adjustments to match the actual folder structure, CLI behavior, and coverage target.
- **Biggest lesson learned:** AI is very useful for generating first drafts, but the developer must still validate requirements, test edge cases, simplify the implementation, and keep the project consistent over time.

---

**Note:** This log is a required component of your final project report. Be thorough and honest in your documentation to demonstrate your learning process and AI collaboration skills.
