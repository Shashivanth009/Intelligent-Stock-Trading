import numpy as np
from preprocessing.preprocess import load_data, add_indicators
from models.lstm_model import build_model
from trading.strategy import simulate_trading
from evaluation.metrics import sharpe_ratio, max_drawdown
from sklearn.preprocessing import MinMaxScaler

# In-memory model cache: (data_path, epochs, window) -> model
_model_cache = {}

def run_simulation(data_path="data/stock_data.csv", epochs=3, window=10, initial_balance=10000):
    df = load_data(data_path)
    df = add_indicators(df)

    features = df[['Open', 'High', 'Low', 'Close', 'Volume', 'SMA', 'EMA']].values
    prices = df['Close'].values
    dates = df.index.strftime('%Y-%m-%d').tolist()

    scaler = MinMaxScaler()
    features_scaled = scaler.fit_transform(features)

    X, y = [], []
    for i in range(window, len(features_scaled)):
        X.append(features_scaled[i-window:i])
        y.append(prices[i])

    X = np.array(X)
    y = np.array(y)

    # Flatten 3D (n, window, features) -> 2D (n, window*features) for sklearn
    X_flat = X.reshape(X.shape[0], -1)

    # 80/20 train-test split
    split = int(len(X_flat) * 0.8)
    X_train, y_train = X_flat[:split], y[:split]

    # Use cached model if parameters match, else train fresh
    cache_key = (data_path, epochs, window)
    if cache_key in _model_cache:
        model = _model_cache[cache_key]
    else:
        model = build_model(epochs=epochs)
        model.fit(X_train, y_train)
        _model_cache[cache_key] = model

    predictions = model.predict(X_flat)

    # Trading simulation
    final_value, trade_count, portfolio_values = simulate_trading(
        prices[window:],
        predictions,
        initial_balance=initial_balance
    )

    net_profit = final_value - initial_balance
    roi = (net_profit / initial_balance) * 100

    # Performance metrics
    daily_returns = np.diff(portfolio_values) / portfolio_values[:-1]
    sharpe = sharpe_ratio(daily_returns) if len(daily_returns) > 0 else 0
    max_dd = max_drawdown(portfolio_values) * 100

    results = {
        "final_value": round(final_value, 2),
        "net_profit": round(net_profit, 2),
        "roi": round(roi, 2),
        "total_trades": trade_count,
        "sharpe_ratio": round(float(sharpe), 4),
        "max_drawdown": round(float(max_dd), 2),
        "actual_prices": prices[window:].tolist(),
        "predicted_prices": predictions.tolist(),
        "dates": dates[window:],
        "ohlc": {
            "open": df['Open'].values[window:].tolist(),
            "high": df['High'].values[window:].tolist(),
            "low":  df['Low'].values[window:].tolist(),
            "close": df['Close'].values[window:].tolist(),
            "dates": dates[window:]
        },
        "indicators": {
            "sma": df['SMA'].values[window:].tolist(),
            "ema": df['EMA'].values[window:].tolist()
        }
    }

    return results


if __name__ == "__main__":
    initial_balance = 10000
    epochs = 3
    window = 10

    results = run_simulation("data/stock_data.csv", epochs, window, initial_balance)

    print("\n" + "=" * 55)
    print(" INTELLIGENT STOCK PRICE PREDICTION & AUTO-TRADING ")
    print("=" * 55)
    print(f"\nTotal Trades Executed: {results['total_trades']}")
    print(f"Final Portfolio Value: ₹{results['final_value']:,.2f}")
    print(f"Net Profit           : ₹{results['net_profit']:,.2f}")
    print(f"Return on Investment : {results['roi']:.2f} %")
    print(f"Sharpe Ratio         : {results['sharpe_ratio']:.4f}")
    print(f"Max Drawdown         : {results['max_drawdown']:.2f} %")
