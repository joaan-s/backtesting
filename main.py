from src.backtester import Backtester, Strategy

if __name__ == "__main__":
  # Create a backtester for Apple stock (AAPL)
  backtester = Backtester("AAPL", "2023-01-01", "2024-01-01")

  # Download the data
  backtester.download_data()

  # Show first 10 rows
  backtester.show_data()

  # Show statistics
  backtester.calculate_statistics()

  # Show chart
  backtester.plot_price_history()

  # Run trading strategy
  strategy = Strategy(short_window=20, long_window=50)
  backtester.run_strategy(strategy)