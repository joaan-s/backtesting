import matplotlib.pyplot as plt
import pandas as pd
from src.data_provider import DataProvider

class Backtester:
  def __init__(self, ticker, start_date, end_date):
    self.ticker = ticker
    self.start_date = start_date
    self.end_date = end_date
    self.data = None
    self.data_provider = DataProvider()

  def download_data(self):
    """Get historical price data (from local cache if available, else downloads it)"""
    self.data = self.data_provider.get_price_data(self.ticker, self.start_date, self.end_date)
    print(f"Loaded {len(self.data)} days for {self.ticker}")
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

  def plot_price_history(self):
      """Display a chart of price history"""
      if self.data is None:
          print("No data available. Download data first!")
          return
      close_prices = self.data['Close'].values.flatten()  # Convert to numpy array

      #Create the chart
      plt.figure(figsize=(12, 6))
      plt.plot(close_prices, linewidth=2, color='blue')
      plt.title(f'{self.ticker} Price History ({self.start_date} to {self.end_date})', fontsize=14)
      plt.xlabel('Days', fontsize=12)
      plt.ylabel('Price ($)', fontsize=12)
      plt.grid(True, alpha=0.3)
      plt.tight_layout()
      plt.show()
  def run_strategy(self, strategy):
      """Run a strategy and display results"""
      if self.data is None:
          print("No data available. Download data first!")
          return

      signals = strategy.generate_signals(self.data['Close'])

      print(f"\n=== Trading signals for {self.ticker} ===")
      for signal_type, day, price in signals:
          print(f"Day {day}: {signal_type} at ${price:.2f}")
      if not signals:
          print("No trading signals  generated")

  def backtest_strategy(self, strategy):
      """Run a strategy and display results"""
      if self.data is None:
          print("No data available. Download data first!")
          return
      signals = strategy.generate_signals(self.data['Close'])

      print(f"\n=== Backtesting signals for {self.ticker} ===")
      if signals:
          for signal_type, day, price in signals:
              print(f"Day {day}: {signal_type} at ${price:.2f}")
      else:
          print("No trading signals generated")

      # Calculate backtest results
      results = BacktestResults(signals, self.data['Close'])
      results.print_results()

  def plot_strategy_signals(self, strategy):
      """Plot price history with buy/sell signals"""
      if self.data is None:
          print("No data available. Download data first!")
          return

      close_prices = self.data['Close'].values.flatten()
      signals = strategy.generate_signals(self.data['Close'])

      # Separate buy and sell signals
      buy_signals = [(day, price) for sig_type, day, price in signals if sig_type == 'BUY']
      sell_signals = [(day, price) for sig_type, day, price in signals if sig_type == 'SELL']

      # Create the chart
      plt.figure(figsize=(14, 7))
      plt.plot(close_prices, linewidth=2, color='blue', label='Price')

      # Plot buy signals
      if buy_signals:
          buy_days, buy_prices = zip(*buy_signals)
          plt.scatter(buy_days, buy_prices, color = 'green', marker='^', s=100, label='BUY Signal')

          # Plot sell signals (red dots)
          if sell_signals:
              sell_days, sell_prices = zip(*sell_signals)
              plt.scatter(sell_days, sell_prices, color='red', marker='v', s=100, label='SELL Signal')

          plt.title(f'{self.ticker} Price History with Trading Signals ({self.start_date} to {self.end_date})',
                    fontsize=14)
          plt.xlabel('Days', fontsize=12)
          plt.ylabel('Price ($)', fontsize=12)
          plt.grid(True, alpha=0.3)
          plt.legend()
          plt.tight_layout()
          plt.show()

  def run_batch_test(self, strategy):
      if self.data is None:
          print("No data available. Download data first!")
          return

      if not isinstance(strategy, DeathCrossStrategy):
          raise ValueError("Strategy must be DeathCrossStrategy")

      results_list = strategy.batch_test_signals(self.data['Close'])

      print(f"\n=== Trading signals for {self.ticker} with 20/50, 30/100, and 50/200 ===")
      for label, signals in results_list:
          print(f"\nFor ratio {label}:")
          results = BacktestResults(signals, self.data['Close'])
          results.print_results()
      return


class DeathCrossStrategy:
  def __init__(self, short_window=20, long_window=50):
    self.short_window = short_window
    self.long_window = long_window

  def calculate_moving_averages(self, prices):
      """Calculate short and long moving averages"""
      short_ma = prices.rolling(window=self.short_window).mean()
      long_ma = prices.rolling(window=self.long_window).mean()
      return short_ma, long_ma

  def generate_signals(self, prices):
      """Generate buy/sell signals based on moving average crossover"""
      # Flatten the prices to handle MultiIndex
      prices_flat = prices.values.flatten()
      df = pd.DataFrame({'Close': prices_flat})

      # Calculate moving averages on flattened data
      short_ma = pd.Series(prices_flat).rolling(window=self.short_window).mean()
      long_ma = pd.Series(prices_flat).rolling(window=self.long_window).mean()

      df['Short'] = short_ma
      df['Long'] = long_ma
      df['Short_Prev'] = df['Short'].shift(1)
      df['Long_Prev'] = df['Long'].shift(1)
      df['BUY_Signal'] = (df['Short'] > df['Long']) & (df['Short_Prev'] <= df['Long_Prev'])
      df['SELL_Signal'] = (df['Short'] < df['Long']) & (df['Short_Prev'] >= df['Long_Prev'])

      # Buy signal: short MA crosses above long MA
      # Sell signal: short MA crosses below long MA
      buy_days = df[df['BUY_Signal']].index.tolist()
      sell_days = df[df['SELL_Signal']].index.tolist()

      signals = []
      for day in buy_days:
          signals.append(('BUY', day, df.loc[day, 'Close']))
      for day in sell_days:
          signals.append(('SELL', day, df.loc[day, 'Close']))

      # Sort chronologically by day - without this, all BUYs would come
      # before all SELLs regardless of which happened first, which corrupts
      # the trade simulation in BacktestResults
      signals.sort(key=lambda signal: signal[1])

      return signals

  def batch_test_signals(self, prices):
      """Tests the usual ratios 20/50, 30/100, 50/200"""
      signals_short = DeathCrossStrategy(short_window=20, long_window=50).generate_signals(prices)
      signals_med = DeathCrossStrategy(short_window=30, long_window=100).generate_signals(prices)
      signals_long = DeathCrossStrategy(short_window=50, long_window=200).generate_signals(prices)
      return [
          ("20/50", signals_short),
          ("30/100", signals_med),
          ("50/200", signals_long),
      ]


class BacktestResults:
    """Calculate and display backtest results"""

    def __init__(self, signals, prices, initial_capital=10000):
        self.signals = signals
        self.prices = prices.values.flatten()
        self.initial_capital = initial_capital

    def calculate_results(self):
        """Calculate backtest metrics"""
        if not self.signals:
            print("No signals to test")
            return

        capital = self.initial_capital
        shares = 0
        trades = []

        for signal_type, day, price in self.signals:
            if signal_type == 'BUY':
                # Buy as many shares as we can afford
                shares = capital / price
                trades.append({'type': 'BUY', 'day': day, 'price': price, 'shares': shares})
                capital = 0

            elif signal_type == 'SELL' and shares > 0:
                # Sell all shares
                capital = shares * price
                trades.append({'type': 'SELL', 'day': day, 'price': price, 'capital': capital})
                shares = 0

        # If we still have shares left we sell them.
        if shares > 0:
            final_price = self.prices[-1]
            capital = shares * final_price
            trades.append({'type': 'SELL', 'day': len(self.prices)-1, 'price': final_price, 'capital': capital})

        # Calculate results
        total_return = capital - self.initial_capital
        return_percent = total_return / self.initial_capital * 100

        return {
            'trades': trades,
            'initial_capital': self.initial_capital,
            'final_capital': capital,
            'total_return': total_return,
            'return_percent': return_percent,
            'num_trades': len([t for t in trades if t['type'] == 'BUY'])
        }

    def print_results(self):
        """Print backtest metrics"""
        results = self.calculate_results()

        if results is None:
            return

        print(f"\n=== Backtest Results ===")
        print(f"Initial Capital: ${results['initial_capital']:.2f}")
        print(f"Final Capital: ${results['final_capital']:.2f}")
        print(f"Total Return: ${results['total_return']:.2f}")
        print(f"Return %: {results['return_percent']:.2f}%")
        print(f"Number of Trades: {results['num_trades']}\n")

        print("Trade Details:")
        for trade in results['trades']:
            if trade['type'] == 'BUY':
                print(f"  Day {trade['day']}: BUY {trade['shares']:.4f} shares @ ${trade['price']:.2f}")
            else:
                print(f"  Day {trade['day']}: SELL @ ${trade['price']:.2f} = ${trade['capital']:.2f}")