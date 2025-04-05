"""Module providing helper functions"""

import re
from collections import defaultdict
from constants import FORM_SUFFIXES


def strip_form_suffix(name):
    """Removes form suffix from Pokemon Name (Alola, Hisui etc.)"""
    for suffix in FORM_SUFFIXES:
        if name.endswith(f"-{suffix}"):
            return name.rsplit(f"-{suffix}", 1)[0]
    return name


def parse_range(range_str):
    """Convert '3–5' or '3-5' to (3, 5), '5' to (5, 5)"""
    parts = re.split(r"[–-]", range_str)  # handles both dash types
    if len(parts) == 1:
        n = int(parts[0])
        return (n, n)
    return (int(parts[0]), int(parts[1]))


def merge_ranges(ranges):
    """Merge overlapping or adjacent ranges"""
    parsed = sorted([parse_range(r) for r in ranges])  # Sorts the level range tuples
    merged = []

    for start, end in parsed:
        if (
            not merged or start > merged[-1][1] + 1
        ):  # Do not merge levels if the current range does not overlap with the last merged one # noqa: E501
            merged.append((start, end))
        else:  # Merge ranges
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))

    # Convert back to strings
    return [str(start) if start == end else f"{start}–{end}" for start, end in merged]


def consolidate_by_location(subgroup):
    """Consolidate the same pokemon by location"""
    by_location = defaultdict(list)

    for _, row in subgroup.iterrows():
        by_location[row["Location"]].append(row["LevelRange"])

    output = []
    for location, levels in by_location.items():
        merged_levels = merge_ranges(levels)
        output.append((location, ", ".join(merged_levels)))

    return output
