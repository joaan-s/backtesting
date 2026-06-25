from src.backtester import Backtester, Strategy

if __name__ == "__main__":
  # Create a backtester for Apple stock (AAPL)
  backtester = Backtester("AAPL", "2023-01-01", "2024-01-01")

  # Download the data
  backtester.download_data()

  # Run trading strategy
  strategy = Strategy(short_window=20, long_window=50)
  backtester.backtest_strategy(strategy)