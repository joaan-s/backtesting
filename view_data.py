import sqlite3
import pandas as pd

conn = sqlite3.connect("data/market_data.db")
df = pd.read_sql_query("SELECT * FROM prices", conn)
print(df)
conn.close()