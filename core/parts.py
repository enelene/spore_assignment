# core/parts.py

"""
Defines the components (Body Parts) that a Creature can have.
This module uses Composition over Inheritance.
"""

from enum import Enum


class ClawSize(Enum):
    """Enumeration for claw size and its power multiplier."""

    SMALL = 2
    MEDIUM = 3
    BIG = 4


class TeethSharpness(Enum):
    """Enumeration for teeth sharpness and its power boost."""

    LOW = 3
    MEDIUM = 6
    HIGH = 9


class Legs:
    """Body part representing legs."""

    def __init__(self, count: int) -> None:
        self.count: int = max(0, count)

    def __repr__(self) -> str:
        return f"Legs(count={self.count})"


class Wings:
    """Body part representing wings."""

    def __init__(self, count: int) -> None:
        self.count: int = max(0, count)

    def __repr__(self) -> str:
        return f"Wings(count={self.count})"


class Claws:
    """Body part representing claws."""

    def __init__(self, size: ClawSize) -> None:
        self.size: ClawSize = size
        self.size_multiplier: int = size.value

    def __repr__(self) -> str:
        return f"Claws(size={self.size.name})"


class Teeth:
    """Body part representing teeth."""

    def __init__(self, sharpness: TeethSharpness) -> None:
        self.sharpness: TeethSharpness = sharpness
        self.sharpness_boost: int = sharpness.value

    def __repr__(self) -> str:
        return f"Teeth(sharpness={self.sharpness.name})"


# Union type for all possible parts
BodyPart = Legs | Wings | Claws | Teeth
