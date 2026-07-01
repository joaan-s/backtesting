from src.backtester import Backtester, DeathCrossStrategy

if __name__ == "__main__":
  # Create a backtester for Apple stock (AAPL)
  backtester = Backtester("AAPL", "2023-01-01", "2024-01-01")

  # Download the data
  backtester.download_data()

  # Run trading strategy
  print("Elige una estrategia:")
  print("1) Death Cross Strategy")

  strategy = input("Escribe el número de tu opción: ")
  if strategy == "1":
      strategy = DeathCrossStrategy(short_window=20, long_window=50)
  else:
      print(ValueError)
  backtester.backtest_strategy(strategy)

  # Plot signals on chart
  backtester.plot_strategy_signals(strategy)