"""Module providing helper functions"""

import re
import pandas as pd
import requests
from collections import defaultdict
from constants import FORM_SUFFIXES, SPRITE_FIXES


def prep_level_range(df):
    df["LevelRange"] = df.apply(
        lambda row: (
            str(row["MinLevel"])
            if row["MinLevel"] == row["MaxLevel"]
            else f"{row['MinLevel']}–{row['MaxLevel']}"
        ),
        axis=1,
    )
    return df


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
    levels = [lvl for lvl, _, _ in ranges]
    parsed = sorted([parse_range(r) for r in levels])  # Sorts the level range tuples
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
    """Consolidate the same Pokémon by (location, method) to support mixed encounters"""
    by_location_and_method = defaultdict(list)

    for _, row in subgroup.iterrows():
        key = (row["Location"], row["Method"])
        by_location_and_method[key].append(
            (row["LevelRange"], row["Method"], row["Star"])
        )

    output = []
    for (location, method), entries in by_location_and_method.items():
        if method == "Raid":
            stars = sorted({int(star) for _, _, star in entries if pd.notna(star)})
            val_string = ", ".join(
                f"{s}" for s in stars
            )  # just the star number, e.g. "5"
        else:
            val_string = ", ".join(merge_ranges(entries))  # e.g. "12–14"

        output.append((location, val_string, method))
    output.sort(key=lambda x: (x[0], "z" if x[2] == "Raid" else "a"))
    return output


def apply_common_filters(
    df,
    selected_pokemon,
    search_location,
    location_type,
    selected_method,
    selected_level_cap,
    methods,
):
    if selected_pokemon != "All":
        df = df[df["BasePokemon"] == selected_pokemon]

    if search_location != "All":
        df = df[df["Location"] == search_location]

    # if time_choice != "All":
    #     df = df[df["Time"] == time_choice]

    if selected_method == "All" and location_type == "Water":
        df = df[df["Method"].isin(methods[0])]

    elif selected_method == "All" and location_type == "Both":
        df = df[df["Method"].isin(methods[1])]

    elif selected_method == "All" and location_type == "Land":
        df = df[df["Method"].isin(methods[2])]

    else:
        df = df[df["Method"] == selected_method]

    if selected_level_cap != 0:
        df = df[df["MaxLevel"] <= selected_level_cap]

    return df


def get_pokemon_sprite(pokemon_name):
    corrected_name = SPRITE_FIXES.get(pokemon_name.lower(), pokemon_name.lower())
    url = f"https://pokeapi.co/api/v2/pokemon/{corrected_name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        sprite_url = data["sprites"]["front_default"]
        return sprite_url
    else:
        return "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png"
