"""Main module containing code for the webapp display"""

import pandas as pd
import streamlit as st
import render as rn
import paths
from utils import strip_form_suffix, consolidate_by_location, apply_common_filters
from constants import TIME_ICONS


# Load data
df = pd.read_csv(paths.encounters)
raid_df = pd.read_csv(paths.raids)
levelcap_df = pd.read_csv(paths.levels, keep_default_na=False)
pokemon_df = pd.read_csv(paths.pokemon)

# Process Data
pokemon_names = sorted(pokemon_df["Name"].unique())
levelcap_df.columns = levelcap_df.columns.str.strip()
levelcap_df["Level Cap"] = levelcap_df["Level Cap"].astype(int)
level_caps = levelcap_df.set_index("Point")["Level Cap"].to_dict()

# Prepare level range as a combined string
df["LevelRange"] = df.apply(
    lambda row: (
        str(row["MinLevel"])
        if row["MinLevel"] == row["MaxLevel"]
        else f"{row['MinLevel']}–{row['MaxLevel']}"
    ),
    axis=1,
)

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
land_methods = ["Grass", "Game Corner"]
land_options = ["All"] + land_methods
water_methods = sorted([m for m in df["Method"].unique() if m not in land_methods])
all_methods = sorted(df["Method"].unique())
water_options = ["All"] + land_methods + water_methods
method_options = ["All"] + all_methods

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
filtered_raid_df = raid_df.copy()

filtered = apply_common_filters(filtered, selected_pokemon, search_location)
if location_type != "Water":
    filtered_raid_df = apply_common_filters(
        filtered_raid_df, selected_pokemon, search_location
    )
else:
    filtered_raid_df = pd.DataFrame(columns=raid_df.columns)

# if time_choice != "All":
#     filtered = filtered[filtered["Time"] == time_choice]

if selected_method == "All" and location_type == "Water":
    filtered = filtered[filtered["Method"].isin(water_methods)]
elif selected_method == "All" and location_type == "Both":
    filtered = filtered[filtered["Method"].isin(all_methods)]
elif selected_method == "All" and location_type == "Land":
    filtered = filtered[filtered["Method"].isin(land_methods)]
else:
    filtered = filtered[filtered["Method"] == selected_method]

if selected_level_cap != 0:
    filtered = filtered[filtered["MaxLevel"] <= selected_level_cap]


# Keep only the essential display columns
filtered = filtered[["Pokemon", "Location", "LevelRange", "Time", "Method"]].dropna()

# Check if any results
if filtered.empty and filtered_raid_df.empty:
    st.warning("No encounters found. Try adjusting your search.")

# Show Results
wild_pokemon = set(filtered["Pokemon"].unique())
raid_pokemon = set(filtered_raid_df["Pokemon"].unique())
all_pokemon = sorted(wild_pokemon | raid_pokemon)  # Union of both

# Loop to go through each pokemon
for pokemon in all_pokemon:
    group = filtered[filtered["Pokemon"] == pokemon]
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
    both_encounters = consolidate_by_location(both_group)
    all_encounters = consolidate_by_location(all_group)

    # Make encounter list for raids
    raid_entries = filtered_raid_df[filtered_raid_df["Pokemon"] == pokemon]
    raid_encounters = [
        (row["Location"], f'{int(row["Star"])}★ Raid')
        for _, row in raid_entries.iterrows()
    ]

    if time_choice == "All":
        # All encounters (combined card, dual layout if needed)
        if both_encounters or all_encounters:
            time_icon = TIME_ICONS.get(frozenset({"All"}), "")
            rn.render_single_column_card(
                pokemon, both_encounters + all_encounters + both_encounters, time_icon
            )

        if day_encounters:
            time_icon = TIME_ICONS.get(frozenset({"Day"}), "")
            rn.render_single_column_card(pokemon, day_encounters, time_icon)

        if night_encounters:
            time_icon = TIME_ICONS.get(frozenset({"Night"}), "")
            rn.render_single_column_card(pokemon, night_encounters, time_icon)

        if raid_encounters and not (both_encounters or all_encounters):
            time_icon = TIME_ICONS.get(frozenset({"All"}), "")
            rn.render_single_column_card(pokemon, raid_encounters, time_icon)

    else:
        # Day/Night filter
        if time_choice == "Day":
            if day_encounters:
                time_icon = TIME_ICONS.get(frozenset({"Day"}), "")
                rn.render_single_column_card(pokemon, day_encounters, time_icon)

            if both_encounters or all_encounters:
                time_icon = TIME_ICONS.get(frozenset({"All"}), "")
                rn.render_single_column_card(
                    pokemon,
                    both_encounters + all_encounters + both_encounters,
                    time_icon,
                )

            if raid_encounters and not (both_encounters or all_encounters):
                time_icon = TIME_ICONS.get(frozenset({"All"}), "")
                rn.render_single_column_card(pokemon, raid_encounters, time_icon)

        elif time_choice == "Night":
            if night_encounters:
                time_icon = TIME_ICONS.get(frozenset({"Night"}), "")
                rn.render_single_column_card(pokemon, night_encounters, time_icon)
            if both_encounters or all_encounters:
                time_icon = TIME_ICONS.get(frozenset({"All"}), "")
                rn.render_single_column_card(
                    pokemon,
                    both_encounters + all_encounters + both_encounters,
                    time_icon,
                )
            if raid_encounters and not (both_encounters or all_encounters):
                time_icon = TIME_ICONS.get(frozenset({"All"}), "")
                rn.render_single_column_card(pokemon, raid_encounters, time_icon)
