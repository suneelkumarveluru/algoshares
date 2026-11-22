"""Read a trade journal CSV and print a reproducible JSON risk report.

Usage: python portfolio/report.py examples/trades.csv --equity examples/equity.csv
"""
import argparse
import csv
import json
from pathlib import Path
from risk_engine import Trade, max_drawdown, sharpe_ratio, trade_summary


def read_trades(path: Path) -> list[Trade]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"symbol", "entry", "exit", "quantity"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"Missing required columns: {sorted(required - set(reader.fieldnames or []))}")
        trades = []
        for line, row in enumerate(reader, 2):
            try:
                trades.append(Trade(row["symbol"], float(row["entry"]),
                                    float(row["exit"]), int(row["quantity"]),
                                    float(row.get("commission") or 0)))
            except (TypeError, ValueError) as error:
                raise ValueError(f"Invalid trade at CSV line {line}: {error}") from error
    return trades


def read_equity(path: Path) -> list[float]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or "equity" not in reader.fieldnames:
            raise ValueError("Equity file must contain 'equity' header")
        return [float(row["equity"]) for row in reader]


def build_report(trades: list[Trade], equity: list[float] | None = None) -> dict:
    report = trade_summary(trades)
    if equity:
        report["max_drawdown_pct"] = round(max_drawdown(equity) * 100, 4)
        period_returns = [b / a - 1 for a, b in zip(equity, equity[1:])]
        report["sharpe_ratio"] = sharpe_ratio(period_returns)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trades", type=Path)
    parser.add_argument("--equity", type=Path)
    args = parser.parse_args()
    try:
        report = build_report(read_trades(args.trades),
                              read_equity(args.equity) if args.equity else None)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
