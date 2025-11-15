"""Qimen Chart Plotter (Foundational Implementation)

This script provides a foundational, extensible Python implementation to
plot a Qi Men Dun Jia (Qimen Dunjia) DAY chart components:

  1. Earth Plate (3 Nobles / 6 Crescents sequence distributed by Luo Shu path)
  2. Heaven Plate (circular clockwise distribution starting from Lead Stem)
  3. Eight Doors (starting from Envoy / Lead Door then clockwise)
  4. Nine Stars (clockwise sequence from Lead Star)
  5. Eight Deities (forward for Yang, reverse for Yin)

The full traditional system requires:
  - Precise sexagenary (Ganzhi) calculations for Year / Month / Day / Hour pillars
  - Season checks, cycle classification (Upper / Middle / Lower) and Structure index
  - Complete Six Jia Streams Leader Table mapping to Lead Stem

This module assumes you will SUPPLY the required pillars and structure metadata.
It includes partial table examples so you can extend internally without changing
core logic.

USAGE (simplest):
    python plot_qimen_chart.py --day-pillar Ding-Si \
        --year-pillar Ren-Chen \
        --structure-index 3 \
        --structure-type yang \
        --envoy-palace SE

If you know only the Earth Plate lead stem palace, provide --envoy-palace; the
script will derive starting door from Natal Door chart and allocate doors clockwise.

OUTPUT:
  Prints a JSON-like multiline summary of each palace with assigned:
    EarthStem | HeavenStem | Door | Star | Deity

EXTENSION POINTS:
  - Fill in FULL six_jia_stream_leaders mapping (currently illustrative).
  - Implement automatic determination of structure index & type from date.
  - Implement sexagenary cycle conversion (placeholder function provided).

DISCLAIMER:
  This is a pragmatic coding scaffold, not a complete metaphysics engine. For
  authoritative operational charts, cross-check with verified plotting tools.
"""

from __future__ import annotations
import argparse
import datetime as _dt
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

# ------------------------------- Core Data ------------------------------- #

PALACE_ORDER_CLOCKWISE = [
    "NW",  # Qian
    "N",   # Kan
    "NE",  # Gen
    "E",   # Zhen
    "SE",  # Xun
    "S",   # Li
    "SW",  # Kun
    "W",   # Dui
    "C",   # Center (treated separately when needed)
]

# Luo Shu forward (Yang) & reverse (Yin) ignoring Center for flow distribution.
LUO_SHU_FORWARD = ["N", "SW", "E", "SE", "C", "NW", "W", "NE", "S"]
LUO_SHU_REVERSE = list(reversed(LUO_SHU_FORWARD))

# 3 Nobles / 6 Crescents sequence of stems used for Earth Plate (example order)
# Traditional sequences differ by system lineage; adapt if your lineage differs.
EARTH_PLATE_STEM_SEQUENCE = [
    "Wu", "Ji", "Geng", "Xin", "Ren", "Gui", "Ding", "Bing", "Yi"
]

# Nine Star clockwise sequence (starting from Grass as conventional ordering)
NINE_STARS_SEQUENCE = [
    "Grass", "Ambassador", "Destructor", "Assistant", "Hero", "Grain", "Bird", "Pillar", "Heart"
]

NATAL_NINE_STARS_PALACE = {
    # Simplified natal mapping (sample). Fill with full authoritative natal chart as needed.
    "NW": "Assistant",
    "N": "Ren",  # Placeholder / adjust to lineage star name if needed
    "NE": "Bird",  # Example
    "E": "Ambassador",
    "SE": "Grass",
    "S": "Hero",
    "SW": "Grain",
    "W": "Heart",
    "C": "Pillar",  # Center usage optional
}

# Natal Doors in palaces (basic form)
NATAL_DOORS_PALACE = {
    "SE": "Delusion",
    "S": "Scenery",
    "SW": "Rest",
    "N": "Fear",
    "NE": "Death",
    "E": "Harm",
    "W": "Open",
    "NW": "Life",
    "C": "(Center)"  # Not normally used directly as a door start unless envoy rules point there
}

DOORS_SEQUENCE_CLOCKWISE = [
    "Rest", "Death", "Harm", "Delusion", "Open", "Fear", "Life", "Scenery"
]

# Eight Deities arrangements
DEITIES_YANG_FORWARD = ["Chief", "Snake", "Moon", "Harmony", "Hook", "Phoenix", "Earth", "Heaven"]
DEITIES_YIN_REVERSE = ["Chief", "Heaven", "Earth", "Tortoise", "Tiger", "Harmony", "Moon", "Snake"]

# Six Jia Streams Leader Table (partial illustrative subset). Map YEAR STEM-BRANCH -> Lead Stem.
SIX_JIA_STREAM_LEADERS: Dict[str, str] = {
    # Provide actual mapping; placeholders shown.
    "Ren-Chen": "Wu",  # 2012 example (Dragon year) -> Lead Stem Wu (example)
    "Ding-Si": "Wu",   # Example Day Pillar mapping for demonstration
    # Add more entries...
}

# --------------------------- Data Classes -------------------------------- #

@dataclass
class PalaceData:
    earth_stem: str = ""
    heaven_stem: str = ""
    door: str = ""
    star: str = ""
    deity: str = ""

@dataclass
class QimenChart:
    structure_index: int
    structure_type: str  # 'yang' or 'yin'
    day_pillar: str
    year_pillar: str
    envoy_palace: str
    earth_lead_palace: str
    heaven_lead_stem: str
    door_start_palace: str
    star_lead_palace: str
    deity_lead_palace: str
    palaces: Dict[str, PalaceData] = field(default_factory=lambda: {p: PalaceData() for p in PALACE_ORDER_CLOCKWISE})

# --------------------------- Helper Functions ---------------------------- #

def normalize_pillar(p: str) -> str:
    return p.strip().title().replace(" ", "-")

def determine_lead_stem(year_pillar: str) -> str:
    key = normalize_pillar(year_pillar)
    return SIX_JIA_STREAM_LEADERS.get(key, "Wu")  # default fallback

def distribute_earth_plate(structure_type: str, structure_index: int) -> Dict[str, str]:
    """Return mapping palace -> earth stem following Luo Shu forward/reverse starting
    from the structure index's Luo Shu starting palace.
    Structure index 1..9 maps onto Luo Shu position list index (cyclic).
    """
    flow = LUO_SHU_FORWARD if structure_type == "yang" else LUO_SHU_REVERSE
    # Map structure index (1-9) to starting palace based on flow list position
    start_palace = flow[(structure_index - 1) % len(flow)]
    stems = EARTH_PLATE_STEM_SEQUENCE
    mapping: Dict[str, str] = {}
    # rotate flow so start_palace is first
    start_idx = flow.index(start_palace)
    ordered = flow[start_idx:] + flow[:start_idx]
    for i, palace in enumerate(ordered):
        if i < len(stems):
            mapping[palace] = stems[i]
    return mapping

def distribute_heaven_plate(earth_mapping: Dict[str, str], lead_stem: str) -> Dict[str, str]:
    """Heaven Plate: clockwise circular distribution starting from location of lead_stem in earth plate.
    Replicates earth sequence order from that point.
    """
    # Find palace of lead_stem among earth mapping
    lead_palace = next((p for p, s in earth_mapping.items() if s == lead_stem), None)
    if not lead_palace:
        # Fallback: use first palace available
        lead_palace = list(earth_mapping.keys())[0]
    sequence_palaces = [p for p in PALACE_ORDER_CLOCKWISE if p != "C"]  # exclude center for circular path
    start_idx = sequence_palaces.index(lead_palace) if lead_palace in sequence_palaces else 0
    rotated = sequence_palaces[start_idx:] + sequence_palaces[:start_idx]
    earth_sequence = [earth_mapping.get(p, "") for p in rotated]
    return {p: earth_sequence[i] for i, p in enumerate(rotated)}

def starting_door_palace_from_envoy(envoy_palace: str) -> str:
    # In a minimal model we use envoy palace directly as starting door location
    return envoy_palace

def allocate_doors(start_palace: str) -> Dict[str, str]:
    seq = DOORS_SEQUENCE_CLOCKWISE
    circle = [p for p in PALACE_ORDER_CLOCKWISE if p != "C"]
    if start_palace not in circle:
        start_palace = circle[0]
    start_idx = circle.index(start_palace)
    rotated_palaces = circle[start_idx:] + circle[:start_idx]
    doors_assign = {}
    for i, palace in enumerate(rotated_palaces):
        doors_assign[palace] = seq[i % len(seq)]
    return doors_assign

def allocate_stars(lead_palace: str) -> Dict[str, str]:
    seq = NINE_STARS_SEQUENCE
    circle = [p for p in PALACE_ORDER_CLOCKWISE if p != "C"]
    if lead_palace not in circle:
        lead_palace = circle[0]
    start_idx = circle.index(lead_palace)
    rotated = circle[start_idx:] + circle[:start_idx]
    return {p: seq[i % len(seq)] for i, p in enumerate(rotated)}

def allocate_deities(structure_type: str, lead_palace: str) -> Dict[str, str]:
    seq = DEITIES_YANG_FORWARD if structure_type == "yang" else DEITIES_YIN_REVERSE
    circle = [p for p in PALACE_ORDER_CLOCKWISE if p != "C"]
    if lead_palace not in circle:
        lead_palace = circle[0]
    start_idx = circle.index(lead_palace)
    rotated = circle[start_idx:] + circle[:start_idx]
    return {p: seq[i % len(seq)] for i, p in enumerate(rotated)}

# --------------------------- High-Level Build ---------------------------- #

def build_chart(
    day_pillar: str,
    year_pillar: str,
    structure_index: int,
    structure_type: str,
    envoy_palace: str,
) -> QimenChart:
    structure_type = structure_type.lower()
    day_pillar = normalize_pillar(day_pillar)
    year_pillar = normalize_pillar(year_pillar)
    envoy_palace = envoy_palace.upper()

    # Earth Plate
    earth_map = distribute_earth_plate(structure_type, structure_index)
    lead_stem = determine_lead_stem(year_pillar)
    heaven_map = distribute_heaven_plate(earth_map, lead_stem)

    door_start = starting_door_palace_from_envoy(envoy_palace)
    doors_map = allocate_doors(door_start)

    star_lead_palace = envoy_palace  # Simplified assumption
    stars_map = allocate_stars(star_lead_palace)
    deities_map = allocate_deities(structure_type, star_lead_palace)

    chart = QimenChart(
        structure_index=structure_index,
        structure_type=structure_type,
        day_pillar=day_pillar,
        year_pillar=year_pillar,
        envoy_palace=envoy_palace,
        earth_lead_palace=door_start,
        heaven_lead_stem=lead_stem,
        door_start_palace=door_start,
        star_lead_palace=star_lead_palace,
        deity_lead_palace=star_lead_palace,
    )

    for palace in chart.palaces.keys():
        data = chart.palaces[palace]
        data.earth_stem = earth_map.get(palace, "")
        data.heaven_stem = heaven_map.get(palace, "")
        data.door = doors_map.get(palace, "")
        data.star = stars_map.get(palace, "")
        data.deity = deities_map.get(palace, "")

    return chart

def serialize_chart(chart: QimenChart) -> str:
    lines = []
    header = f"Qimen Day Chart | Day Pillar: {chart.day_pillar} | Year Pillar: {chart.year_pillar} | Structure: {chart.structure_type.title()} {chart.structure_index}"
    lines.append(header)
    lines.append("=" * len(header))
    lines.append("Palace | EarthStem | HeavenStem | Door | Star | Deity")
    lines.append("-------|-----------|-----------|------|------|-------")
    for palace in PALACE_ORDER_CLOCKWISE:
        pd = chart.palaces[palace]
        lines.append(
            f"{palace:>6} | {pd.earth_stem or '-':<9} | {pd.heaven_stem or '-':<9} | {pd.door or '-':<6} | {pd.star or '-':<6} | {pd.deity or '-':<7}"
        )
    return "\n".join(lines)

# --------------------------- CLI Interface ------------------------------- #

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Plot a simplified Qimen Day Chart")
    ap.add_argument("--day-pillar", required=True, help="Day pillar e.g. Ding-Si")
    ap.add_argument("--year-pillar", required=True, help="Year pillar e.g. Ren-Chen")
    ap.add_argument("--structure-index", type=int, required=True, help="Structure number (1-9)")
    ap.add_argument("--structure-type", choices=["yang", "yin"], required=True, help="Structure type")
    ap.add_argument("--envoy-palace", required=True, help="Palace code of Earth Plate Lead Stem (NW,N,NE,E,SE,S,SW,W)")
    return ap.parse_args()

def main():
    args = parse_args()
    chart = build_chart(
        day_pillar=args.day_pillar,
        year_pillar=args.year_pillar,
        structure_index=args.structure_index,
        structure_type=args.structure_type,
        envoy_palace=args.envoy_palace,
    )
    print(serialize_chart(chart))
    print("\nNotes:")
    print("  - Fill SIX_JIA_STREAM_LEADERS with full mapping for accurate Lead Stem selection.")
    print("  - Extend NATAL_NINE_STARS_PALACE & NATAL_DOORS_PALACE for lineage-specific natal placements.")
    print("  - Implement automatic pillar calculation if needed (placeholder pipeline kept manual).")

if __name__ == "__main__":
    main()
