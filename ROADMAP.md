# Development Roadmap

## Phase 1: Data Persistence ⏳ (In Progress)
**Goal:** Store historical data instead of downloading every run

- [ ] SQLite database setup
- [ ] `DataStore` class for save/load
- [ ] Avoid API rate limits by caching data
- [ ] CLI to manage database

**Why:** Real systems don't re-download data. You'll learn SQL + database design.

---

## Phase 2: Strategy Comparison (In progress)
**Goal:** Test multiple strategies and compare results

- [ ] Parameterizable strategy windows
- [ ] Batch test (20/50, 30/100, 50/200 combinations)
- [ ] Compare metrics across strategies
- [ ] Export results to CSV

**Why:** Learn optimization + data analysis. Which parameters work best?

---

## Phase 3: Risk Metrics (Not Started)
**Goal:** Measure risk, not just return

- [ ] Sharpe Ratio calculation
- [ ] Max Drawdown analysis
- [ ] Win Rate %
- [ ] Return vs Risk visualization

**Why:** Professional traders care about risk. Profit alone is incomplete.

---

## Phase 4: Advanced Features (Not Started)
**Goal:** Build a production-ready backtester

- [ ] Transaction fees/slippage
- [ ] Multiple stock support
- [ ] Different timeframes (daily, weekly, hourly)
- [ ] Unit tests (pytest)
- [ ] Command-line interface (click or argparse)

**Why:** Real backtesting is complex. These are essentials.

---

## Phase 5: Visualization & Export (Not Started)
**Goal:** Export results for analysis

- [ ] Save trades to CSV
- [ ] Generate performance reports (PDF)
- [ ] Interactive charts (plotly)
- [ ] Equity curve visualization

**Why:** Results mean nothing if you can't analyze and share them.

---

## Long-term Vision

Once complete, this becomes a **full backtesting framework** you can:
- Use to test your own strategies
- Share as an open-source tool
- Build a web UI on top of it
- Extend with ML-based strategies

Your README says "salto de escribir código a diseñar software" — this roadmap is exactly that journey. 🚀
