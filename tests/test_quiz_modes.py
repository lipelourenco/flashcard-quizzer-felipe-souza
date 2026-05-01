from quiz_modes import AdaptiveMode, QuizModeFactory, RandomMode, SequentialMode


def test_quiz_mode_factory():
    cards = [{"front": "Q1", "back": "A1"}]

    assert isinstance(QuizModeFactory.create_mode("sequential", cards), SequentialMode)
    assert isinstance(QuizModeFactory.create_mode("random", cards), RandomMode)
    assert isinstance(QuizModeFactory.create_mode("adaptive", cards), AdaptiveMode)


def test_adaptive_mode_behavior():
    cards = [
        {"front": "Q1", "back": "A1"},
        {"front": "Q2", "back": "A2"},
    ]
    mode = AdaptiveMode(cards)

    first = mode.get_next_question()
    assert first == cards[0]

    mode.record_result(first, is_correct=False)

    repeated = mode.get_next_question()
    assert repeated == cards[0]

    mode.record_result(repeated, is_correct=True)

    next_card = mode.get_next_question()
    assert next_card == cards[1]
