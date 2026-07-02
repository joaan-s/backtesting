import sqlite3
import pandas as pd
import yfinance as yf
import os


class DataProvider:
    """
    Handles downloading, storing, and retrieving historical price data.

    Data is cached in a local SQLite database (data/market_data.db).
    On each request, it checks what's already stored and only downloads
    from yfinance whatever is missing, instead of re-downloading everything
    every time the program runs.
    """

    def __init__(self, db_path="data/market_data.db"):
        self.db_path = db_path

        # Make sure the folder for the database file exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        self._create_table_if_missing()

    def _connect(self):
        """Open a connection to the SQLite database file."""
        return sqlite3.connect(self.db_path)

    def _create_table_if_missing(self):
        """
        Create the 'prices' table if it doesn't exist yet.

        PRIMARY KEY (ticker, date) means SQLite will reject any attempt
        to insert a duplicate row for the same ticker+date combo. That's
        what protects us from storing the same day twice.
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prices (
                ticker TEXT NOT NULL,
                date TEXT NOT NULL,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                PRIMARY KEY (ticker, date)
            )
        """)
        conn.commit()
        conn.close()

    def _get_stored_dates(self, ticker, start_date, end_date):
        """Return the set of dates we already have stored for this ticker/range."""
        conn = self._connect()
        query = """
            SELECT date FROM prices
            WHERE ticker = ? AND date >= ? AND date <= ?
        """
        df = pd.read_sql_query(query, conn, params=(ticker, start_date, end_date))
        conn.close()
        return set(df["date"])

    def _download_from_yfinance(self, ticker, start_date, end_date):
        """Download fresh data from yfinance for the given range."""
        print(f"Downloading {ticker} data from Yahoo Finance ({start_date} to {end_date})...")
        data = yf.download(ticker, start=start_date, end=end_date)

        if data.empty:
            return pd.DataFrame()

        # yfinance can return MultiIndex columns (e.g. when downloading
        # multiple tickers at once) - flatten just in case
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        data = data.reset_index()  # turns the Date index into a normal column
        data["date"] = data["Date"].dt.strftime("%Y-%m-%d")
        data["ticker"] = ticker

        return data[["ticker", "date", "Open", "High", "Low", "Close", "Volume"]].rename(
            columns={
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume",
            }
        )

    def _save_to_db(self, df):
        """Insert new rows into the database, skipping any that already exist."""
        if df.empty:
            return

        conn = self._connect()
        cursor = conn.cursor()

        rows = df[["ticker", "date", "open", "high", "low", "close", "volume"]].values.tolist()

        # INSERT OR IGNORE: if a row with the same (ticker, date) primary key
        # already exists, silently skip it instead of raising an error
        cursor.executemany(
            """
            INSERT OR IGNORE INTO prices (ticker, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        conn.commit()
        conn.close()

    def get_price_data(self, ticker, start_date, end_date):
        """
        Main method: returns a DataFrame of price data for the given ticker
        and date range, downloading only what's missing from yfinance.
        """
        all_dates_needed = set(
            pd.date_range(start=start_date, end=end_date, freq="D").strftime("%Y-%m-%d")
        )
        stored_dates = self._get_stored_dates(ticker, start_date, end_date)
        missing = all_dates_needed - stored_dates

        # Trading days are a subset of calendar days (no weekends/holidays),
        # so "missing" here is a loose upper bound - if there's a meaningful
        # gap, just re-download the whole range to keep this simple for now.
        if missing:
            fresh_data = self._download_from_yfinance(ticker, start_date, end_date)
            self._save_to_db(fresh_data)
        else:
            print(f"Using cached data for {ticker} ({start_date} to {end_date})")

        return self._load_from_db(ticker, start_date, end_date)

    def _load_from_db(self, ticker, start_date, end_date):
        """Read the requested range back out of SQLite as a DataFrame."""
        conn = self._connect()
        query = """
            SELECT date, open, high, low, close, volume FROM prices
            WHERE ticker = ? AND date >= ? AND date <= ?
            ORDER BY date ASC
        """
        df = pd.read_sql_query(query, conn, params=(ticker, start_date, end_date))
        conn.close()

        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date")
        df.columns = ["Open", "High", "Low", "Close", "Volume"]  # match yfinance naming
        return df
