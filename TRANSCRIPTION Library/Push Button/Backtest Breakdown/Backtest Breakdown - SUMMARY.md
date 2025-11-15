# Backtest Breakdown — SUMMARY

Location: `TRANSCRIPTION Library/Push Button/Backtest Breakdown/`

Generated: October 16, 2025 (summary of session transcripts in this folder)

Purpose: one-page table of contents and concise per-session TL;DR + actionable recommendations so you can scan lessons learned from the Backtest Breakdown series without opening each raw transcript.

---

## Table of contents

1. Backtest Breakdown - July 3 2025.txt
2. Backtest Breakdown - July 31 2025.txt
3. Backtest Breakdown - August 7, 2025.txt
4. Backtest Breakdown - August 14 2025.txt
5. Backtest Breakdown - Sept 11 2025.txt
6. Backtest Breakdown September 18 2025.txt
7. Backtest Breakdown - September 25 2025.txt
8. Backtest Breakdown September 25 2025 - Push Button Trading (720p, h264).txt
9. Backtest Breakdown - Oct 9 2025.txt
10. Backtest Breakdown Session October 16 2025.txt
11. Backtest Breakdown Session October 16 2025 - Push Button Trading (720p, h264).txt

---

## Per-session summaries

Each entry below contains: TL;DR, key highlights, and recommended next actions (copyable checklist).

1) Backtest Breakdown - July 3 2025
    - File metadata:
       - Path: `TRANSCRIPTION Library/Push Button/Backtest Breakdown/Backtest Breakdown - July 3 2025.txt`
       - Type: instructor-led backtest review session (transcript)
       - Primary topics: Mega Scalper (MES), Mega Orb, Mega Snapback, one-tick backtests, strategy templates, VPS & funded-account operational guidance

    - TL;DR
       A practical coaching session that walks through user-submitted backtests (Diana's Mega Scalper on MES is the main example), demonstrates running single backtests with "high one-tick" historical fill processing, and explains how to map backtest parameters (risk, trailing stops, profit-taker, max trades/day) to funded-account sizing and live deployment. The instructor also covers operational hygiene (template naming, timezone handling, VPS housekeeping) and trader psychology (how to handle losing streaks).

    - File structure & flow (what happens in the recording)
       1. Opening logistics and quick NinjaTrader restart due to a frozen client.
       2. Load Diana's Mega Scalper template (MES, 3-minute), run a single high one-tick backtest, and inspect performance and trade list.
       3. Discuss bot configuration: $150 risk, no profit taker (so exits on max unrealized giveback or drawdown), trailing stop = 75 ticks, max-trades/day = 10.
       4. Map results to account sizing (10% rule example), equity-curve interpretation, and funded-account (Apex) payout rules (30% single-day threshold).
       5. Run additional examples (Mega Orb, Mega Snapback, larger-account templates) and compare behavior.
       6. Operational & behavioral guidance: VPS routines, avoid chart clutter, template/version hygiene, and emotional discipline when facing losing streaks.

    - Key excerpts & instructor notes (paraphrased/verbatim highlights)
       - "Always run single backtests with high one-tick historical fill processing for accuracy." — repeated emphasis.
       - If profit taker is off the bot may remain in trades until hitting configured unrealized-gain reversal or max drawdown.
       - Label templates clearly (name/date/version) and convert strategy times to local timezone before live deployment.
       - Use the Strategies tab instead of many open charts to reduce VPS resource use and avoid micromanagement.

    - Technical details you can reuse
       - Recommended NinjaTrader setting for single backtests: High one-tick (historical fill processing).
       - Example bot params from session:
          - Risk per trade: $150 (example mapping to a 25K/50K style account depending on goal)
          - Trailing stop: 75 ticks (MES example ~ $18.75)
          - Profit taker: off (so exits based on drawback or trailing stop)
          - Max trades/day: 10
       - Mapping example: 50K funded goal ~ $3,000 objective; 10% risk rule -> $150 per trade.

    - Actionable checklist (copy/paste in your workflow)
       - [ ] Run any single-strategy backtest with "high one-tick" for accurate fills.
       - [ ] Save the strategy template as: <User>-<Bot>-YYYYMMDD-<notes>.tpl
       - [ ] Confirm profit taker / trailing stop behavior — if profit-taker is off, document unrealized-exit rules.
       - [ ] Convert strategy time windows to your local timezone before going live; save a timezone-labeled template.
       - [ ] Compare Strategy Analyzer trade count vs. live account trade count: if mismatched, check partial-day settings, connectivity, or version mismatch.
       - [ ] VPS housekeeping: weekly cache/db cleanup, reconnect before market open, and keep chart count minimal.

    - Observations & instructor recommendations
       - Reproducibility and template/version hygiene are primary defenses against live-vs-backtest mismatches.
       - Large single-day wins can trigger funded-account payout rules (some firms have a 30% single-day cap) — track daily P&L per funded account carefully.
       - Behavioral: accept losing runs as part of the distribution; avoid switching strategies mid-run unless a structural issue is found.

    - Suggested follow-ups (I can do these for you)
       - Export the exact template settings shown in this session into a Markdown snippet or JSON saved under `TRANSCRIPTION Library/Push Button/Backtest Breakdown/`.
       - Generate a one-page "Backtest checklist" Markdown file for your team (I can create `Backtest-Checklist.md`).
       - Create a CSV row summarizing July 3 (filename, one-line TL;DR, top actions).
       Tell me which of the three you'd like and I will create it now.

2) Backtest Breakdown - July 31 2025
   - TL;DR: Deep dive into Mega Orb and implications of trade counts, consecutive losers, and template/version control.
   - Highlights: trade-count analysis, consecutive-loss statistics, recommendations on template naming and versioning.
   - Actionable: standardize strategy template naming (include date/version); log consecutive-loss runs and add a kill-switch threshold in templates.

3) Backtest Breakdown - August 7, 2025
   - TL;DR: Contrast CL and MYM backtests; micro vs full contracts and how front-loaded gains and monthly distributions present in results.
   - Highlights: contract sizing impacts commission and sample distribution; front-loaded gains vs steady returns.
   - Actionable: include contract-size as factor in portfolio builder; test same strategy across micro/mini/full to compare commission drag.

4) Backtest Breakdown - August 14 2025
   - TL;DR: Volume-bot discussion and combining backtests; Quant Analyzer integration and portfolio-level effects.
   - Highlights: combining strategies changes drawdown and net profit; toolchain improvements (built-in analyzer) reduce manual spreadsheet work.
   - Actionable: use built-in portfolio builder/analyzer for combined stats; maintain a checklist for correlation/conflict checks before live deployment.

5) Backtest Breakdown - Sept 11 2025
   - TL;DR: Portfolio mixing, sample-size guidance, and funded/eval account rules; statistics on consecutive losers and how to interpret sample size.
   - Highlights: suggested sample sizes, how consecutive-loss distributions inform risk sizing, Apex funded account considerations (percent rules).
   - Actionable: build a short CSV of strategy sample sizes and consecutive loser stats; add Apex rule checks to your account checklist.

6) Backtest Breakdown September 18 2025
   - TL;DR: Troubleshooting connection and snapshot losses; guidance on exporting logs and verifying execution/connection issues.
   - Highlights: common live vs backtest mismatch causes (connection hiccups, rollover issues), recommended logger/export steps.
   - Actionable: implement a daily connection & log export routine; add a template for 'when live losses spike' diagnostics.

7) Backtest Breakdown - September 25 2025
   - TL;DR: Contract rollover, template saving habits, commission templates for Apex; account-reset & rebill edge cases discussed.
   - Highlights: commission and rollover handling, account rebill pitfalls (email/payment timing), template/version hygiene.
   - Actionable: create commission template per broker; add calendar reminders for rebill windows; ensure template versions include broker/contract symbols.

8) Backtest Breakdown September 25 2025 - Push Button Trading (720p, h264)
   - TL;DR: Video-session variant — same core points as 9/25 transcript plus visual walk-through of templates and installer behavior.
   - Highlights: installer workflow, zip/unzip/installer steps, Microsoft Defender smart-screen guidance for installer acceptance.
   - Actionable: save copy of the installer instructions in a README under this folder; include a short 'trusted installer' FAQ for users.

9) Backtest Breakdown - Oct 9 2025
   - TL;DR: Trade copier entry modes — execution (market) vs order (limit/stop-limit) and volume-based choice; demo of built-in portfolio builder & quant analyzer replacement.
   - Highlights: when to use execution vs order mode (use execution for very liquid assets like MNQ/MES; order/limit for low-liquidity assets like MBT); new built-in portfolio builder/analyzer features and conflict detection.
   - Actionable: choose order vs execution by volume threshold (suggested: use execution when 5-min avg volume > ~1k); add volume-check to pre-deployment checklist and save portfolio templates in the new built-in format.

10) Backtest Breakdown Session October 16 2025
    - TL;DR: Portfolio builder + analyzer walkthrough, live testimonials, VPS & resource guidance, new feature previews (directional filter, contract limits, SuperSnap Orb) and operational recommendations.
    - Highlights: installer and template workflows; portfolio generation replaces spreadsheets; added directional filters and contract limit settings; VPS sizing & housekeeping recommendations; suggestion to transition from funded accounts to personal trading accounts over time.
    - Actionable: run portfolio builder with default templates; convert selected strategies to local timezone before live run; weekly VPS cleanup routine and keep only one chart open on VPS; reserve 50% of payouts into a bootstrap personal account.

11) Backtest Breakdown Session October 16 2025 - Push Button Trading (720p, h264)
    - TL;DR: Video-recorded variant of the Oct 16 session; contains same content plus on-screen demo of directional-filter UI, no-trades-greater/less-than contract feature, and SuperSnap Orb overview.
    - Highlights: visual demo of the new settings, and the roadmap for upcoming bots and filters.
    - Actionable: watch the installer & demo video; try the new SuperSnap Orb in a sandbox once released; add 'directional-filter' parameter to backtest metadata for future comparisons.

---

## Quick next steps (recommended)
- Save this SUMMARY.md and commit to repo for team reference.
- Export a CSV row for each file with: filename, date, TL;DR (one line), key actions (short). I can generate that next if you want.
- If you'd like, I can also generate a short README (How to use these transcripts) and a diagnostics checklist for live-vs-backtest mismatches.

If you want edits, or a CSV export of the TOC + TL;DR rows, tell me and I'll generate it into `md/` or `CSVs/` under this folder.

---

Generated by: repository assistant (synthesized from session transcripts in this folder).
