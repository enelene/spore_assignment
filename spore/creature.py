# spore/creature.py

"""
Defines the Creature class.

This class holds the creature's state (health, stamina, parts)
and delegates actions like 'move' to its current MovementStrategy.
"""

from __future__ import annotations
import logging
from spore import parts
from spore import strategies

LOGGER = logging.getLogger(__name__)


class Creature:
    """
    Represents a single creature in the simulation.
    """

    def __init__(
        self,
        position: int,
        max_health: int,
        max_stamina: int,
        base_power: int,
    ) -> None:
        self.position: int = position
        self.max_health: int = max_health
        self.current_health: int = max_health
        self.max_stamina: int = max_stamina
        self.current_stamina: int = max_stamina
        self.base_power: int = base_power

        self.parts: list[parts.BodyPart] = []

        self.movement_strategy: strategies.MovementStrategy = (
            strategies.CrawlMovement()  # Default
        )

    @property
    def is_alive(self) -> bool:
        """Returns True if the creature has health > 0."""
        return self.current_health > 0

    @property
    def has_stamina(self) -> bool:
        """Returns True if the creature has stamina > 0."""
        return self.current_stamina > 0

    @property
    def _num_legs(self) -> int:
        """Helper to count legs."""
        return sum(part.count for part in self.parts if isinstance(part, parts.Legs))

    @property
    def _num_wings(self) -> int:
        """Helper to count wings."""
        return sum(part.count for part in self.parts if isinstance(part, parts.Wings))

    def log_characteristics(self) -> None:
        """Logs the creature's evolved stats and parts."""
        LOGGER.info(f"  Health: {self.max_health}, Stamina: {self.max_stamina}")
        LOGGER.info(f"  Power: {self.base_power}, Parts: {self.parts}")

    def update_movement_strategy(self) -> None:
        """
        Selects the best available movement strategy based on parts and stats.
        This implements the "greedy" approach.
        """
        num_legs = self._num_legs
        num_wings = self._num_wings

        if (
            num_wings >= 2
            and self.max_stamina >= strategies.FLY_MIN_STAMINA
            and self.current_stamina >= strategies.FLY_STAMINA_COST 
        ):
            self.movement_strategy = strategies.FlyMovement()
        elif (
            num_legs >= 2
            and self.max_stamina >= strategies.RUN_MIN_STAMINA
            and self.current_stamina >= strategies.RUN_STAMINA_COST
        ):
            self.movement_strategy = strategies.RunMovement()
        elif (
            num_legs >= 2
            and self.max_stamina >= strategies.WALK_MIN_STAMINA
            and self.current_stamina >= strategies.WALK_STAMINA_COST 
        ):
            self.movement_strategy = strategies.WalkMovement()
        elif (
            num_legs >= 1
            and self.max_stamina >= strategies.HOP_MIN_STAMINA
            and self.current_stamina >= strategies.HOP_STAMINA_COST 
        ):
            self.movement_strategy = strategies.HopMovement()
        else:
            # Default to crawl, which will run as long as current_stamina >= 1
            self.movement_strategy = strategies.CrawlMovement()

    def move(self) -> int:
        """
        Moves the creature by delegating to its current movement strategy.
        Returns the distance moved.
        """
        # Re-evaluate strategy every turn (greedy)
        self.update_movement_strategy()
        
        distance_moved = self.movement_strategy.move(self)
        self.position += distance_moved
        return distance_moved

    def attack(self, target: "Creature") -> None:
        """Calculates and applies damage to a target creature."""
        total_damage = self.base_power
        claw_multiplier = 1
        teeth_boost = 0

        # Apply damage modifiers from parts
        for part in self.parts:
            if isinstance(part, parts.Claws):
                # If creature has multiple claws, use the best one
                claw_multiplier = max(claw_multiplier, part.size_multiplier)
            elif isinstance(part, parts.Teeth):
                # If creature has multiple teeth, use the sharpest
                teeth_boost = max(teeth_boost, part.sharpness_boost)

        # Final damage calculation: (Base + Boost) * Multiplier
        total_damage = (total_damage + teeth_boost) * claw_multiplier

        LOGGER.debug(f"Attacked for {total_damage} damage.")
        target.current_health -= total_damage