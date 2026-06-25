import yfinance as yf

class Backtester:
  def __init__(self, ticker, start_date, end_date):
    self.ticker = ticker
    self.start_date = start_date
    self.end_date = end_date
    self.data = None

  def download_data(self):
    """Download historical price data"""
    print(f"Downlowding data for {self.ticker}...")
    self.data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
    print(f"Downloaded {len(self.data)} days")
    return self.data

  def show_data(self):
    """Display the downloaded data"""
    print(self.data.head(10))  # Show first 10 rows

  def calculate_statistics(self):
      """Calculate and print simple statistics"""
      if self.data is None:
          print("No data available. Download data first!")
          return

      close_prices = self.data['Close'].values.flatten()  # Convert to numpy array

      # Calculate statistics
      avg_price = close_prices.mean()
      max_price = close_prices.max()
      min_price = close_prices.min()
      start_price = float(close_prices[0])
      end_price = float(close_prices[-1])
      price_change = end_price - start_price
      price_change_percent = (price_change / start_price) * 100

      # Print results
      print(f"\n=== Statistics for {self.ticker} ===")
      print(f"Average Price: ${avg_price:.2f}")
      print(f"Highest Price: ${max_price:.2f}")
      print(f"Lowest Price: ${min_price:.2f}")
      print(f"Starting Price: ${start_price:.2f}")
      print(f"Ending Price: ${end_price:.2f}")
      print(f"Total Change: ${price_change:.2f} ({price_change_percent:.2f}%)\n")