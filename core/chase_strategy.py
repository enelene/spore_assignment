# core/chase_strategy.py


from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.creature import Creature


from core import config, movement
from core.movement import MovementStrategy


class MovementDecisionStrategy(ABC):
    """
    Abstract base class for deciding which movement strategy to use.
    This allows different decision-making approaches (greedy, conservative, etc.)
    """

    @abstractmethod
    def decide_movement(self, creature: "Creature") -> "MovementStrategy":
        pass


class GreedyDecision(MovementDecisionStrategy):
    """
    Greedy strategy: Always choose the fastest movement available.
    This checks movements in order from fastest to slowest and picks
    the first one the creature can afford (has required stamina and parts).
    """

    def decide_movement(self, creature: "Creature") -> "MovementStrategy":
        """Choose the fastest available movement."""
        num_legs = creature._num_legs
        num_wings = creature._num_wings
        current_stamina = creature.current_stamina
        max_stamina = creature.max_stamina

        # Check from fastest to slowest
        # Fly is the fastest (speed 8)
        if (
            num_wings >= 2
            and max_stamina >= config.FLY_MIN_STAMINA
            and current_stamina >= config.FLY_STAMINA_COST
        ):
            return movement.FlyMovement()

        # Run is second fastest (speed 6)
        if (
            num_legs >= 2
            and max_stamina >= config.RUN_MIN_STAMINA
            and current_stamina >= config.RUN_STAMINA_COST
        ):
            return movement.RunMovement()

        # Walk is third (speed 4)
        if (
            num_legs >= 2
            and max_stamina >= config.WALK_MIN_STAMINA
            and current_stamina >= config.WALK_STAMINA_COST
        ):
            return movement.WalkMovement()

        # Hop is fourth (speed 3)
        if (
            num_legs >= 1
            and max_stamina >= config.HOP_MIN_STAMINA
            and current_stamina >= config.HOP_STAMINA_COST
        ):
            return movement.HopMovement()

        # Fall back to crawl (speed 1, always available if stamina > 0)
        return movement.CrawlMovement()


class ConservativeDecision(MovementDecisionStrategy):
    """
    Conservative strategy: Choose movement that preserves stamina.
    Useful for prey that wants to run away for as long as possible,
    or predators that need to conserve energy for a long chase.
    Uses slower movements to make stamina last longer.
    """

    def decide_movement(self, creature: "Creature") -> "MovementStrategy":
        """Choose the most stamina-efficient movement."""
        num_legs = creature._num_legs
        num_wings = creature._num_wings
        current_stamina = creature.current_stamina
        max_stamina = creature.max_stamina

        # If low on stamina (< 30%), be very conservative
        if current_stamina < max_stamina * 0.3:
            # Try to use least stamina-expensive options
            if (
                num_legs >= 1
                and max_stamina >= config.HOP_MIN_STAMINA
                and current_stamina >= config.HOP_STAMINA_COST
            ):
                return movement.HopMovement()
            return movement.CrawlMovement()

        # If moderate stamina (30-70%), use moderate speed
        if current_stamina < max_stamina * 0.7:
            if (
                num_legs >= 2
                and max_stamina >= config.WALK_MIN_STAMINA
                and current_stamina >= config.WALK_STAMINA_COST
            ):
                return movement.WalkMovement()
            if (
                num_legs >= 1
                and max_stamina >= config.HOP_MIN_STAMINA
                and current_stamina >= config.HOP_STAMINA_COST
            ):
                return movement.HopMovement()
            return movement.CrawlMovement()

        # If high stamina (> 70%), can afford faster movements
        if (
            num_wings >= 2
            and max_stamina >= config.FLY_MIN_STAMINA
            and current_stamina >= config.FLY_STAMINA_COST
        ):
            return movement.FlyMovement()

        if (
            num_legs >= 2
            and max_stamina >= config.RUN_MIN_STAMINA
            and current_stamina >= config.RUN_STAMINA_COST
        ):
            return movement.RunMovement()

        if (
            num_legs >= 2
            and max_stamina >= config.WALK_MIN_STAMINA
            and current_stamina >= config.WALK_STAMINA_COST
        ):
            return movement.WalkMovement()

        return movement.CrawlMovement()


class AdaptiveDecision(MovementDecisionStrategy):
    """
    Adaptive strategy: Adjusts behavior based on role.
    - Predators: Start fast to close distance, then conserve
    - Prey: Balance speed and endurance to escape
    """

    def __init__(self, role: str = "prey") -> None:
        """
        Initialize with a role.
        Args:
            role: Either 'predator' or 'prey'
        """
        self.role = role

    def decide_movement(self, creature: "Creature") -> "MovementStrategy":
        """Choose movement based on role and stamina."""
        stamina_ratio = creature.current_stamina / creature.max_stamina

        if self.role == "predator":
            # Predators: aggressive early, then sustainable
            if stamina_ratio > 0.5:
                # High stamina: go fast
                return GreedyDecision().decide_movement(creature)
            else:
                # Low stamina: conserve but stay moving
                return ConservativeDecision().decide_movement(creature)
        else:  # prey
            # Prey: always try to maintain speed to escape
            if stamina_ratio > 0.3:
                # Enough stamina: go fast
                return GreedyDecision().decide_movement(creature)
            else:
                # Critical stamina: conserve
                return ConservativeDecision().decide_movement(creature)
