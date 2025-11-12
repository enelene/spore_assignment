# spore/factory.py

"""
Implements the Factory Design Pattern for creature creation.

This encapsulates the complex logic of "evolving" a creature
(randomizing stats and parts) into one dedicated class.
This follows the Single Responsibility Principle.

--- UPDATED ---
The factory now accepts a 'role' to evolve creatures
with different stats and part probabilities, which is
key for balancing the simulation.
"""

import random
from spore import parts
from spore.creature import Creature

# --- Constants for Evolution ---
MIN_HEALTH, MAX_HEALTH = 80, 120
MIN_POWER, MAX_POWER = 5, 15

# --- Predator-specific Constants ---
PREDATOR_MIN_STAMINA = 70
PREDATOR_MAX_STAMINA = 150
PREDATOR_CHANCE_LEGS = 0.6
PREDATOR_CHANCE_WINGS = 0.5
PREDATOR_CHANCE_CLAWS = 0.8  # High chance for attack
PREDATOR_CHANCE_TEETH = 0.7  # High chance for attack

# --- Prey-specific Constants ---
PREY_MIN_STAMINA = 30
PREY_MAX_STAMINA = 90
PREY_CHANCE_LEGS = 0.8  # High chance for escape
PREY_CHANCE_WINGS = 0.4  # High chance for escape
PREY_CHANCE_CLAWS = 0.3
PREY_CHANCE_TEETH = 0.3


class CreatureFactory:
    """A factory responsible for 'evolving' new creatures."""

    def evolve_creature(self, position: int, role: str = "prey") -> Creature:
        """
        Creates a new Creature instance with randomized stats and parts
        based on the provided 'role' (predator or prey).
        """
        # 1. Evolve base stats based on role
        if role == "predator":
            max_stamina = random.randint(PREDATOR_MIN_STAMINA, PREDATOR_MAX_STAMINA)
            chance_legs = PREDATOR_CHANCE_LEGS
            chance_wings = PREDATOR_CHANCE_WINGS
            chance_claws = PREDATOR_CHANCE_CLAWS
            chance_teeth = PREDATOR_CHANCE_TEETH
        else:  # 'prey'
            max_stamina = random.randint(PREY_MIN_STAMINA, PREY_MAX_STAMINA)
            chance_legs = PREY_CHANCE_LEGS
            chance_wings = PREY_CHANCE_WINGS
            chance_claws = PREY_CHANCE_CLAWS
            chance_teeth = PREY_CHANCE_TEETH

        max_health = random.randint(MIN_HEALTH, MAX_HEALTH)
        base_power = random.randint(MIN_POWER, MAX_POWER)

        new_creature = Creature(
            position=position,
            max_health=max_health,
            max_stamina=max_stamina,
            base_power=base_power,
        )

        # 2. Evolve body parts based on role-specific chances
        evolved_parts: list[parts.BodyPart] = []
        if random.random() < chance_legs:
            evolved_parts.append(parts.Legs(count=random.randint(1, 4)))

        if random.random() < chance_wings:
            # Must have at least 2 wings to fly
            evolved_parts.append(parts.Wings(count=random.choice([2, 4])))

        if random.random() < chance_claws:
            evolved_parts.append(parts.Claws(size=random.choice(list(parts.ClawSize))))

        if random.random() < chance_teeth:
            evolved_parts.append(
                parts.Teeth(sharpness=random.choice(list(parts.TeethSharpness)))
            )

        new_creature.parts = evolved_parts
        return new_creature