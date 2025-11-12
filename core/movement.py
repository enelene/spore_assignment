# core/movement.py

"""
Implements the Strategy Design Pattern for creature movement.

This allows movement behaviors (e.g., Crawl, Run, Fly) to be
swapped at runtime and new behaviors to be added without
modifying the Creature class (Open-Closed Principle).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from core import config

# Use TYPE_CHECKING to avoid circular imports at runtime
if TYPE_CHECKING:
    from core.creature import Creature


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
        if creature.current_stamina >= config.CRAWL_STAMINA_COST:
            creature.current_stamina -= config.CRAWL_STAMINA_COST
            return config.CRAWL_SPEED
        return 0


class HopMovement(MovementStrategy):
    """Concrete strategy for hopping."""

    def move(self, creature: "Creature") -> int:
        if (
            creature.max_stamina >= config.HOP_MIN_STAMINA
            and creature.current_stamina >= config.HOP_STAMINA_COST
        ):
            creature.current_stamina -= config.HOP_STAMINA_COST
            return config.HOP_SPEED
        return 0


class WalkMovement(MovementStrategy):
    """Concrete strategy for walking."""

    def move(self, creature: "Creature") -> int:
        if (
            creature.max_stamina >= config.WALK_MIN_STAMINA
            and creature.current_stamina >= config.WALK_STAMINA_COST
        ):
            creature.current_stamina -= config.WALK_STAMINA_COST
            return config.WALK_SPEED
        return 0


class RunMovement(MovementStrategy):
    """Concrete strategy for running."""

    def move(self, creature: "Creature") -> int:
        if (
            creature.max_stamina >= config.RUN_MIN_STAMINA
            and creature.current_stamina >= config.RUN_STAMINA_COST
        ):
            creature.current_stamina -= config.RUN_STAMINA_COST
            return config.RUN_SPEED
        return 0


class FlyMovement(MovementStrategy):
    """Concrete strategy for flying."""

    def move(self, creature: "Creature") -> int:
        if (
            creature.max_stamina >= config.FLY_MIN_STAMINA
            and creature.current_stamina >= config.FLY_STAMINA_COST
        ):
            creature.current_stamina -= config.FLY_STAMINA_COST
            return config.FLY_SPEED
        return 0
