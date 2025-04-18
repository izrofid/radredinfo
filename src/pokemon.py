"""Main module containing code for the webapp display"""

import pandas as pd
import streamlit as st
import render as rn
import paths
from utils import (
    strip_form_suffix,
    consolidate_by_location,
    apply_common_filters,
    prep_level_range,
)

from constants import TIME_ICONS, REQUIRED_FIELDS

# Page Config
st.markdown("<style>" + open(paths.styles).read() + "</style>", unsafe_allow_html=True)
# Load data
df = pd.read_csv(paths.encounters)


pokemon_df = pd.read_csv(paths.pokemon)
pokemon_names = sorted(pokemon_df["Name"].unique())

levelcap_df = pd.read_csv(paths.levels, keep_default_na=False)
levelcap_df.columns = levelcap_df.columns.str.strip()
levelcap_df["Level Cap"] = levelcap_df["Level Cap"].astype(int)
level_caps = levelcap_df.set_index("Point")["Level Cap"].to_dict()


# Prepare level range as a combined string
df = prep_level_range(df)


# Page title
st.title("Radical Red Pokemon Locations")

st.markdown(
    "Search for a Pokémon or a Location to find where and at what levels it can be encountered."  # noqa: E501
)

# Search inputs
col1, col2 = st.columns(2)

with col1:
    selected_pokemon = st.selectbox("Pokémon", ["All"] + pokemon_names)

with col2:
    search_location = st.selectbox(
        "Location", ["All"] + sorted(df["Location"].unique())
    )

time_icons = {"All": "🌓 All", "Day": "☀️ Day", "Night": "🌙 Night"}

col3, col4 = st.columns(2)


with col3:
    location_type = st.radio(
        "Land or Water?",
        options=["Both", "Land", "Water"],
        format_func=lambda t: {
            "Both": "🌏 Both",
            "Land": "🗾 Land",
            "Water": "💧 Water",
        }[t],
        horizontal=True,
    )

with col4:
    if location_type == "Water":
        time_choice = st.radio(
            "Time of Day",
            options=["All"],
            format_func=lambda t: {"All": "🌓 All"}[t],
            horizontal=True,
        )

    else:
        time_choice = st.radio(
            "Time of Day",
            options=["All", "Day", "Night"],
            format_func=lambda t: {
                "All": "🌓 All",
                "Day": "☀️ Day",
                "Night": "🌙 Night",
            }[t],
            horizontal=True,
        )

df["Method"] = df["Method"].str.strip()
land_methods = ["Grass", "Game Corner", "Raid"]
land_options = ["All"] + land_methods
water_methods = sorted([m for m in df["Method"].unique() if m not in land_methods])
all_methods = sorted(df["Method"].unique())
water_options = ["All"] + land_methods + water_methods
method_options = ["All"] + all_methods

methods = [water_methods, all_methods, land_methods]

col5, col6 = st.columns(2)

with col5:
    if location_type == "Land":
        selected_method = st.selectbox("Method", land_options, index=0)
    elif location_type == "Water":
        selected_method = st.selectbox("Method", water_options, index=0)
    else:
        selected_method = st.selectbox("Method", method_options, index=0)

with col6:
    selected_label = st.selectbox("Level Cap", list(level_caps.keys()))
    selected_level_cap = level_caps[selected_label]


# Filter data
df["BasePokemon"] = df["Pokemon"].apply(strip_form_suffix)
filtered = df.copy()

filtered = apply_common_filters(
    filtered,
    selected_pokemon,
    search_location,
    location_type,
    selected_method,
    selected_level_cap,
    methods,
)

# Keep only the essential display columns
filtered = filtered.dropna(subset=REQUIRED_FIELDS)

# Check if any results
if filtered.empty:
    st.warning("No encounters found. Try adjusting your search.")

# Show Results
grouped = filtered.groupby("Pokemon")

card_html_list = []


def add_card(encounters, label):
    if not encounters:
        return
    time_icon = TIME_ICONS.get(frozenset({label}), "")
    card_html = rn.build_fancy_card_html(pokemon, encounters, time_icon)
    card_html_list.append(card_html)


for pokemon, group in grouped:
    times = set(group["Time"].unique())

    # Break up group by time
    day_group = group[group["Time"] == "Day"]
    night_group = group[group["Time"] == "Night"]
    any_group = group[group["Time"] == "All"]

    # If both day and night encounters exist
    day_locs = set(day_group["Location"])
    night_locs = set(night_group["Location"])
    both_locs = day_locs & night_locs

    # Create both_group to store those
    both_group = pd.concat(
        [
            day_group[day_group["Location"].isin(both_locs)],
            night_group[night_group["Location"].isin(both_locs)],
        ]
    )

    # Remove these from day and night groups
    day_group = day_group[~day_group["Location"].isin(both_locs)]
    night_group = night_group[~night_group["Location"].isin(both_locs)]

    # Combine any_group with both_group to create all_group
    all_group = pd.concat([any_group, both_group], ignore_index=True)

    # Turn into encounter lists
    day_encounters = consolidate_by_location(day_group)
    night_encounters = consolidate_by_location(night_group)
    all_encounters = consolidate_by_location(all_group)
    both_encounters = consolidate_by_location(both_group)

    if time_choice == "All":
        if both_encounters or all_encounters:
            usable = all_encounters if all_encounters else both_encounters
            add_card(usable, "All")

        if day_encounters:
            add_card(day_encounters, "Day")

        if night_encounters:
            add_card(night_encounters, "Night")
    else:
        # Day/Night filter
        if time_choice == "Day":
            if day_encounters:
                add_card(day_encounters, "Day")

            if both_encounters or all_encounters:
                usable = all_encounters if all_encounters else both_encounters
                add_card(usable, "All")

        elif time_choice == "Night":
            if night_encounters:
                add_card(night_encounters, "Night")

            if both_encounters or all_encounters:
                usable = all_encounters if all_encounters else both_encounters
                add_card(usable, "All")

if card_html_list:
    rn.render_all_cards(card_html_list)
