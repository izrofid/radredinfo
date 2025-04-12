import streamlit as st
import paths
import json
import pandas as pd
from constants import METHOD_MAP


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


@st.cache_data
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


@st.cache_data
def get_pokemon_types(pokemon_name):
    """Fetches the types of a given Pokémon."""
    # Look up pokemon name in paths.pokemon
    df = pd.read_csv(paths.rrtypes, index_col="Pokemon")

    if pokemon_name in df.index:
        try:
            types = df.loc[pokemon_name, ["Type 1", "Type 2"]].dropna().tolist()
            if len(types) == 0:
                # No type data found
                raise KeyError(f"No type data for Pokemon '{pokemon_name}'")
            elif len(types) == 1:
                # Only one type, duplicate it
                return [types[0], types[0]]
            else:
                return types
        except KeyError:
            # The DataFrame doesn't have Type1/Type2 columns
            raise KeyError(f"Type data columns not found for Pokemon '{pokemon_name}'")

    # If we get here, the Pokemon isn't in any of our databases
    raise KeyError(f"Pokemon '{pokemon_name}' not found in any type database.")


def get_pokemon_by_location(location, encounters_json):
    """Returns a sorted list of Pokémon names for a specific location."""

    names = set()

    location_data = encounters_json.get(location)
    if not location_data:
        return []

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

            if method_sanitized == "Gift":
                for entry in entries:
                    if isinstance(entry, dict) and "Pokemon" in entry:
                        if entry["Pokemon"].lower() == pokemon_name.lower():
                            results.append(
                                {
                                    "Location": location,
                                    "Method": "Gift",
                                    "LevelRange": entry["Type"],
                                }
                            )

            if isinstance(entries[0], dict) and method_sanitized not in [
                "Gift",
                "Raid",
            ]:
                for entry in entries:
                    if (
                        "Pokemon" in entry
                        and entry["Pokemon"].lower() == pokemon_name.lower()
                    ):
                        if not entry.get("MinLevel") or not entry.get("MaxLevel"):
                            level_range = "???"
                        else:
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
    result = []

    # First create a hash map to deduplicate identical encounters
    unique_encounters = {}

    for encounter in encounter_list:
        # Create a key that uniquely identifies this encounter
        encounter_key = (
            encounter["Location"],
            encounter["Method"],
            encounter["LevelRange"],
        )

        # Only keep one copy of each identical encounter
        unique_encounters[encounter_key] = encounter

    # Now we have deduped identical encounters, we can apply Day/Night consolidation
    # Group encounters by location and level range
    location_groups = {}
    for encounter in unique_encounters.values():
        key = (encounter["Location"], encounter["LevelRange"])
        if key not in location_groups:
            location_groups[key] = []
        location_groups[key].append(encounter)

    # Process each location group
    for encounters in location_groups.values():
        methods = {e["Method"] for e in encounters}

        # If both Day and Night exist in this location with same level range
        if "Day" in methods and "Night" in methods:
            # Create a consolidated Walk encounter
            walk_encounter = {
                "Location": encounters[0]["Location"],
                "Method": "Walk",
                "LevelRange": encounters[0]["LevelRange"],
            }

            # Add the consolidated walk encounter
            result.append(walk_encounter)

            # Add all other encounters that aren't Day or Night
            for e in encounters:
                if e["Method"] not in ["Day", "Night"]:
                    result.append(e)
        else:
            # No consolidation needed, add all unique encounters
            result.extend(encounters)

    return result


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
