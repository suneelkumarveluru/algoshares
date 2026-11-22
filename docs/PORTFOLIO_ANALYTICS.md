# Portfolio risk analysis CLI

This example takes **your own CSV inputs** and produces a local JSON risk report. There is no brokerage connection, trading signal, data download or order execution.

## Run

From the repository root:

```bash
python portfolio/report.py examples/trades.csv --equity examples/equity.csv
python -m unittest discover -s tests -v
```

Python 3.10+ is sufficient; there are no third-party dependencies.

Trade CSV requires `symbol,entry,exit,quantity`, optionally `commission` (per trade, not per share). Equity CSV requires `equity`, in chronological order; each observation must be positive.

The report includes total net P&L, win rate, average realized trade return, profit factor, maximum peak-to-trough drawdown, and an annualized Sharpe estimate when equity data is available.

**Assumptions:** trades are long-only, equity observations are uniformly spaced and assumed daily for Sharpe (252 periods per year). Positions may overlap; this is a journal summary rather than a comprehensive portfolio accounting engine. Profit factor is null when no losses occur. Historical performance does not predict future returns. Prices exclude slippage, taxes and market-impact effects. Use anonymized inputs and never commit personal brokerage statements.
