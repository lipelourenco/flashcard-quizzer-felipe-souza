# AI-Assisted Development Project Report

**Student Name:** Felipe Souza  
**Project Title:** FlashCardQuizzer CLI  
**Date:** May 1, 2026

## Executive Summary

This project delivers **FlashCardQuizzer**, a Python command-line application for studying with flashcards stored in JSON files. The app loads and validates flashcard datasets, runs interactive quiz sessions in multiple modes, and provides optional end-of-session statistics. The product is intentionally lightweight, but it applies structured software engineering practices including design patterns, input validation, and automated tests.

Core functionality includes robust data ingestion (with support for two JSON shapes), strategy-based quiz behavior (`sequential`, `random`, and `adaptive`), and user-friendly command-line interaction with graceful exit handling. Instead of surfacing raw exceptions, the project reports clearer domain-specific errors through a custom exception type, improving usability for non-technical users.

AI was used throughout development as a coding collaborator rather than an autopilot. The workflow combined AI-generated first drafts with manual review, refactoring, and targeted test updates. The interaction log shows repeated cycles of prompting, evaluating generated code against requirements, tightening edge-case handling, and improving consistency (especially around `front`/`back` naming and predictable behavior in tests).

## Project Overview

### Problem Statement

Students and developers often need a fast way to rehearse concepts using flashcards, but many simple scripts lack validation, predictable quiz behavior, and maintainable structure. The challenge was to build a small yet reliable CLI quiz app that can:

- Accept flexible input formats.
- Prevent malformed data from breaking runtime behavior.
- Support different quiz strategies for varied learning styles.
- Be testable and maintainable.

### Solution Approach

The solution was organized around small modules with clear responsibilities:

- `utils/file_handler.py` handles JSON loading, format normalization, and card validation.
- `utils/quiz_engine.py` contains quiz strategy implementations and a factory for mode selection.
- `main.py` focuses on CLI parsing and interaction flow.
- `tests/` covers loader logic, strategy behavior, and a complete session flow.

Key design decisions:

1. **Normalize input early:** both raw list and wrapped `{ "cards": [...] }` formats are converted to one internal representation.
2. **Use Strategy + Factory patterns:** mode behaviors are encapsulated and selected by a single factory interface.
3. **Favor explicit error messages:** users get clear, actionable data errors.
4. **Keep CLI state simple:** score tracking and exit behavior are explicit and easy to follow.

Technology stack:

- Python 3
- Standard library modules (`argparse`, `json`, `pathlib`, `abc`, `collections`, `random`)
- Pytest for automated testing

### Final Features

- [x] Load flashcards from JSON list format
- [x] Load flashcards from wrapper object format (`cards`)
- [x] Validate required `front`/`back` non-empty string fields
- [x] Interactive CLI quiz loop
- [x] Sequential mode
- [x] Random mode
- [x] Adaptive mode with missed-card reprioritization
- [x] Graceful exit (`exit` and Ctrl+C)
- [x] Optional end-session statistics (`--stats`)

## AI Collaboration Experience

### AI Tools Used

- [x] Claude
- [ ] GitHub Copilot
- [x] ChatGPT
- [ ] Other

### Collaboration Workflow

1. **Prompt structure:** prompts were requirement-driven (e.g., specific mode names, JSON schema rules, error behavior).
2. **AI task types:** scaffolding, first-pass implementations, test generation, and data file drafting.
3. **Validation process:** each AI suggestion was checked against acceptance criteria, manually reviewed, and re-tested with pytest.
4. **Refinement loop:** code was adjusted for naming consistency, usability, and predictable test behavior.

### Most Valuable AI Interactions

#### Example 1: Data Loader and JSON Validation
**Context:** Implement robust JSON loading with two supported formats.  
**AI Prompt:** Build a loader that accepts both list and wrapper formats and handles invalid files.  
**AI Response:** Provided initial loader with parsing and exception handling.  
**Your Changes:** Added strict per-card validation for `front`/`back`, non-empty checks, and clearer user-facing messages.  
**Outcome:** Reliable and consistent data pipeline used by the entire app.

#### Example 2: Strategy + Factory Quiz Engine
**Context:** Build three quiz modes with central mode selection.  
**AI Prompt:** Implement `SequentialMode`, `RandomMode`, `AdaptiveMode`, and a factory method.  
**AI Response:** Generated OOP structure and factory-based dispatch.  
**Your Changes:** Improved method naming, avoided mutating original card lists, and tuned adaptive behavior to avoid frustrating loops.  
**Outcome:** Clean extensible architecture with mode-specific logic isolated.

#### Example 3: CLI Interaction and Graceful Exit
**Context:** Provide a usable terminal flow with flags and friendly exits.  
**AI Prompt:** Add `argparse` flags, colored feedback, and Ctrl+C handling.  
**AI Response:** Generated baseline parser and quiz loop.  
**Your Changes:** Added defaults, explicit typed exit support, cleaner output handling, and ensured `--stats` behavior matched requirements.  
**Outcome:** Better user experience for manual runs and demos.

#### Example 4: Test Suite and Coverage
**Context:** Reach coverage target with loader, strategy, and integration tests.  
**AI Prompt:** Generate pytest modules for critical behavior.  
**AI Response:** Produced initial tests and coverage command suggestion.  
**Your Changes:** Fixed imports/assumptions, improved assertions for friendly errors, and added deterministic integration via input mocking.  
**Outcome:** A stable automated suite with passing tests and evidence of >80% coverage (from generated report artifact).

### Challenges with AI Collaboration

- AI sometimes assumed slightly different file/module names than the current repo layout.
- First drafts tended to handle “happy path + obvious exceptions,” requiring manual edge-case hardening.
- Generated behavior occasionally met technical requirements but not UX expectations (especially adaptive repetition).
- Strongest outcomes came from constrained prompts and explicit acceptance checks.

## Software Engineering Practices

### Code Quality Measures

- [ ] Code formatting (Black, isort)
- [ ] Linting (flake8, mypy)
- [x] Type hints
- [x] Documentation/comments (docstrings)
- [x] Error handling

### Testing Strategy

The test strategy combined:

- **Unit tests** for loader validation and strategy/factory behavior.
- **Integration test** for a complete quiz session using mocked user input.

Reliability was improved by testing both supported JSON formats, invalid payloads, mode selection, adaptive repetition behavior, and final stats output. While `pytest-cov` was unavailable in this environment during this update run, the existing coverage artifact (`pytest_coverage_report.html`) shows **83% total coverage**, satisfying the >80% target.

TDD was used partially: some tests were authored alongside implementations, while others were added after reviewing gaps.

### Design Patterns Used

- **Strategy Pattern:** `QuizMode` abstract class with `SequentialMode`, `RandomMode`, and `AdaptiveMode` implementations.
- **Factory Pattern:** `QuizModeFactory.create_mode(...)` centralizes runtime mode selection and validation.

### Code Structure and Organization

- **Separation of concerns:** input validation, quiz logic, and CLI orchestration are in separate modules.
- **Test organization:** tests are grouped by subsystem (`loader`, `modes`, `integration`).
- **Refactoring choices:** naming alignment to `front`/`back`, clearer exceptions, and reduced side effects in random mode.

## Technical Challenges and Solutions

### Challenge 1: Supporting Two JSON Input Shapes
**Problem:** Need to accept both list and wrapper formats without duplicating downstream logic.  
**Solution:** Normalize both formats to one validated internal list of cards.  
**AI Involvement:** AI drafted initial loader skeleton; manual refinement added strict validation and better errors.  
**Lessons Learned:** Data normalization at boundaries simplifies the rest of the codebase.

### Challenge 2: Adaptive Mode Balance
**Problem:** Repeating missed cards too aggressively can feel like a loop and reduce learning flow.  
**Solution:** Re-queue missed cards near the front (not as a separate hard loop) and keep queue behavior explicit.  
**AI Involvement:** AI provided initial adaptive implementation; behavior was tuned manually based on expected UX.  
**Lessons Learned:** Meeting a pattern requirement is not enough—behavioral quality matters for user satisfaction.

### Challenge 3: Testing Interactive CLI Logic
**Problem:** CLI code is inherently interactive, but CI tests must run unattended.  
**Solution:** Use `monkeypatch` for `input()` and capture output with `capsys` for deterministic assertions.  
**AI Involvement:** AI proposed starter test scaffolding; final version required manual adjustments.  
**Lessons Learned:** Mocking I/O is essential for robust CLI testing.

## Code Quality Analysis

### Metrics

- Lines of code (Python, non-empty): **283**
- Test coverage: **83%** (from existing HTML coverage artifact)
- Number of functions/classes: **23 functions**, **6 classes**
- Linting score: **Not measured in this repository state**

### Self-Assessment

- **Code Readability:** 4/5 — clear module boundaries, descriptive names, and docstrings.
- **Code Maintainability:** 4/5 — strategy/factory architecture enables feature growth.
- **Test Quality:** 4/5 — good core behavior coverage with one full-flow test; can be expanded for more edge cases.
- **Documentation:** 4/5 — README and docstrings explain usage and architecture; report and logs add process context.

## Learning Outcomes

### Technical Skills Developed

- Stronger JSON boundary validation and custom domain errors.
- Better understanding of Strategy/Factory trade-offs in small apps.
- Improved CLI testing with mocked inputs and output assertions.
- Cleaner modular decomposition in Python projects.

### AI Collaboration Skills

- Writing more constrained prompts improves first-pass quality.
- AI output requires systematic code review and test-driven verification.
- Best results come from using AI for acceleration, not authority.
- Keeping a detailed interaction log makes retrospective analysis easier.

### Software Engineering Insights

- Good architecture is valuable even in small CLI projects.
- Testing should include both component behavior and user flow.
- Data contract consistency (`front`/`back`) prevents many downstream bugs.
- Documentation is part of deliverable quality, not an afterthought.

## Reflection

### What Worked Well

- Clear modularization and early pattern decisions reduced complexity.
- Frequent AI-assisted iteration accelerated development.
- Automated tests caught regressions while changing field naming and quiz behavior.
- Friendly errors and graceful exits improved practical usability.

### What Could Be Improved

- Add lint/type-check automation in CI (ruff/flake8/mypy).
- Increase negative-path integration tests (e.g., bad file inputs through CLI entrypoint).
- Improve adaptive algorithm sophistication (e.g., spaced repetition heuristics).
- Strengthen dataset-level validation (duplicate fronts, overly long answers warnings).

### Future Enhancements

- Persistent session history and progress tracking.
- Timed mode and streak-based scoring.
- Near-match answer checking (case/typo tolerance with configurable strictness).
- Exportable statistics and study analytics.

## Conclusion

This project demonstrates that AI-assisted development works best as a structured collaboration model: AI accelerates scaffolding and ideation, while the developer remains responsible for correctness, UX quality, and maintainability. The final CLI application satisfies core requirements, applies formal design patterns, and is supported by an automated test suite and documentation.

Going forward, the most durable practices from this work are: modular architecture, explicit data validation, test-first thinking for risky paths, and disciplined review of AI-generated code. These habits will remain central in future development projects, whether AI is involved or not.

## Appendices

### Appendix A: AI Interaction Log

See `docs/ai_edit_log.md` for detailed chronological entries. Key entries include loader validation, strategy/factory implementation, CLI handling, test suite growth, and naming standardization.

### Appendix B: Code Statistics

- Existing coverage artifact indicates **83%** total coverage (`pytest_coverage_report.html`).
- Current local test run: **6 tests passed**.
- Python code metrics computed from repository source files: **283 non-empty LOC**, **23 functions**, **6 classes**.

### Appendix C: Additional Resources

- Python standard library docs (`argparse`, `json`, `pathlib`, `abc`)
- Pytest docs (`monkeypatch`, `capsys`)
- Coverage.py docs for interpreting HTML reports
