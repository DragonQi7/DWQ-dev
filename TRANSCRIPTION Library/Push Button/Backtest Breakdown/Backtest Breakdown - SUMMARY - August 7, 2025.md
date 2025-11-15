# Backtest Breakdown — August 7, 2025 (clean summary)

## Quick summary
- Reviewed two backtests (presented live): **CL** (Crude Oil, full contract) and **MYM** (one-day-per-week setup).
- Main findings: both showed strong early gains that later flattened. CL skipped some days because of dynamic sizing thresholds. Both show attractive profit-to-drawdown ratios but need stability checks.

## Session details
- Tool: NinjaTrader (strategy/backtest view)
- Working account example: $50,000
- Example sizing: CL used $200 risk (2R profit-taker), MYM example used 1.4/200

## 1) CL (Crude Oil)

### Setup & metrics
- Trading days: Mon / Wed / Fri
- Risk example: $200
- Account: $50k
- Example position sizing: 10 lots

### Observations
- Early performance was front-loaded: most gains happened in the first 4–5 weeks.
- June was largely flat (very few trades that month).
- The backtest skipped some days. Root cause: dynamic sizing floor — required fractional positions (<1 contract) were not possible, so the engine skipped those signals.
- Switching to micros (or increasing risk) removed the missing-day problem but changed trade counts and volatility.

### Implications / recommendations
- If you want more consistent daily exposure: increase risk so required sizing meets whole-contract minimums, or trade micro contracts (if available).
- Run rolling-window robustness tests (walk-forward, monthly re-samples) to verify whether the early streak is repeatable or a lucky run.

## 2) MYM (one-day-per-week)

### Setup & metrics
- Trades in example: ~27
- Risk: $200 (example), 1.4 sizing in notes

### Observations
- Similar shape: quick early gains then tapering.
- Small sample size → higher variance; consecutive losing run seen (three losers in a row).

### Implications / recommendations
- One-day-per-week systems need longer evaluation windows. Consider expanding to multiple days per week for steadier statistics.
- Test sensitivity to exit time (example used 12:55 exit) and profit target.

## Analysis tips (how to inspect these issues in NinjaTrader)
- Use Analysis → set aggregation to Daily or Monthly and inspect cumulative net profit to detect front-loaded gains vs steady growth.
- Sort the trade list by profit to find suspicious large wins/losses and open those individual trades for inspection.

## Template backup & restore (how to keep NinjaTrader templates)
Steps used in demonstration:
1. Copy the NinjaTrader templates folder (Documents\NinjaTrader\templates\strategy or similar) to a safe location (desktop/Downloads).
2. Import or install the new strategy version (e.g., MegaOrb 2.2) using Tools → Import NinjaScript Add-on.
3. Paste the backed-up templates folder back into the NinjaTrader directory so saved presets reappear.

## Recommendations / next runs
- For CL:
	- Rerun backtest with $200 vs $500 risk to see if skipped days disappear.
	- If available, test micro contract (MCL) and compare trade counts, net profit, and drawdown.
- For MYM:
	- Run sensitivity tests on exit time and profit target.
	- Accumulate more trades (longer test period) before making a final decision.
- General:
	- Prefer strategies that produce smoother, incremental gains across months rather than ones driven by a single strong streak.
	- Keep a simple backup routine for templates before importing/upgrading strategies or NinjaTrader itself.

## Informal ratings (from the review)
- CL: B- / C+ — good ratios but sizing gap + front-loaded gains.
- MYM: C+ — promising but small sample size.

## Action items
1. Re-run CL with different risk levels & micro contract test.
2. Run rolling-window / walk-forward testing for CL and MYM.
3. For MYM, test exit sensitivity and gather more data.

---
_This file is a cleaned summary of the August 7 live backtest review. Filler conversation was removed; all findings, observations and recommended next steps were preserved._