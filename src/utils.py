import streamlit as st
import paths
import json
import pandas as pd
from constants import METHOD_MAP
from collections import OrderedDict


# ---------------------
# Helper Functions
# ---------------------


def sanitize_method(raw_method):
    """Sanitizes the method name extracted from the encounter data for display"""
    return METHOD_MAP.get(raw_method)


def load_styles():
    """Loads css styles for use in streamlit"""
    st.html("<style>" + open(paths.styles).read() + "</style>")


@st.cache_data
def load_encounter_json():
    """Loads the encounter data and caches it"""
    with open(paths.encounters, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def load_sprite_lookup():
    return pd.read_csv(paths.sprites, index_col="Pokemon")["SpriteURL"].to_dict()


# ---------------------
# Encounter Functions
# ---------------------


def get_all_pokemon_names(encounters_json):
    """loops through the ecnounters data to return a sorted list of pokemon names"""

    names = set()  # Blank set to dedupe pokemon names

    for location_data in encounters_json.values():
        for method, entries in location_data.items():
            if isinstance(entries, list):
                for entry in entries:
                    # Handle raid format (dict with "Pokemon")
                    if isinstance(entry, dict) and "Pokemon" in entry:
                        names.add(entry["Pokemon"])
                    # Handle gift/trade string entries
                    elif isinstance(entry, str):
                        names.add(entry.strip())

    return sorted(names)


def get_encounters_for_pokemon(pokemon_name, encounter_data):
    results = []

    for location, methods in encounter_data.items():
        for method, entries in methods.items():
            method_sanitized = sanitize_method(method)

            if method_sanitized == "Raid":
                for entry in entries:
                    if isinstance(entry, dict) and "Pokemon" in entry:
                        if entry["Pokemon"].lower() == pokemon_name.lower():
                            results.append(
                                {
                                    "Location": location,
                                    "Method": "Raid",
                                    "LevelRange": f"{method.split()[0]} Star",
                                }
                            )

            elif isinstance(entries[0], dict):
                for entry in entries:
                    if (
                        "Pokemon" in entry
                        and entry["Pokemon"].lower() == pokemon_name.lower()
                    ):
                        min_lvl = entry["MinLevel"]
                        max_lvl = entry["MaxLevel"]
                        level_range = (
                            f"{min_lvl}"
                            if min_lvl == max_lvl
                            else f"{min_lvl}-{max_lvl}"
                        )
                        results.append(
                            {
                                "Location": location,
                                "Method": method_sanitized,
                                "LevelRange": level_range,
                            }
                        )

            # gift/trade/etc. methods (strings) are skipped
    return results


def consolidate_day_night(encounter_list):
    # Loop through encounter list and change Day/Night to Walk
    for encounter in encounter_list:
        if encounter["Method"] in ["Day", "Night"]:
            encounter["Method"] = "Walk"

    # Dedeuplicates the list of dictionaries

    consolidated_encounter_list = list(
        OrderedDict((frozenset(item.items()), item) for item in encounter_list).values()
    )
    return consolidated_encounter_list


def add_pokemon_to_dict(complete_dict, pokemon, encounter_list):
    # updates a dictionary with pokemon, encounter_list key pairs
    complete_dict.update({pokemon: encounter_list})
    return complete_dict


def consolidate_encounters_by_pokemon(pokemon_names, encounters):
    complete_dict = {}
    for pokemon in pokemon_names:
        encounter_list = get_encounters_for_pokemon(pokemon, encounters)
        day_night_list = consolidate_day_night(encounter_list)
        complete_dict = add_pokemon_to_dict(complete_dict, pokemon, day_night_list)
    return complete_dict
