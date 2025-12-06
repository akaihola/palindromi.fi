"""Utilities for YAML file handling with proper formatting of short and long text values."""

from io import StringIO
from typing import Any, Union

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString, preserve_literal


def maybe_preserve_literal(text: str) -> Union[str, LiteralScalarString]:
    """Use a multi-line YAML literal if the text contains a newline or is too long.

    Short text values (≤50 characters with no newlines) are stored inline on the same line.
    Longer text or multi-line text uses the `|-` YAML block literal format.

    :param text: The text to check
    :return: The text, possibly wrapped in a YAML literal scalar

    """
    if "\n" in text or len(text) > 50:
        return preserve_literal(text)
    return text


def create_yaml_dumper() -> YAML:
    """Create a YAML dumper configured with standard settings.

    Configuration:
    - Line width: 88 characters (matching Black formatter width)
    - Preserves literal scalars for long/multi-line text

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
