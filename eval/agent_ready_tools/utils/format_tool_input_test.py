import enum
import json

import pytest

from agent_ready_tools.utils import format_tool_input


def test_string_to_list_of_strings() -> None:
    """Verifies that the `string_to_list_of_strings` functions."""
    assert format_tool_input.string_to_list_of_strings("foo") == ["foo"]
    assert format_tool_input.string_to_list_of_strings("['foo', 'bar']") == ["foo", "bar"]

    with pytest.raises(json.JSONDecodeError):
        format_tool_input.string_to_list_of_strings("['foo'], ['bar']")

    assert format_tool_input.string_to_list_of_strings("[foo") == ["[foo"]


def test_string_to_list_of_enums() -> None:
    """Verifies that the `string_to_list_of_enums` functions."""

    class MyClass(enum.Enum):
        """Test Enum."""

        FOO = 1
        BAR = 2

    assert format_tool_input.string_to_list_of_enums(
        "FOO",
        MyClass,
    ) == [MyClass.FOO]

    assert format_tool_input.string_to_list_of_enums(
        "['FOO', 'BAR']",
        MyClass,
    ) == [MyClass.FOO, MyClass.BAR]

    with pytest.raises(KeyError):
        format_tool_input.string_to_list_of_enums(
            "['FOO', 'BAR', 'BAZ']",
            MyClass,
        )


def test_string_to_list_of_ints() -> None:
    """Verifies that the `string_to_list_of_ints` function behaves as expected."""
    assert format_tool_input.string_to_list_of_ints([123, 456]) == [123, 456]
    assert format_tool_input.string_to_list_of_ints("123") == [123]
    assert format_tool_input.string_to_list_of_ints("123,456") == [123, 456]
    assert format_tool_input.string_to_list_of_ints("[123, 456]") == [123, 456]
