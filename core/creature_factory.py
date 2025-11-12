# core/creature_factory.py

import random

from core import chase_strategy, config, parts
from core.creature import Creature


class CreatureFactory:
    """
    A factory responsible for 'evolving' new creatures.s
    Creates creatures with stats and body parts appropriate to their role,
    and assigns them a decision strategy that fits their behavior.
    """

    def evolve_creature(self, position: int, role: str = "prey") -> Creature:
        """
        Creates a new Creature instance with randomized stats and parts
        based on the provided 'role' (predator or prey).
        Args:
            position: Starting position on the world ray
            role: Either "predator" or "prey"
        Returns:
            A fully evolved Creature instance
        """
        # 1. Evolve base stats based on role
        if role == "predator":
            max_stamina = random.randint(
                config.PREDATOR_MIN_STAMINA, config.PREDATOR_MAX_STAMINA
            )
            chance_legs = config.PREDATOR_CHANCE_LEGS
            chance_wings = config.PREDATOR_CHANCE_WINGS
            chance_claws = config.PREDATOR_CHANCE_CLAWS
            chance_teeth = config.PREDATOR_CHANCE_TEETH
            # Predators use adaptive strategy: fast early, sustainable later
            decision_strategy = chase_strategy.AdaptiveDecision(role="predator")
        else:  # 'prey'
            max_stamina = random.randint(
                config.PREY_MIN_STAMINA, config.PREY_MAX_STAMINA
            )
            chance_legs = config.PREY_CHANCE_LEGS
            chance_wings = config.PREY_CHANCE_WINGS
            chance_claws = config.PREY_CHANCE_CLAWS
            chance_teeth = config.PREY_CHANCE_TEETH
            # Prey use adaptive strategy: prioritize escape
            decision_strategy = chase_strategy.AdaptiveDecision(role="prey")

        max_health = random.randint(config.MIN_HEALTH, config.MAX_HEALTH)
        base_power = random.randint(config.MIN_POWER, config.MAX_POWER)

        new_creature = Creature(
            position=position,
            max_health=max_health,
            max_stamina=max_stamina,
            base_power=base_power,
            decision_strategy=decision_strategy,
        )

        # 2. Evolve body parts based on role-specific chances
        evolved_parts: list[parts.BodyPart] = []

        # Legs: Essential for running/walking
        if random.random() < chance_legs:
            # More legs = more movement options
            evolved_parts.append(parts.Legs(count=random.randint(1, 4)))

        # Wings: Best for speed (flying) but require 2+ wings
        if random.random() < chance_wings:
            # Must have at least 2 wings to fly
            evolved_parts.append(parts.Wings(count=random.choice([2, 4])))

        # Claws: Damage multipliers
        if random.random() < chance_claws:
            evolved_parts.append(parts.Claws(size=random.choice(list(parts.ClawSize))))

        # Teeth: Damage boosts
        if random.random() < chance_teeth:
            evolved_parts.append(
                parts.Teeth(sharpness=random.choice(list(parts.TeethSharpness)))
            )

        new_creature.parts = evolved_parts
        return new_creature
