import unittest

from core import chase_strategy
from core.creature_factory import CreatureFactory


class TestCreatureFactory(unittest.TestCase):
    """Test creature factory functionality."""

    def setUp(self) -> None:
        """Create a factory instance."""
        self.factory = CreatureFactory()

    def test_evolve_predator(self) -> None:
        """Test that predators are evolved correctly."""
        predator = self.factory.evolve_creature(position=0, role="predator")
        self.assertEqual(predator.position, 0)
        self.assertGreaterEqual(predator.max_stamina, 120)
        self.assertLessEqual(predator.max_stamina, 200)

    def test_evolve_prey(self) -> None:
        """Test that prey are evolved correctly."""
        prey = self.factory.evolve_creature(position=100, role="prey")
        self.assertEqual(prey.position, 100)
        self.assertGreaterEqual(prey.max_stamina, 40)
        self.assertLessEqual(prey.max_stamina, 100)

    def test_predator_has_decision_strategy(self) -> None:
        """Test that evolved creatures have decision strategies."""
        predator = self.factory.evolve_creature(position=0, role="predator")
        self.assertIsNotNone(predator.decision_strategy)
        self.assertIsInstance(
            predator.decision_strategy,
            chase_strategy.AdaptiveDecision,
        )
