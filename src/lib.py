from typing import Protocol


class Dimensions(Protocol):
    """Structural type of terminal dimensions."""

    columns: int
    lines: int
