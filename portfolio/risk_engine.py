"""Deterministic long-only risk and portfolio analysis tools.

No market data is downloaded. Price inputs must be independently verified.
"""
from dataclasses import dataclass
from math import isfinite, sqrt
from statistics import mean, stdev


@dataclass(frozen=True)
class Trade:
    symbol: str
    entry: float
    exit: float
    quantity: int
    commission: float = 0.0

    def __post_init__(self):
        if not self.symbol.strip():
            raise ValueError("symbol required")
        if any(not isfinite(x) for x in (self.entry, self.exit, self.commission)):
            raise ValueError("prices and costs must be finite")
        if self.entry <= 0 or self.exit < 0 or self.quantity <= 0 or self.commission < 0:
            raise ValueError("invalid prices, quantity, or commission")

    @property
    def pnl(self) -> float:
        return (self.exit - self.entry) * self.quantity - self.commission

    @property
    def capital(self) -> float:
        return self.entry * self.quantity

    @property
    def return_pct(self) -> float:
        return self.pnl / self.capital * 100


def max_drawdown(equity: list[float]) -> float:
    """Return maximum peak-to-trough drawdown as a nonnegative fraction."""
    if not equity or any(not isfinite(x) or x <= 0 for x in equity):
        raise ValueError("equity must contain positive finite values")
    peak = equity[0]
    largest = 0.0
    for value in equity:
        peak = max(peak, value)
        largest = max(largest, (peak - value) / peak)
    return largest


def sharpe_ratio(returns: list[float], periods_per_year: int = 252,
                 risk_free_per_period: float = 0.0) -> float | None:
    """Annualized arithmetic Sharpe ratio; returns None for zero variance."""
    if periods_per_year <= 0 or not isfinite(risk_free_per_period):
        raise ValueError("invalid parameters")
    if len(returns) < 2 or any(not isfinite(x) for x in returns):
        return None
    excess = [x - risk_free_per_period for x in returns]
    sigma = stdev(excess)
    return mean(excess) / sigma * sqrt(periods_per_year) if sigma else None


def trade_summary(trades: list[Trade]) -> dict[str, float | int | None]:
    winners = [t for t in trades if t.pnl > 0]
    losers = [t for t in trades if t.pnl < 0]
    gross_win = sum(t.pnl for t in winners)
    gross_loss = -sum(t.pnl for t in losers)
    return {
        "trade_count": len(trades),
        "net_pnl": round(sum(t.pnl for t in trades), 2),
        "win_rate": round(len(winners) / len(trades), 4) if trades else None,
        "profit_factor": round(gross_win / gross_loss, 4) if gross_loss else None,
        "average_return_pct": round(mean(t.return_pct for t in trades), 4) if trades else None,
    }
