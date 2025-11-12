import unittest

from core import movement, parts
from core.creature import Creature


class TestMovementStrategies(unittest.TestCase):
    """Test movement strategy implementations."""

    def setUp(self) -> None:
        """Create a creature with full stamina."""
        self.creature = Creature(0, 100, 100, 10)

    def test_crawl_movement(self) -> None:
        """Test crawl movement."""
        strategy = movement.CrawlMovement()
        distance = strategy.move(self.creature)
        self.assertEqual(distance, 1)
        self.assertEqual(self.creature.current_stamina, 99)

    def test_hop_movement_success(self) -> None:
        """Test hop movement with sufficient stamina."""
        self.creature.parts = [parts.Legs(count=1)]
        self.creature.max_stamina = 20
        self.creature.current_stamina = 20
        strategy = movement.HopMovement()
        distance = strategy.move(self.creature)
        self.assertEqual(distance, 3)
        self.assertEqual(self.creature.current_stamina, 18)

    def test_hop_movement_failure(self) -> None:
        """Test hop movement without sufficient stamina."""
        self.creature.max_stamina = 10
        self.creature.current_stamina = 1
        strategy = movement.HopMovement()
        distance = strategy.move(self.creature)
        self.assertEqual(distance, 0)

    def test_walk_movement(self) -> None:
        """Test walk movement."""
        self.creature.max_stamina = 40
        self.creature.current_stamina = 40
        strategy = movement.WalkMovement()
        distance = strategy.move(self.creature)
        self.assertEqual(distance, 4)
        self.assertEqual(self.creature.current_stamina, 38)

    def test_run_movement(self) -> None:
        """Test run movement."""
        self.creature.max_stamina = 60
        self.creature.current_stamina = 60
        strategy = movement.RunMovement()
        distance = strategy.move(self.creature)
        self.assertEqual(distance, 6)
        self.assertEqual(self.creature.current_stamina, 56)

    def test_fly_movement(self) -> None:
        """Test fly movement."""
        self.creature.max_stamina = 80
        self.creature.current_stamina = 80
        strategy = movement.FlyMovement()
        distance = strategy.move(self.creature)
        self.assertEqual(distance, 8)
        self.assertEqual(self.creature.current_stamina, 76)
