import unittest

from core import parts
from core.creature import Creature


class TestCreature(unittest.TestCase):
    """Test Creature class functionality."""

    def setUp(self) -> None:
        """Create a basic creature for testing."""
        self.creature = Creature(
            position=0,
            max_health=100,
            max_stamina=100,
            base_power=10,
        )

    def test_creature_initialization(self) -> None:
        """Test that creatures are initialized correctly."""
        self.assertEqual(self.creature.position, 0)
        self.assertEqual(self.creature.max_health, 100)
        self.assertEqual(self.creature.current_health, 100)
        self.assertEqual(self.creature.max_stamina, 100)
        self.assertEqual(self.creature.current_stamina, 100)
        self.assertEqual(self.creature.base_power, 10)

    def test_is_alive_property(self) -> None:
        """Test the is_alive property."""
        self.assertTrue(self.creature.is_alive)
        self.creature.current_health = 0
        self.assertFalse(self.creature.is_alive)

    def test_has_stamina_property(self) -> None:
        """Test the has_stamina property."""
        self.assertTrue(self.creature.has_stamina)
        self.creature.current_stamina = 0
        self.assertFalse(self.creature.has_stamina)

    def test_num_legs_property(self) -> None:
        """Test that leg counting works."""
        self.creature.parts = [parts.Legs(count=2), parts.Legs(count=2)]
        self.assertEqual(self.creature._num_legs, 4)

    def test_num_wings_property(self) -> None:
        """Test that wing counting works."""
        self.creature.parts = [parts.Wings(count=2)]
        self.assertEqual(self.creature._num_wings, 2)

    def test_attack_base_damage(self) -> None:
        """Test basic attack without modifiers."""
        target = Creature(0, 100, 100, 10)
        self.creature.attack(target)
        self.assertEqual(target.current_health, 90)

    def test_attack_with_claws(self) -> None:
        """Test attack with claw multiplier."""
        target = Creature(0, 100, 100, 10)
        self.creature.parts = [parts.Claws(size=parts.ClawSize.SMALL)]
        self.creature.attack(target)
        # 10 * 2 = 20 damage
        self.assertEqual(target.current_health, 80)

    def test_attack_with_teeth(self) -> None:
        """Test attack with teeth boost."""
        target = Creature(0, 100, 100, 10)
        self.creature.parts = [parts.Teeth(sharpness=parts.TeethSharpness.LOW)]
        self.creature.attack(target)
        # (10 + 3) * 1 = 13 damage
        self.assertEqual(target.current_health, 87)

    def test_attack_with_claws_and_teeth(self) -> None:
        """Test attack with both claws and teeth."""
        target = Creature(0, 100, 100, 10)
        self.creature.parts = [
            parts.Claws(size=parts.ClawSize.MEDIUM),
            parts.Teeth(sharpness=parts.TeethSharpness.MEDIUM),
        ]
        self.creature.attack(target)
        # (10 + 6) * 3 = 48 damage
        self.assertEqual(target.current_health, 52)
