import unittest

from core import chase_strategy, movement, parts
from core.creature import Creature


class TestDecisionStrategies(unittest.TestCase):
    """Test movement decision strategies."""

    def setUp(self) -> None:
        """Create a creature with various parts."""
        self.creature = Creature(0, 100, 150, 10)
        self.creature.parts = [
            parts.Legs(count=2),
            parts.Wings(count=2),
        ]

    def test_greedy_decision_chooses_fastest(self) -> None:
        """Test that greedy decision chooses flying (fastest)."""
        strategy = chase_strategy.GreedyDecision()
        chosen = strategy.decide_movement(self.creature)
        self.assertIsInstance(chosen, movement.FlyMovement)

    def test_greedy_decision_no_wings(self) -> None:
        """Test greedy decision without wings."""
        self.creature.parts = [parts.Legs(count=2)]
        self.creature.current_stamina = 100
        strategy = chase_strategy.GreedyDecision()
        chosen = strategy.decide_movement(self.creature)
        self.assertIsInstance(chosen, movement.RunMovement)

    def test_conservative_decision_low_stamina(self) -> None:
        """Test conservative decision with low stamina."""
        self.creature.current_stamina = 20  # Low stamina
        strategy = chase_strategy.ConservativeDecision()
        chosen = strategy.decide_movement(self.creature)
        # Should choose hop or crawl, not fly/run
        self.assertNotIsInstance(chosen, movement.FlyMovement)
        self.assertNotIsInstance(chosen, movement.RunMovement)

    def test_adaptive_decision_predator(self) -> None:
        """Test adaptive decision for predator role."""
        strategy = chase_strategy.AdaptiveDecision(role="predator")
        chosen = strategy.decide_movement(self.creature)
        # With high stamina, should be aggressive (fly)
        self.assertIsInstance(chosen, movement.FlyMovement)

    def test_strategy_change_at_runtime(self) -> None:
        """Test that decision strategy can be changed."""
        self.creature.set_decision_strategy(chase_strategy.ConservativeDecision())
        self.assertIsInstance(
            self.creature.decision_strategy,
            chase_strategy.ConservativeDecision,
        )
