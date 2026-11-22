# Quantitative Trading Utilities

Educational Python utilities for calculating position size based on a maximum dollar-risk budget.

## Run

```bash
python examples/position_sizing.py
```

The function caps shares by both account buying power and risk between the entry and stop prices. It does not account for slippage, fees, liquidity, or price gaps and does not guarantee a maximum realized loss.

Requires only the Python standard library. Not investment advice.
