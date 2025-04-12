"""Module to display enconter data"""

import streamlit as st
import render as rn
import utils
from constants import METHOD_NAMES, POKEMON_TYPES, DEBUG


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
    selected_type = st.selectbox("Type", ["All"] + POKEMON_TYPES, index=0)


# Filtering
filtered_pokemon = set(pokemon_names)  # Start with all Pokémon

# Pokémon name filter (always apply this first as it's the most specific)
if selected_pokemon != "All":
    filtered_pokemon = filtered_pokemon.intersection([selected_pokemon])


# Define a function to check if a pokemon meets all selected criteria
def meets_criteria(pokemon):
    encounters_for_pokemon = utils.get_encounters_for_pokemon(pokemon, encounters)
    pokemon_types = utils.get_pokemon_types(pokemon)

    # Check type criteria first (if applied)
    if selected_type != "All" and selected_type not in pokemon_types:
        return False

    # Apply location filter if needed
    if selected_location != "All":
        location_matches = [
            e for e in encounters_for_pokemon if e["Location"] == selected_location
        ]
        if not location_matches:
            return False

        # If only location is selected, we've found at least one match
        if selected_method == "All":
            return True

        # If location and method are both selected, check the subset of location matches
        encounters_to_check = location_matches
    else:
        # If only method is selected, check all encounters
        encounters_to_check = encounters_for_pokemon

    # Apply method filter if needed
    if selected_method != "All":
        combined_methods = {
            "Walk": ["Day", "Night", "Walk"],  # Include "Walk" for consolidated entries
            "Water": ["Surf", "Old Rod", "Good Rod", "Super Rod"],
        }

        methods_to_check = combined_methods.get(selected_method, [selected_method])

        # Check if any encounter matches the method criteria
        if not any(e["Method"] in methods_to_check for e in encounters_to_check):
            return False

    return True


# Apply all filters at once using the criteria function
has_filter_selected = any(
    [selected_location != "All", selected_method != "All", selected_type != "All"]
)

if has_filter_selected:
    filtered_pokemon = {
        pokemon for pokemon in filtered_pokemon if meets_criteria(pokemon)
    }

if DEBUG:
    debug_info = st.expander("Debug Information", expanded=False)
    with debug_info:
        st.write(
            f"Filter criteria: Location: {selected_location}, Method: {selected_method}, Type: {selected_type}"
        )
        st.write(f"Found {len(filtered_pokemon)} Pokémon matching criteria")

        # Show a few example Pokémon and their types
        if list_of_pokemon:
            sample_size = min(5, len(list_of_pokemon))
            st.write("#### Sample Pokémon Types:")
            for pokemon in list_of_pokemon[:sample_size]:
                types = utils.get_pokemon_types(pokemon)
                st.write(f"{pokemon}: {types}")

# Sort the final list for display
list_of_pokemon = sorted(filtered_pokemon)

# Sort the final list for display
list_of_pokemon = sorted(filtered_pokemon)

complete_dict = utils.consolidate_encounters_by_pokemon(list_of_pokemon, encounters)
if list_of_pokemon:
    st.html(rn.build_multiple_cards(complete_dict, selected_location, selected_method))
else:
    st.warning("No Encounters found. Try adjusting your search")
