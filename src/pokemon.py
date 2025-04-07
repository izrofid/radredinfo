"""Module to display enconter data"""

import streamlit as st
import render as rn
import utils


# Load encounter data
encounters = utils.load_encounter_json()

# Load styles
utils.load_styles()

# Show title
st.title("Radical Red Pokemon Locations")
st.markdown(
    "Search for a Pokémon or a Location to find where and at what levels it can be encountered."  # noqa: E501
)


selected_pokemon = st.selectbox(
    "Search Pokémon", utils.get_all_pokemon_names(encounters)
)


complete_dict = {}
pokemon_names = utils.get_all_pokemon_names(encounters)

complete_dict = utils.consolidate_encounters_by_pokemon(pokemon_names, encounters)

st.html(rn.build_multiple_cards(complete_dict))
# encounter_list = utils.get_encounters_for_pokemon(selected_pokemon, encounters)

# consolidated_list = utils.consolidate_day_night(encounter_list)

# st.html(rn.to_card(selected_pokemon, consolidated_list))
