# core/creature.py

"""
Defines the Creature class.
This class holds the creature's state (health, stamina, parts)
and delegates actions like 'move' to its current MovementStrategy
and decision-making to a MovementDecisionStrategy.
"""

from __future__ import annotations

import logging

from core import chase_strategy, parts
from core import movement as strategies

LOGGER = logging.getLogger(__name__)


class Creature:
    """
    Represents a single creature in the simulation.
    Uses two strategy patterns:
    1. MovementStrategy: HOW to move (crawl, run, fly, etc.)
    2. MovementDecisionStrategy: WHICH movement to choose
    This separation allows independent modification of movement
    execution and movement selection logic.
    """

    def __init__(
        self,
        position: int,
        max_health: int,
        max_stamina: int,
        base_power: int,
        decision_strategy: chase_strategy.MovementDecisionStrategy | None = None,
    ) -> None:
        """
        Initialize a creature.
        Args:
            position: Starting position on the world ray
            max_health: Maximum health points
            max_stamina: Maximum stamina points
            base_power: Base attack power
            decision_strategy: Strategy for deciding which movement to use
                             (defaults to GreedyDecision)
        """
        self.position: int = position
        self.max_health: int = max_health
        self.current_health: int = max_health
        self.max_stamina: int = max_stamina
        self.current_stamina: int = max_stamina
        self.base_power: int = base_power

        self.parts: list[parts.BodyPart] = []

        # Strategy for HOW to move (will be set by decision strategy)
        self.movement_strategy: strategies.MovementStrategy = strategies.CrawlMovement()

        # Strategy for WHICH movement to choose
        self.decision_strategy: chase_strategy.MovementDecisionStrategy = (
            decision_strategy or chase_strategy.GreedyDecision()
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
        """Helper to count total legs from all Legs parts."""
        return sum(part.count for part in self.parts if isinstance(part, parts.Legs))

    @property
    def _num_wings(self) -> int:
        """Helper to count total wings from all Wings parts."""
        return sum(part.count for part in self.parts if isinstance(part, parts.Wings))

    def log_characteristics(self) -> None:
        """Logs the creature's evolved stats and parts."""
        LOGGER.info(f"  Health: {self.max_health}, Stamina: {self.max_stamina}")
        LOGGER.info(f"  Power: {self.base_power}, Parts: {self.parts}")

    def set_decision_strategy(
        self, strategy: chase_strategy.MovementDecisionStrategy
    ) -> None:
        """
        Change the decision-making strategy at runtime.
        This allows you to switch between greedy, conservative, adaptive,
        or any custom decision strategy during the simulation.
        Args:
            strategy: The new MovementDecisionStrategy to use
        """
        self.decision_strategy = strategy

    def move(self) -> int:
        """
        Moves the creature by delegating to its decision and movement strategies.
        Flow:
        1. Decision strategy chooses which movement to use
        2. Movement strategy executes the movement
        3. Position is updated
        Returns:
            The distance moved (int)
        """
        # Use the decision strategy to pick the best movement
        self.movement_strategy = self.decision_strategy.decide_movement(self)

        # Execute the chosen movement
        distance_moved = self.movement_strategy.move(self)
        self.position += distance_moved
        return distance_moved

    def attack(self, target: "Creature") -> None:
        """
        Calculates and applies damage to a target creature.
        Damage calculation:
        1. Start with base power
        2. Find the best claw multiplier (if creature has claws)
        3. Find the best teeth boost (if creature has teeth)
        4. Apply formula: (base_power + teeth_boost) * claw_multiplier
        Args:
            target: The creature to attack
        """
        total_damage = self.base_power
        claw_multiplier = 1  # Default: no claws
        teeth_boost = 0  # Default: no teeth

        # Apply damage modifiers from body parts
        for part in self.parts:
            if isinstance(part, parts.Claws):
                # If creature has multiple claws, use the largest multiplier
                claw_multiplier = max(claw_multiplier, part.size_multiplier)
            elif isinstance(part, parts.Teeth):
                # If creature has multiple teeth sets, use the sharpest
                teeth_boost = max(teeth_boost, part.sharpness_boost)

        # Final damage: (Base + Teeth Boost) × Claw Multiplier
        total_damage = (total_damage + teeth_boost) * claw_multiplier

        LOGGER.debug(f"Attacked for {total_damage} damage.")
        target.current_health -= total_damage
