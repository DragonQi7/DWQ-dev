"""generate_ics_2026.py

Simple generator that reads a precomputed day/month animal listing and
produces an iCalendar (.ics) file with all-day events according to
configured feng-shui rules.

How it works (high level):
- Reads a text file that lists each calendar date along with the day's
    zodiac animal and the month's zodiac animal (see DATA_FILE path below).
- Scans the parsed dates for 2026 and applies two rule sets: DAY_RULES
    and MONTH_RULES. When a match is found, an all-day VEVENT is emitted.
- Writes a single VCALENDAR file to the calendar output path (see OUT_FILE).

Files used/read:
- data/DayMonthAnimals-2025-2026.txt (DATA_FILE) — source list of dates
    with day and month animals. The script expects lines like:
        "Jan 01, 2026 (Thu) Yin Wood Pig Chou Ox"
    The parsing is simple and matches the pattern used in the repository.

Output:
- calendar/Generated-2026-ZodiacDays.ics (OUT_FILE) — the generated
    iCalendar with one VEVENT per matched day/month rule. The file will
    contain alarms (VALARM) and simple conflict markings in the DESCRIPTION.

Notes / assumptions:
- The script uses the text file as authoritative; it does not compute
    zodiac animals itself. If you want computed animals instead, supply
    a different data source or extend the script.
- Events are all-day (DTSTART;VALUE=DATE) and alarms are added as
    relative TRIGGER values so calendar apps translate reminders to local
    time. The calendar sets X-WR-TIMEZONE to America/New_York (EST).
"""

import re
from datetime import datetime, timedelta, date
from pathlib import Path

# Input data file and output ICS path
DATA_FILE = Path(r"c:\Users\tztle\Documents\GitHub\DWQ-dev\data\DayMonthAnimals-2025-2026.txt")
OUT_FILE = Path(r"c:\Users\tztle\Documents\GitHub\DWQ-dev\calendar\Generated-2026-ZodiacDays.ics")

# Rules (day animals)
DAY_RULES = {
    'Rat': [
        ("Nobleman Day — Monkey SW3", "Monkey SW3", "day=Rat → Nobleman Day — Monkey SW3"),
    ],
    'Horse': [
        ("Nobleman Day — Rat N2 (possible clash with Horse 2026)", "Rat N2", "day=Horse → Nobleman Day — Rat N2"),
        ("Peach Blossom Day — Horse S2", "Horse S2", "day=Horse → Peach Blossom Day — Horse S2"),
    ],
    'Rooster': [
        ("Intelligence Day — Rooster W2", "Rooster W2", "day=Rooster → Intelligence Day — Rooster W2"),
    ],
    'Pig': [
        ("Sky Horse Day — Pig NW3", "Pig NW3", "day=Pig → Sky Horse Day — Pig NW3"),
    ],
}

# Rules (month animals)
MONTH_RULES = {
    'Rat': [
        ("Nobleman Month — Monkey SW3", "Monkey SW3", "month=Rat → Nobleman Month — Monkey SW3"),
    ],
    'Horse': [
        ("Nobleman Month — Rat N2 (possible clash with Horse 2026)", "Rat N2", "month=Horse → Nobleman Month — Rat N2"),
        ("Peach Blossom Month — Horse S2", "Horse S2", "month=Horse → Peach Blossom Month — Horse S2"),
    ],
    'Rooster': [
        ("Intelligence Month — Rooster W2", "Rooster W2", "month=Rooster → Intelligence Month — Rooster W2"),
    ],
    'Pig': [
        ("Sky Horse Month — Pig NW3", "Pig NW3", "month=Pig → Sky Horse Month — Pig NW3"),
    ],
}

# Example lines look like:
# "Jan 01, 2026 (Thu) Yin Wood Pig Chou Ox"
DATE_RE = re.compile(r"^(\w{3})\s(\d{2}),\s(\d{4})\s\([^)]*\)\s(?:Yin|Yang)\s\w+\s(\w+)\s\w+\s(\w+)$")
MONTHS = {m: i for i, m in enumerate(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"], start=1)}


def parse_lines():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Data file not found: {DATA_FILE}")
    text = DATA_FILE.read_text(encoding='utf-8')
    tokens = re.split(r"\s*(?=\w{3}\s\d{2},\s\d{4}\s\()", text.strip())
    days = []
    for t in tokens:
        t = t.strip()
        if not t:
            continue
        m = DATE_RE.match(t)
        if not m:
            continue
        mon_abbr, day_s, year_s, day_animal, month_animal = m.groups()
        dt = date(int(year_s), MONTHS[mon_abbr], int(day_s))
        days.append({
            'date': dt,
            'day_animal': day_animal,
            'month_animal': month_animal,
        })
    return days


# ---------------------------------------------------------------------------
# Helper/utility notes
# - gen_uid: creates a stable UID for each event using the date, a slug of
#   the summary and an index. This helps avoid duplicate UIDs when emitting
#   multiple events for the same date (conflicts).
# - fmt_date: formats a date to YYYYMMDD as required by VALUE=DATE fields.
# - fold_long_line: folds long iCalendar lines to avoid violating the
#   recommended 75-octet line length (simple split at 70 chars).
# ---------------------------------------------------------------------------


def gen_uid(dt: date, summary: str, idx: int):
    slug = re.sub(r'[^a-z0-9]+','-', summary.lower())
    return f"uid-{dt.strftime('%Y%m%d')}-{slug}-{idx}@dwq-dev"


def fmt_date(d: date):
    return d.strftime('%Y%m%d')


def fold_long_line(s: str) -> list[str]:
    # iCalendar recommends 75 octets per line; we do a simple fold at 70 chars
    res = []
    while len(s) > 70:
        res.append(s[:70])
        s = " " + s[70:]
    res.append(s)
    return res


def emit_event(lines: list[str], dt_start: date, dt_end: date, summary: str, code: str, note: str, conflict: bool, others: list[str], idx: int):
    lines.append("BEGIN:VEVENT")
    lines.append(f"UID:{gen_uid(dt_start, summary, idx)}")
    lines += fold_long_line(f"SUMMARY:{summary}")
    lines.append(f"DTSTART;VALUE=DATE:{fmt_date(dt_start)}")
    lines.append(f"DTEND;VALUE=DATE:{fmt_date(dt_end)}")
    desc_parts = [code, f"Generated from rule: {note}", f"CONFLICT: {'true' if conflict else 'false'}"]
    if conflict and others:
        desc_parts.append("Other events on this date: " + "; ".join(others))
    full_desc = "\\n".join(desc_parts)
    lines += fold_long_line(f"DESCRIPTION:{full_desc}")
    lines.append("CATEGORIES:Zodiac")
    if conflict:
        lines.append("X-PRIORITY:5")
    # Alarm relative to start at 00:00 local: -PT15H => 09:00 previous day in local TZ
    lines.append("BEGIN:VALARM")
    lines.append("TRIGGER:-PT15H")
    lines.append("ACTION:DISPLAY")
    lines += fold_long_line(f"DESCRIPTION:Reminder: {summary} begins soon.")
    lines.append("END:VALARM")
    lines.append("END:VEVENT")


def main():
    days = parse_lines()
    days_2026 = [d for d in days if d['date'].year == 2026]

    out: list[str] = []
    out.append("BEGIN:VCALENDAR")
    out.append("VERSION:2.0")
    out.append("PRODID:-//DWQ Generated//EN")
    out.append("CALSCALE:GREGORIAN")
    out.append("X-WR-CALNAME:2026 Zodiac Investment Windows (EST)")
    out.append("X-WR-TIMEZONE:America/New_York")

    # Day events
    total_day = 0
    for d in days_2026:
        animal = d['day_animal']
        if animal in DAY_RULES:
            rules = DAY_RULES[animal]
            summaries = [r[0] for r in rules]
            conflict = len(rules) > 1
            for idx, (summary, code, note) in enumerate(rules, start=1):
                emit_event(out, d['date'], d['date'] + timedelta(days=1), summary, code, note, conflict, [s for s in summaries if s != summary], idx)
                total_day += 1

    # Month events — contiguous ranges with same month_animal
    total_month = 0
    i = 0
    n = len(days_2026)
    targets = set(MONTH_RULES.keys())
    while i < n:
        cur = days_2026[i]
        m_animal = cur['month_animal']
        if m_animal in targets:
            start = cur['date']
            j = i + 1
            while j < n and days_2026[j]['month_animal'] == m_animal:
                j += 1
            end_excl = days_2026[j-1]['date'] + timedelta(days=1)
            rules = MONTH_RULES[m_animal]
            summaries = [r[0] for r in rules]
            conflict = len(rules) > 1
            for idx, (summary, code, note) in enumerate(rules, start=1):
                emit_event(out, start, end_excl, summary, code, note, conflict, [s for s in summaries if s != summary], idx)
                total_month += 1
            i = j
        else:
            i += 1

    out.append("END:VCALENDAR")

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text("\n".join(out), encoding='utf-8')

    print({
        'total_events': total_day + total_month,
        'total_day_events': total_day,
        'total_month_events': total_month,
        'out_file': str(OUT_FILE)
    })


if __name__ == '__main__':
    main()
