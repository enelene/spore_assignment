import unittest

from core import parts
from core.creature import Creature


class TestCreatureMovement(unittest.TestCase):
    """Integration tests for creature movement."""

    def test_creature_move_updates_position(self) -> None:
        """Test that moving updates creature position."""
        creature = Creature(0, 100, 100, 10)
        creature.parts = [parts.Legs(count=2)]
        initial_pos = creature.position
        creature.move()
        self.assertGreater(creature.position, initial_pos)

    def test_creature_movement_depletes_stamina(self) -> None:
        """Test that moving depletes stamina."""
        creature = Creature(0, 100, 100, 10)
        initial_stamina = creature.current_stamina
        creature.move()
        self.assertLess(creature.current_stamina, initial_stamina)
