# Stock Backtesting Engine

A Python backtesting framework for testing trading strategies on historical stock data.

## Features

- 📊 Download real market data (yfinance)
- 📈 Moving average crossover strategy
- 💰 Calculate profit/loss metrics
- 📉 Visualize price history and trade signals

## Quick Start

### Setup
```bash
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run
```bash
python main.py
```

This will:
1. Download 1 year of AAPL stock data
2. Run moving average strategy (20/50 day windows)
3. Calculate backtest results
4. Display chart with buy/sell signals
5. For changing dates and tickers use config.json

## Project Structure

```
src/
  backtester.py    - Core classes (Backtester, Strategy, BacktestResults)
main.py            - Entry point
requirements.txt   - Dependencies
config.json        - User configuration
```

## Current Capabilities

- ✅ Download historical stock data
- ✅ Calculate price statistics (avg, min, max, change %)
- ✅ Moving average crossover strategy
- ✅ Backtest performance metrics
- ✅ Price visualization with trade signals

## Next Steps

See [ROADMAP.md](ROADMAP.md) for upcoming features.
