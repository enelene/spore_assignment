import unittest

from core import parts


class TestBodyParts(unittest.TestCase):
    """Test body part creation and attributes."""

    def test_legs_creation(self) -> None:
        """Test that Legs are created correctly."""
        legs = parts.Legs(count=2)
        self.assertEqual(legs.count, 2)

    def test_legs_negative_count(self) -> None:
        """Test that negative leg counts are handled."""
        legs = parts.Legs(count=-1)
        self.assertEqual(legs.count, 0)

    def test_wings_creation(self) -> None:
        """Test that Wings are created correctly."""
        wings = parts.Wings(count=4)
        self.assertEqual(wings.count, 4)

    def test_claws_creation(self) -> None:
        """Test that Claws have correct multipliers."""
        small = parts.Claws(size=parts.ClawSize.SMALL)
        medium = parts.Claws(size=parts.ClawSize.MEDIUM)
        big = parts.Claws(size=parts.ClawSize.BIG)

        self.assertEqual(small.size_multiplier, 2)
        self.assertEqual(medium.size_multiplier, 3)
        self.assertEqual(big.size_multiplier, 4)

    def test_teeth_creation(self) -> None:
        """Test that Teeth have correct boosts."""
        low = parts.Teeth(sharpness=parts.TeethSharpness.LOW)
        medium = parts.Teeth(sharpness=parts.TeethSharpness.MEDIUM)
        high = parts.Teeth(sharpness=parts.TeethSharpness.HIGH)

        self.assertEqual(low.sharpness_boost, 3)
        self.assertEqual(medium.sharpness_boost, 6)
        self.assertEqual(high.sharpness_boost, 9)
