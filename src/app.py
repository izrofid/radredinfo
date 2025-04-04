import pandas as pd
import streamlit as st
from forms import strip_form_suffix

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

elif time_choice == "All" and selected_method not in method_options:
    # 🌓 COMBINED LAYOUT
    # 1. Group Day and Night separately
    day_grouped = (
        filtered[filtered["Time"] == "Day"]
        .groupby("Pokemon", as_index=False)
        .apply(lambda x: pd.Series({
            "DayEncounters": list(zip(x["Location"], x["LevelRange"]))
        }))
        .reset_index(drop=True)
    )

    night_grouped = (
        filtered[filtered["Time"] == "Night"]
        .groupby("Pokemon", as_index=False)
        .apply(lambda x: pd.Series({
            "NightEncounters": list(zip(x["Location"], x["LevelRange"]))
        }))
        .reset_index(drop=True)
    )


    all_grouped = (
        filtered[filtered["Time"] == "All"]
        .groupby("Pokemon", as_index=False)
        .apply(lambda x: pd.Series({
            "NightEncounters": list(zip(x["Location"], x["LevelRange"]))
        }))
        .reset_index(drop=True)
    )

    grouped = pd.merge(day_grouped, night_grouped, on="Pokemon", how="outer").fillna("")


    for _, row in grouped.iterrows():
        pokemon = row["Pokemon"]
        day_list = row.get("DayEncounters", [])
        night_list = row.get("NightEncounters", [])

        # HTML for each encounter list
        def render_encounter_list(encounters):
            if not encounters:
                return "<p style='color: #888;'>—</p>"
            html = "<ul style='margin: 0.5em 0; padding-left: 1.2em;'>"
            for loc, lvl in encounters:
                html += f"<li><strong>{loc}</strong> — Level {lvl}</li>"
            html += "</ul>"
            return html

        left = render_encounter_list(day_list)
        right = render_encounter_list(night_list)

        st.markdown(f"""
            <div style="
                background-color: #2b2b2b;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 1.2em;
                margin-bottom: 1.2em;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
                color: #f0f0f0;
                font-family: 'Segoe UI', sans-serif;
            ">
                <h4 style="margin-bottom: 1em; color: #ffffff; font-size: 1.2em;">{pokemon}</h4>
                <div style="display: flex; gap: 2em;">
                    <div style="flex: 1;">
                        <h5 style="margin: 0 0 0.5em;">☀️ Day</h5>
                        {left}
                    </div>
                    <div style="width: 2px; background-color: #555;"></div>
                    <div style="flex: 1;">
                        <h5 style="margin: 0 0 0.5em;">🌙 Night</h5>
                        {right}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:

    # Group by Pokémon to consolidate encounters
    grouped = (
        filtered.groupby("Pokemon")
        .apply(lambda x: list(zip(x["Location"], x["LevelRange"])))
        .reset_index(name="Encounters")
    )

    # Render cards
    for _, row in grouped.iterrows():
        pokemon = row["Pokemon"]
        encounters = row["Encounters"]

        encounter_list = ""
        for loc, lvl in encounters:
            encounter_list += f"<li><strong>{loc}</strong> — Level {lvl}</li>"

        st.markdown(f"""
            <div style="
                background-color: #2b2b2b;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 1.2em;
                margin-bottom: 1.2em;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
                color: #f0f0f0;
                font-family: 'Segoe UI', sans-serif;
            ">
                <h4 style="margin-bottom: 0.6em; color: #ffffff; font-size: 1.2em;">{pokemon}</h4>
                <ul style="margin: 0.5em 0; padding-left: 1.2em; list-style-type: disc;">
                    {encounter_list}
                </ul>
            </div>
        """, unsafe_allow_html=True)
