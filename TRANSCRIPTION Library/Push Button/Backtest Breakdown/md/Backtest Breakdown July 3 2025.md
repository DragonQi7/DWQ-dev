# Backtest Breakdown — July 3, 2025

**Path:** `TRANSCRIPTION Library/Push Button/Backtest Breakdown/Backtest Breakdown - July 3 2025.txt`

## TL;DR

A practical coaching session that reviews user-submitted backtests (primary example: Diana's Mega Scalper on MES). The instructor demonstrates single backtests with "high one-tick" historical fill processing and explains how to map strategy parameters (risk, trailing stops, profit-taker, max trades/day) to live deployment and funded-account sizing. Operational hygiene (template naming, timezone handling, VPS routines) and trader behavior (handling losing streaks) are emphasized.

---

## File structure & flow

1. Opening / logistics (NinjaTrader froze briefly and was restarted).
2. Main review — Diana's Mega Scalper (MES, 3‑min): run high one-tick backtest, inspect trades and equity curve.
3. Parameter discussion: risk, trailing stop, profit-taker, max trades/day, and exit triggers.
4. Mapping results to account sizing and funded-account constraints (Apex 30% single-day rule).
5. Additional examples (Mega Orb, Mega Snapback, larger-account templates).
6. Operational & behavioral guidance (VPS, templates, psychology).
7. Announcements / side topics (Options Pilot credit-spread product).

---

## Key points & instructor highlights

- Always run single-strategy backtests with **High one-tick** (historical fill processing) for the most accurate fills.
- If a strategy has **no profit taker enabled**, it may remain in trades until hitting a configured unrealized-gain reversal or max-drawdown.
- Use the **Strategies** tab (not many open charts) to reduce VPS resource usage and avoid micromanagement.
- Label and version templates clearly (e.g., `Diana-MegaScalper-20250703-v1`) and convert strategy times to your local timezone before going live.
- Watch funded-account rules (example: Apex's ~30% single-day cap) — large single-day wins can affect payouts.

---

## Technical details (reusable)

- NinjaTrader recommendation: **High one-tick** for single backtests (slower but precise).
- Example bot parameters shown in session:
  - Risk per trade: **$150**
  - Trailing stop: **75 ticks** (MES example ≈ $18.75)
  - Profit taker: **disabled** in example (so exits on drawdown / trailing stop)
  - Max trades per day: **10**
- Mapping example: for a **50K** funded target → $3,000 goal, using 10% rule → $150 risk per trade.

---

## Actionable checklist (copy/paste)

- [ ] Run single-strategy backtests with **High one-tick**.
- [ ] Save templates using clear names: `<User>-<Bot>-YYYYMMDD-<notes>.tpl`.
- [ ] Confirm profit-taker / trailing-stop behaviors; document unrealized-exit rules if profit-taker is off.
- [ ] Convert strategy time windows to your local timezone and save a timezone-labeled template.
- [ ] Compare Strategy Analyzer trade counts to live account trade counts; investigate mismatches (partial-day settings, connectivity, template/version mismatch).
- [ ] VPS housekeeping: schedule weekly cleanup (cache/db), reconnect/restart NinjaTrader before market open, keep chart count minimal.

---

## Observations & recommendations

- Reproducibility (templates, timezone hygiene, one-tick backtests) is crucial to avoid live/backtest discrepancies.
- Psychological discipline matters: accept losing runs as expected sample behavior; avoid switching strategies mid-run unless structural issues are discovered.
- Operational reliability (VPS + simple startup routine) reduces missed trades and helps preserve backtest expectations.

---

## Suggested follow-ups (I can create any of these)

1. Export the exact template settings shown in the session into `md/Diana-MegaScalper-20250703-SETTINGS.md` (or JSON).
2. Create a one-page `Backtest-Checklist.md` containing the copyable checklist and minimal NinjaTrader how-to steps.
3. Produce a CSV summarizing session bots and example risk/account mappings: `md/Backtest_Breakdown_SUMMARY.csv`.

Tell me which follow-up(s) you want and I'll create them now.
I'll (1) mark the Backtest Breakdown summary task complete in your todo list, and (2) open Backtest Breakdown - July 3 2025.txt to extract details — expecting the file contents so I can produce a precise, sectioned explanation. I'll run those two actions now.

Completed (45/45) Create Backtest Breakdown TOC & Summaries

Read Backtest Breakdown - July 3 2025.txt

Progress update: I updated the todo list to mark "Create Backtest Breakdown TOC & Summaries" as completed and opened the July 3, 2025 transcript to extract details. Next, I'll give a structured, detailed explanation of Backtest Breakdown - July 3 2025.txt (what it contains, structure, key lessons, actionable recommendations, and suggested next steps).

Quick file metadata
Path: TRANSCRIPTION Library/Push Button/Backtest Breakdown/Backtest Breakdown - July 3 2025.txt
Type: Meeting / backtest review transcript (text)
Speaker/context: Instructor-led backtest review session for Push Button Trading (weekly series). The session reviews multiple user-submitted backtests (Diana/Inga/others), runs live backtests in NinjaTrader, and offers operational/process guidance.
Approx. length read: ~400 lines (I read lines 1–400).
Short summary (TL;DR)
This is a recorded coaching session where the instructor reviews user-submitted backtests (primarily a Mega Scalper on MES and Mega Orb / Mega Snapback examples), walks through live backtest runs in NinjaTrader using high one-tick historical fill processing, explains configuration choices (risk, profit taker, trailing stops, max trades/day), and covers operational topics: versioning templates, VPS practices, funded-account limits (Apex 30% rule), multi-bot portfolio behavior, and an options credit-spread product. The tone is practical and guidance-oriented, aimed at helping students interpret backtest output and translate it to live settings.

File structure and flow
Opening / logistics

Quick check: the instructor asks if attendees have backtests, mentions someone in Italy, and begins session.
NinjaTrader froze briefly and was restarted — this starts a pattern of "how to recover and verify" in live trading.
Main backtest review (Diana's MES Mega Scalper)

The instructor loads Diana's Mega Scalper settings (MES, M3 chart) and emphasizes running with high one-tick historical fill processing for accuracy.
Shows how templates are applied and how to run the strategy both from the Strategy Analyzer and directly on charts.
Discusses specific bot settings: $150 risk per trade, no profit taker enabled (so open until trailing or drawdown condition), trailing stop of 75 ticks, max-trades/day = 10, and how the bot exits on unrealized drawdown or hitting the day's loss limit.
Interpretation of results & account sizing

Explains how to map backtest risk to funded account targets (10% rule example: $1,500 goal -> 10% = $150 risk per trade).
Examines equity curve shape (bottom-left to top-right desirable), sample-size considerations, and the effect of a few large winning streaks on results.
Addresses the 30% per-day payout rule from some prop firms (Apex) and how outsized single-day wins can impact payouts for funded accounts.
Secondary examples

Runs Mega Orb (MNQ 5-minute) and other templates; points out differences in account sizing (example: $500 risk for a 150K setup).
Runs Mega Snapback and other bots with emphasis on using high one-tick for single backtests.
Operational & behavioral guidance

Recommends using the strategies tab (not many charts) to reduce resource load and avoid micromanaging trades.
Encourages using a VPS and a daily reconnection/cleanup routine to keep connections stable.
Discusses how to label and save templates, keep good versioning (date/version included), and save templates named by user/date for reproducibility.
Talks about psychology: do not overreact to small losing streaks (sample-driven), and the importance of letting a vetted backtest play out in a fresh/reset account.
New products & side topics

Mentions Options Pilot (credit spread product) and examples of how small accounts can grow with low-frequency options trades (one or two trades a week).
Also mentions that they acquired another company and integrated options offerings.
Closing

Instructor wraps, gives next-steps suggestions, and invites participants to submit backtests.
Key excerpts / points to note (verbatim paraphrases)
"Always run single backtests with high one-tick historical fill processing for accuracy." (repeated emphasis)
"If there is no profit taker enabled the bot may stay in the trade until hitting a max unrealized-gain reversal (configured) or max-drawdown." (explains why some trades are exited)
"Use the strategies tab rather than opening many charts — charts consume resources on a VPS." (practical system ops)
"Label templates with date/version and save them; template/version hygiene is important." (operational suggestion)
"For funded account rules (Apex): watch single-day large wins — there’s a 30% per-day gain rule that can affect payouts." (risk governance)
Technical details the file explains (useful for applying tests)
Recommended NinjaTrader settings for accurate backtesting:
High one-tick historical fill processing (slow but precise)
Match contract symbols / time zones when saving templates
Typical bot parameters inspected:
Risk per trade ($150 example)
Max-trades/day (10 in sample)
Profit taker usage (on/off); trailing stop (e.g., 75 ticks)
Trade schedule (e.g., Mon/Tue/Thu or specific time windows)
How to map risk to account goals:
Example mapping: 50K funded goal => $3,000 goal, 10% per trade rule => $150 risk per trade
Practical diagnostics:
If backtest shows many trades but live took fewer trades — check partial-day schedule, connection reset, version mismatch, or template timezone differences.
Actionable takeaways (copyable checklist)
For each strategy you test:
 Run a single backtest with "high one-tick" historical fill processing.
 Save a template named like "<User>-<Bot>-YYYYMMDD-<notes>.tpl".
 Record risk-per-trade and expected R-multiples; map to account sizing (10% rule).
 Confirm "profit taker" and "trailing stop" behaviours in template; if profit taker is off, ensure you understand unrealized-exit triggers.
 Check the strategy's day-of-week and time windows match your local timezone before live deployment.
 Run a quick diagnostics: compare Strategy Analyzer trade count vs live account trade count; if mismatch, check dates/time zones and connection logs.
 On VPS: schedule a weekly cleanup (clear cache/database), and reconnect/restart NinjaTrader before market open.
Observations & instructor recommendations (interpretation)
The instructor repeatedly stresses reproducibility: use named templates, consistent timezone handling, and one-tick backtests where precision matters.
Behavioral rules are emphasized: accept losing runs as expected sample behavior, avoid micromanaging and overreacting, and use the strategies tab to minimize resource usage and emotional over-focus.
Operational reliability matters: running on a VPS with housekeeping and simple startup routine (connect, enable strategies) prevents missed trades and lost opportunities.
Suggested follow-ups I can do for you (pick any)
Extract and save the precise bot parameter snapshots shown in the transcript into a small Markdown or JSON file for the Diana template (I can parse and save the settings).
Produce a one-page "Backtest checklist" Markdown with the copyable checklist above and small NinjaTrader how-to steps.
Create a CSV that lists the session's talked-about bots (Mega Scalper, Mega Orb, Mega Snapback, Options Pilot) and their example risk/account mappings.
Extract timestamps (if the transcript had exact timestamps) — this transcript did not include timestamps, but I can add section anchors for linking.
Which follow-up(s) should I do now?