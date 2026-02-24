# Intelligent Stock Price Prediction & Auto-Trading

An AI-powered stock trading simulator using LSTM deep learning, with a Flask web interface featuring live charting and performance metrics.

## Features
- LSTM model with Dropout for price prediction
- Technical indicators: SMA(5), EMA(5)
- Automated trading simulation (buy/sell signal logic)
- Performance metrics: ROI, Sharpe Ratio, Max Drawdown
- Interactive Plotly charts: Line + Candlestick with overlays
- CSV file upload (drag & drop)
- Model caching — repeat simulations are instant

## Local Setup

```bash
pip install -r requirements.txt
python app.py
```
Visit `http://127.0.0.1:5000`

## Deploy to Render (Free)

1. Push this project to a GitHub repository
2. Go to [render.com](https://render.com) → **New → Web Service**
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` — click **Deploy**
5. Done! Your app is live in ~3 minutes.

## Project Structure
```
├── app.py                  # Flask web server
├── main.py                 # Simulation orchestrator (with model cache)
├── requirements.txt        # Python dependencies
├── Procfile                # Production start command
├── render.yaml             # Render deployment config
├── preprocessing/
│   └── preprocess.py       # Data loading, date parsing, indicators
├── models/
│   └── lstm_model.py       # LSTM + Dropout architecture
├── trading/
│   └── strategy.py         # Buy/Sell simulation + portfolio tracking
├── evaluation/
│   └── metrics.py          # Sharpe ratio, max drawdown
├── templates/
│   └── index.html          # Web UI
├── static/
│   ├── css/style.css       # Glassmorphism dark-mode styles
│   └── js/script.js        # Plotly charting + API calls
└── data/
    └── stock_data.csv      # Default dataset
```
