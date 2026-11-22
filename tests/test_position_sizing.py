import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from position_sizing import shares_for_risk


class PositionSizingTests(unittest.TestCase):
    def test_risk_limit(self):
        self.assertEqual(shares_for_risk(10000, .01, 10, 9), 100)

    def test_cash_limit(self):
        self.assertEqual(shares_for_risk(100, .5, 10, 9.9), 10)

    def test_rejects_invalid_stop(self):
        with self.assertRaises(ValueError):
            shares_for_risk(10000, .01, 10, 11)

    def test_rejects_invalid_risk_fraction(self):
        with self.assertRaises(ValueError):
            shares_for_risk(10000, 0, 10, 9)


if __name__ == "__main__":
    unittest.main()
