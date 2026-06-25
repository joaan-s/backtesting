from src.backtester import Backtester

backtester = Backtester("AAPL", "2023-01-01", "2024-01-01")
backtester.download_data()

close_prices = backtester.data['Close']
print(type(close_prices))
print(close_prices.head())
print(type(close_prices.mean()))
print(close_prices.mean())