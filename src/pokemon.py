"""Module to display enconter data"""

import streamlit as st
import render as rn
import utils
from constants import METHOD_NAMES


# Load encounter data
encounters = utils.load_encounter_json()

# Variable definitions
pokemon_names = utils.get_all_pokemon_names(encounters)
location_names = list(encounters.keys())
pokemon_options = ["All"] + pokemon_names
location_options = ["All"] + location_names
method_options = ["All"] + METHOD_NAMES
list_of_pokemon = []

# Load styles
utils.load_styles()

# Show title
st.title("Radical Red Pokemon Locations")
st.markdown(
    "Search for a Pokémon or a Location to find where and at what levels it can be encountered."  # noqa: E501
)

# Two column layout
col1, col2 = st.columns(2)
with col1:
    selected_pokemon = st.selectbox("Search Pokémon", pokemon_options)
with col2:
    selected_location = st.selectbox("Choose Location", location_options)

col3, col4 = st.columns(2)
with col3:
    selected_method = st.selectbox("Choose Method", method_options)
with col4:
    selected_lvl_cap = st.selectbox("Choose Location", ["All", "Level 1", "Level 2"])

# Filtering
filtered_pokemon = set(pokemon_names)  # Start with all Pokémon

# Location filter
if selected_location != "All":
    location_pokemon = set(utils.get_pokemon_by_location(selected_location, encounters))
    filtered_pokemon = filtered_pokemon.intersection(location_pokemon)

# Pokémon name filter
if selected_pokemon != "All":
    filtered_pokemon = filtered_pokemon.intersection([selected_pokemon])

# Encounter method filter
if selected_method != "All":
    method_pokemon = set()
    combined_methods = {
        "Walk": ["Day", "Night"],
        "Water": ["Surf", "Old Rod", "Good Rod", "Super Rod"],
    }

    # Determine which methods to check for
    methods_to_check = []
    if selected_method in combined_methods:
        methods_to_check = combined_methods[selected_method]
    else:
        methods_to_check = [selected_method]

    for pokemon in filtered_pokemon:
        encounters_for_pokemon = utils.get_encounters_for_pokemon(pokemon, encounters)
        if any(
            encounter["Method"] in methods_to_check
            for encounter in encounters_for_pokemon
        ):
            method_pokemon.add(pokemon)

    filtered_pokemon = method_pokemon

# Level cap filter (placeholder implementation)
if selected_lvl_cap != "All":
    # Implement level cap filtering logic
    pass

# Sort the final list for display
list_of_pokemon = sorted(filtered_pokemon)

complete_dict = utils.consolidate_encounters_by_pokemon(list_of_pokemon, encounters)
if list_of_pokemon:
    st.html(rn.build_multiple_cards(complete_dict, selected_location, selected_method))
else:
    st.warning("No Encounters found. Try adjusting your search")
