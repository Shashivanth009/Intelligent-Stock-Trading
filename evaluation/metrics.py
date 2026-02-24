import numpy as np

def profit_loss(initial, final):
    return final - initial

def sharpe_ratio(returns):
    if returns.std() == 0:
        return 0
    return returns.mean() / returns.std()

def max_drawdown(values):
    peak = values[0]
    max_dd = 0

    for v in values:
        if v > peak:
            peak = v
        dd = (peak - v) / peak
        if dd > max_dd:
            max_dd = dd

    return max_dd
