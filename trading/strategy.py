import numpy as np

def simulate_trading(prices, predictions, initial_balance=10000):
    balance = initial_balance
    shares = 0
    trade_count = 0
    portfolio_values = []

    for i in range(len(predictions)):
        price = prices[i]

        if predictions[i] > price and balance >= price:
            shares += 1
            balance -= price
            trade_count += 1

        elif predictions[i] < price and shares > 0:
            shares -= 1
            balance += price
            trade_count += 1

        portfolio_values.append(balance + shares * price)

    final_value = balance + shares * prices[-1]
    return final_value, trade_count, np.array(portfolio_values)
