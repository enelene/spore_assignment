# core/simulation.py

import logging
import random

from core import config
from core.creature import Creature
from core.creature_factory import CreatureFactory

LOGGER = logging.getLogger(__name__)


class Simulation:
    """Manages the full simulation loop."""

    def __init__(self) -> None:
        self.factory: CreatureFactory = CreatureFactory()

    def run(self) -> None:
        """Runs a single, complete simulation."""

        # 1. Evolution Phase
        LOGGER.info("--- EVOLUTION PHASE ---")

        # Evolve a 'predator' at position 0
        predator = self.factory.evolve_creature(position=0, role="predator")
        LOGGER.info("Evolved Predator:")
        predator.log_characteristics()

        # Evolve a 'prey' at a random distance ahead
        prey_pos = random.randint(config.PREY_MIN_SPAWN, config.PREY_MAX_SPAWN)
        prey = self.factory.evolve_creature(position=prey_pos, role="prey")
        LOGGER.info(f"Evolved Prey at {prey_pos}:")
        prey.log_characteristics()

        # 2. Chase Phase
        LOGGER.info("--- CHASE PHASE ---")
        chase_result = self._run_chase(predator, prey)

        if not chase_result:
            # Predator failed to catch prey (ran out of stamina or took too long)
            LOGGER.warning("Pray ran into infinity")
            return

        # 3. Fight Phase (only happens if predator caught prey)
        LOGGER.info("--- FIGHT PHASE ---")
        self._run_fight(predator, prey)

    def _run_chase(self, predator: Creature, prey: Creature) -> bool:
        """
        Runs the chase phase with improved logic.
        The chase continues until:
        - Predator catches prey (positions meet/overlap) → True
        - Predator runs out of stamina → False
        - Maximum iterations reached (failsafe) → False
        Args:
            predator: The hunting creature
            prey: The fleeing creature
        Returns:
            True if predator catches prey, False if prey escapes
        """
        iterations = 0

        while predator.position < prey.position:
            iterations += 1

            # Failsafe: prevent infinite loops
            if iterations > config.MAX_CHASE_ITERATIONS:
                LOGGER.debug("Chase exceeded maximum iterations.")
                return False

            # Check if predator has stamina to continue
            if not predator.has_stamina:
                LOGGER.debug("Predator ran out of stamina during chase.")
                return False

            # Predator moves (using its decision strategy)
            pred_move = predator.move()

            # Prey also tries to escape (using its decision strategy)
            # Prey will move as long as it has stamina
            prey_move = 0
            if prey.has_stamina:
                prey_move = prey.move()
            # If prey is out of stamina, it can't move (prey_move stays 0)

            LOGGER.debug(
                f"Chase turn {iterations}: "
                f"Predator at {predator.position} (+{pred_move}), "
                f"Prey at {prey.position} (+{prey_move}), "
                f"Gap: {prey.position - predator.position}"
            )

            # Check for stalemate scenarios
            if pred_move == 0:
                # Predator can't move anymore
                LOGGER.debug("Predator cannot move (no valid movement).")
                return False

            # If both are moving at same speed and predator has no stamina advantage,
            # prey will escape eventually
            if (
                pred_move <= prey_move
                and predator.current_stamina <= prey.current_stamina
            ):
                LOGGER.debug(
                    "Stalemate detected: prey matching or exceeding predator speed."
                )
                return False

        # If we exit the loop, predator has caught up
        LOGGER.info(f"CATCH! Predator caught prey at position {predator.position}")
        return True

    def _run_fight(self, predator: Creature, prey: Creature) -> None:
        """
        Runs the fight phase.
        Creatures take turns attacking until one dies:
        1. Predator attacks first
        2. If prey survives, prey counterattacks
        3. Repeat until one dies
        Args:
            predator: The attacking creature
            prey: The defending creature
        """
        fight_round = 0

        while True:
            fight_round += 1

            # Predator attacks first
            predator.attack(prey)
            LOGGER.debug(
                f"Round {fight_round}: Predator attacks. "
                f"Prey health: {prey.current_health}/{prey.max_health}"
            )

            # Check if prey died
            if not prey.is_alive:
                # Per assignment: "Some R-rated things have happened"
                LOGGER.warning("Some R-rated things have happened")
                return

            # Prey fights back
            prey.attack(predator)
            LOGGER.debug(
                f"Round {fight_round}: Prey counterattacks. "
                f"Predator health: {predator.current_health}/{predator.max_health}"
            )

            # Check if predator died
            if not predator.is_alive:
                # Per assignment: "Pray ran into infinity"
                # (Prey won the fight, so it effectively escaped)
                LOGGER.warning("Pray ran into infinity")
                return
