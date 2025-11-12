# spore/simulation.py

"""
Defines the main Simulation class.

This class orchestrates the simulation phases:
1. Evolution Phase (using the CreatureFactory)
2. Chase Phase
3. Fight Phase
"""

import random
import logging
from spore.factory import CreatureFactory
from spore.creature import Creature

LOGGER = logging.getLogger(__name__)

# --- Balancing Constants ---
PREY_MIN_DISTANCE = 100
PREY_MAX_DISTANCE = 600  # Reduced from 1000 to help the predator


class Simulation:
    """Manages the full simulation loop."""

    def __init__(self) -> None:
        self.factory: CreatureFactory = CreatureFactory()

    def run(self) -> None:
        """Runs a single, complete simulation."""

        # 1. Evolution Phase
        LOGGER.info("--- EVOLUTION PHASE ---")
        # Evolve a 'predator'
        predator = self.factory.evolve_creature(position=0, role="predator")
        LOGGER.info("Evolved Predator:")
        predator.log_characteristics()

        prey_pos = random.randint(PREY_MIN_DISTANCE, PREY_MAX_DISTANCE)
        # Evolve a 'prey'
        prey = self.factory.evolve_creature(position=prey_pos, role="prey")
        LOGGER.info(f"Evolved Prey at {prey_pos}:")
        prey.log_characteristics()

        # 2. Chase Phase
        LOGGER.info("--- CHASE PHASE ---")
        chase_result = self._run_chase(predator, prey)

        if not chase_result:
            # Predator ran out of stamina
            LOGGER.warning("Pray ran into infinity")
            return

        # 3. Fight Phase
        LOGGER.info("--- FIGHT PHASE ---")
        self._run_fight(predator, prey)

    def _run_chase(self, predator: Creature, prey: Creature) -> bool:
        """
        Runs the chase phase.
        Returns True if catch, False if prey escapes.
        """
        while predator.position < prey.position:
            if not predator.has_stamina:
                LOGGER.debug("Predator ran out of stamina during chase.")
                return False  # Prey escapes

            pred_move = predator.move()

            # Prey is also "smart" and runs away
            prey_move = 0
            if prey.has_stamina:
                prey_move = prey.move()

            LOGGER.debug(
                f"Chase: Predator at {predator.position} (+{pred_move}), "
                f"Prey at {prey.position} (+{prey_move})"
            )

            # Failsafe for a stalemate (e.g., both crawl at same speed)
            if pred_move <= prey_move and not predator.has_stamina:
                return False

        LOGGER.info(f"CATCH! Predator at {predator.position}")
        return True  # Predator caught prey

    def _run_fight(self, predator: Creature, prey: Creature) -> None:
        """Runs the fight phase."""
        while True:
            # Predator attacks first
            predator.attack(prey)
            LOGGER.debug(f"Predator attacks. Prey health: {prey.current_health}")
            if not prey.is_alive:
                # Per assignment: "Some R-rated things have happened" :D
                LOGGER.warning("Some R-rated things have happened :D")
                return

            # Prey fights back
            prey.attack(predator)
            # (FIX: E501 - Split long line)
            LOGGER.debug(
                "Prey fights back. Predator health: "
                f"{predator.current_health}"
            )
            if not predator.is_alive:
                # Per assignment: "Pray ran into infinity"
                LOGGER.warning("Pray ran into infinity")
                return