import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "portfolio"))
from risk_engine import Trade, max_drawdown, sharpe_ratio, trade_summary
from report import read_trades, read_equity, build_report


class RiskEngineTests(unittest.TestCase):
    def test_trade_pnl(self):
        self.assertEqual(Trade("X", 10, 12, 5, 1).pnl, 9)

    def test_invalid_trade(self):
        with self.assertRaises(ValueError):
            Trade("X", 0, 12, 5)

    def test_drawdown(self):
        self.assertAlmostEqual(max_drawdown([100, 120, 90, 130]), .25)

    def test_zero_variance_sharpe(self):
        self.assertIsNone(sharpe_ratio([.01, .01, .01]))

    def test_summary(self):
        stats = trade_summary([Trade("A", 10, 12, 5), Trade("B", 10, 9, 5)])
        self.assertEqual(stats["trade_count"], 2)
        self.assertEqual(stats["net_pnl"], 5)
        self.assertEqual(stats["win_rate"], 0.5)

    def test_csv_end_to_end(self):
        with tempfile.TemporaryDirectory() as directory:
            trades = Path(directory) / "trades.csv"
            equity = Path(directory) / "equity.csv"
            trades.write_text("symbol,entry,exit,quantity,commission\nX,10,11,2,0\n", encoding="utf-8")
            equity.write_text("equity\n100\n90\n110\n", encoding="utf-8")
            report = build_report(read_trades(trades), read_equity(equity))
            self.assertEqual(report["net_pnl"], 2)
            self.assertEqual(report["max_drawdown_pct"], 10)

    def test_rejects_malformed_csv(self):
        with tempfile.TemporaryDirectory() as directory:
            trades = Path(directory) / "trades.csv"
            trades.write_text("symbol,entry\nX,10\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_trades(trades)


if __name__ == "__main__":
    unittest.main()
