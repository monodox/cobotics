from cobotics.core.intent import IntentKind, parse


def test_parse_empty():
    assert parse("   ").kind is IntentKind.EMPTY


def test_parse_command():
    intent = parse("/move 3 4")
    assert intent.kind is IntentKind.COMMAND
    assert intent.command == "move"
    assert intent.args == ["3", "4"]


def test_parse_command_case_insensitive():
    assert parse("/HELP").command == "help"


def test_parse_chat():
    intent = parse("move the arm to the left")
    assert intent.kind is IntentKind.CHAT
    assert intent.text == "move the arm to the left"


def test_parse_quoted_args():
    intent = parse('/grip "close"')
    assert intent.args == ["close"]
