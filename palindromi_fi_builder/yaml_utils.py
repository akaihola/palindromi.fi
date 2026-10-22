"""Utilities for YAML file handling with proper formatting of short and long text values."""

from io import StringIO
from typing import Any, Union

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString, preserve_literal


def maybe_preserve_literal(text: str) -> Union[str, LiteralScalarString]:
    """Use a multi-line YAML literal if the text contains a newline or is too long.

    Values of at most 50 characters without LF newlines are returned unchanged,
    including any existing scalar style. Other values use a literal scalar;
    ruamel's helper normalizes CRLF/CR to LF. Trailing newlines determine chomping
    (|- without one, | with one, |+ with additional trailing newlines).

    :param text: The text to check
    :return: Unchanged text, or a literal scalar with normalized line endings

    """
    if "\n" in text or len(text) > 50:
        return preserve_literal(text)
    return text


def create_yaml_dumper() -> YAML:
    """Create a YAML dumper configured with standard settings.

    Configuration:
    - Preferred line width: 88 characters (not a limit for literal blocks)
    - Round-trip YAML retains existing literal/folded scalar wrappers

    Call maybe_preserve_literal() explicitly to convert text fields to literals;
    this factory does not choose styles based on text length or newlines.

    :return: A configured YAML instance

    """
    yaml = YAML()
    yaml.width = 88  # type: ignore[assignment]
    return yaml


def yaml_dump(data: Any) -> str:  # type: ignore[misc]
    """Dump data as YAML with standard configuration and return as string.

    :param data: The data to dump
    :return: The YAML string

    """
    yaml = create_yaml_dumper()
    buffer = StringIO()
    yaml.dump(data, buffer)  # type: ignore[misc]
    return buffer.getvalue()
