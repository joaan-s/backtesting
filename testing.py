from src.backtester import Backtester

backtester = Backtester("AAPL", "2023-01-01", "2024-01-01")
backtester.download_data()
avg_price = backtester.calculate_statistics().iloc[0]
print(type(avg_price))