# spore/strategies.py

"""
Implements the Strategy Design Pattern for creature movement.

This allows movement behaviors (e.g., Crawl, Run, Fly) to be
swapped at runtime and new behaviors to be added without
modifying the Creature class (Open-Closed Principle).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

# Use TYPE_CHECKING to avoid circular imports at runtime
if TYPE_CHECKING:
    from spore.creature import Creature

# --- Movement Constants ---
CRAWL_MIN_STAMINA = 0
CRAWL_STAMINA_COST = 1
CRAWL_SPEED = 1

HOP_MIN_STAMINA = 20
HOP_STAMINA_COST = 2
HOP_SPEED = 3

WALK_MIN_STAMINA = 40
WALK_STAMINA_COST = 2
WALK_SPEED = 4

RUN_MIN_STAMINA = 60
RUN_STAMINA_COST = 4
RUN_SPEED = 6

FLY_MIN_STAMINA = 80
FLY_STAMINA_COST = 4
FLY_SPEED = 8


class MovementStrategy(ABC):
    """
    The abstract base class (interface) for all movement strategies.
    """

    @abstractmethod
    def move(self, creature: "Creature") -> int:
        """
        Attempts to move the creature based on this strategy.
        Modifies the creature's stamina in-place.
        Returns the distance moved (int).
        """
        pass


class CrawlMovement(MovementStrategy):
    """Concrete strategy for crawling."""

    def move(self, creature: "Creature") -> int:
        if creature.current_stamina >= CRAWL_STAMINA_COST:
            creature.current_stamina -= CRAWL_STAMINA_COST
            return CRAWL_SPEED
        return 0


class HopMovement(MovementStrategy):
    """Concrete strategy for hopping."""

    def move(self, creature: "Creature") -> int:
        if (
            creature.max_stamina >= HOP_MIN_STAMINA
            and creature.current_stamina >= HOP_STAMINA_COST
        ):
            creature.current_stamina -= HOP_STAMINA_COST
            return HOP_SPEED
        return 0


class WalkMovement(MovementStrategy):
    """Concrete strategy for walking."""

    def move(self, creature: "Creature") -> int:
        if (
            creature.max_stamina >= WALK_MIN_STAMINA
            and creature.current_stamina >= WALK_STAMINA_COST
        ):
            creature.current_stamina -= WALK_STAMINA_COST
            return WALK_SPEED
        return 0


class RunMovement(MovementStrategy):
    """Concrete strategy for running."""

    def move(self, creature: "Creature") -> int:
        if (
            creature.max_stamina >= RUN_MIN_STAMINA
            and creature.current_stamina >= RUN_STAMINA_COST
        ):
            creature.current_stamina -= RUN_STAMINA_COST
            return RUN_SPEED
        return 0


class FlyMovement(MovementStrategy):
    """Concrete strategy for flying."""

    def move(self, creature: "Creature") -> int:
        if (
            creature.max_stamina >= FLY_MIN_STAMINA
            and creature.current_stamina >= FLY_STAMINA_COST
        ):
            creature.current_stamina -= FLY_STAMINA_COST
            return FLY_SPEED
        return 0
