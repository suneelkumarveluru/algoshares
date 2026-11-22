"""Educational, dependency-free position sizing example.

Not investment advice; does not predict returns.
"""


def shares_for_risk(
    account_value: float,
    risk_fraction: float,
    entry_price: float,
    stop_price: float,
) -> int:
    if account_value <= 0 or not 0 < risk_fraction <= 1:
        raise ValueError("Account and risk fraction must be positive")
    if stop_price < 0 or entry_price <= stop_price:
        raise ValueError("Entry price must be above nonnegative stop price")
    risk_budget = account_value * risk_fraction
    loss_per_share = entry_price - stop_price
    affordable = int(account_value // entry_price)
    by_risk = int(risk_budget // loss_per_share)
    return min(affordable, by_risk)


if __name__ == "__main__":
    print(shares_for_risk(10000, 0.01, 10, 9))
