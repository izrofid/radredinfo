import pandas as pd
import streamlit as st
from forms import strip_form_suffix

water_methods = {"Surf", "Old Rod", "Good Rod", "Super Rod"}


# Load data
df = pd.read_csv("flat_encounters.csv")
pokemon_df = pd.read_csv("pokemon.csv")
pokemon_names = sorted(pokemon_df["Name"].unique())



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
    method_options = sorted(df["Method"].unique())
    selected_method = st.selectbox("Method", method_options, index=method_options.index("Grass"))

with col4:
    if selected_method in water_methods:
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

# Filter data
df["BasePokemon"] = df["Pokemon"].apply(strip_form_suffix)
filtered = df.copy()

if selected_pokemon != "All":
    filtered = filtered[filtered["BasePokemon"] == selected_pokemon]

if search_location != "All":
    filtered = filtered[filtered["Location"] == search_location]

if time_choice != "All":
    filtered = filtered[filtered["Time"] == time_choice]

if selected_method != "All":
    filtered = filtered[filtered["Method"] == selected_method]

# Keep only the essential display columns
filtered = filtered[["Pokemon", "Location", "LevelRange", "Time", "Method"]].dropna()


# Check if any results
if filtered.empty:
    st.warning("No encounters found. Try adjusting your search.")
# Show Results

elif time_choice == "All" and selected_method not in water_methods:
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
