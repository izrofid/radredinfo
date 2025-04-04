import pandas as pd
import streamlit as st
from forms import strip_form_suffix
import render as rn

# Load data
df = pd.read_csv("flat_encounters.csv")

pokemon_df = pd.read_csv("pokemondata.csv")
pokemon_names = sorted(pokemon_df["Name"].unique())

levelcap_df= pd.read_csv("levelcap.csv", keep_default_na=False)
levelcap_df.columns = levelcap_df.columns.str.strip()
levelcap_df['Level Cap'] = levelcap_df['Level Cap'].astype(int)
level_caps = levelcap_df.set_index('Point')['Level Cap'].to_dict()

# Prepare level range as a combined string
df["LevelRange"] = df["MinLevel"].astype(str) + "–" + df["MaxLevel"].astype(str)

# Page title
st.title("Radical Red Pokemon Locations")

st.markdown("Search for a Pokémon or a Location to find where and at what levels it can be encountered.")

# Search inputs
col1, col2 = st.columns(2)

with col1:
    selected_pokemon = st.selectbox("Pokémon", ["All"] + pokemon_names)

with col2:
    search_location = st.selectbox("Location", ["All"] + sorted(df["Location"].unique()))

time_icons = {
    "All": "🌓 All",
    "Day": "☀️ Day",
    "Night": "🌙 Night"
}

col3, col4 = st.columns(2)


with col3:
    location_type = st.radio(
        "Land or Water?",
        options=["Land", "Water", "Both"],
        format_func=lambda t: {"Land": "🗾 Land", "Water": "💧 Water", "Both": "🌏 Both"}[t],
        horizontal=True
    )

with col4:
    if location_type == "Water":
        time_choice = st.radio(
            "Time of Day",
            options=["All"],
            format_func=lambda t: {"All": "🌓 All"}[t],
            horizontal=True
        )
       
    else:
        time_choice = st.radio(
            "Time of Day",
            options=["All", "Day", "Night"],
            format_func=lambda t: {"All": "🌓 All", "Day": "☀️ Day", "Night": "🌙 Night"}[t],
            horizontal=True
        )

df["Method"] = df["Method"].str.strip()
water_methods = sorted([m for m in df["Method"].unique() if m != "Grass"])
all_methods = sorted([m for m in df["Method"].unique()])
method_options = ["All"] + water_methods
all_method_options = ["All"] + all_methods

col5, col6 = st.columns(2)

with col5:
    if location_type == "Land":
        selected_method = st.selectbox("Method", "Grass")
    elif location_type == "Water":
        selected_method = st.selectbox("Method", method_options, index=0)
    else:
        selected_method = st.selectbox("Method", all_method_options, index=0)

with col6:
    selected_label = st.selectbox("Level Cap", list(level_caps.keys()))
    selected_level_cap = level_caps[selected_label]


# Filter data
df["BasePokemon"] = df["Pokemon"].apply(strip_form_suffix)
filtered = df.copy()

if selected_pokemon != "All":
    filtered = filtered[filtered["BasePokemon"] == selected_pokemon]

if search_location != "All":
    filtered = filtered[filtered["Location"] == search_location]

if time_choice != "All":
    filtered = filtered[filtered["Time"] == time_choice]

if selected_method == "All" and location_type == "Water":
    filtered = filtered[filtered["Method"].isin(water_methods)]
elif selected_method == "All" and location_type =="Both":
    filtered = filtered[filtered["Method"].isin(all_methods)]
else:
    filtered = filtered[filtered["Method"] == selected_method]

if selected_level_cap != 0:
    filtered = filtered[filtered["MaxLevel"] <= selected_level_cap]



# Keep only the essential display columns
filtered = filtered[["Pokemon", "Location", "LevelRange", "Time", "Method"]].dropna()


# Check if any results
if filtered.empty:
    st.warning("No encounters found. Try adjusting your search.")

# Show Results
grouped = filtered.groupby("Pokemon") #Group by pokemon to consolidate encounters

for pokemon, group in grouped:
    times = set(group["Time"].unique())

    # When Day/Night Encounters exist
    if times == {"Day","Night"}:
        #Makes list of day encounters with location/levels
        day_encounters = list(zip(
            group[group["Time"] == "Day"]["Location"],
            group[group["Time"] == "Day"]["LevelRange"]
        ))
        # Same for night
        night_encounters = list(zip(
            group[group["Time"] == "Night"]["Location"],
            group[group["Time"] == "Night"]["LevelRange"]
        ))
        # Render using dual column layout
        time_icon = rn.time_icons.get(frozenset(times), "")
        rn.render_dual_column_card(pokemon, day_encounters, night_encounters, time_icon)
    
    # When both day and night encounters don't exist
    else:
        encounters = list(zip(
            group["Location"],
            group["LevelRange"]
        ))
        # Render using single column layout
        time_icon = rn.time_icons.get(frozenset(times), "")
        rn.render_single_column_card(pokemon, encounters, time_icon)