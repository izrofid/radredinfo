import streamlit as st

# Dictionary lookup for time of day
time_icons = {
    frozenset({"Day"}): "☀️",
    frozenset({"Night"}): "🌙",
    frozenset({"Day", "Night"}): "🌓",
    frozenset({"All"}): "🌓", 
}

# Single Column Render
def render_single_column_card(pokemon, encounters, time_icon):
    encounter_list = ""
    for loc, lvl in encounters:
        encounter_list += f"<li><strong>{loc}</strong> — Level {lvl}</li>"

    st.markdown(f"""
        <div style="
            position: absolute;
            top: 0.5em;
            right: 0.7em;
            font-size: 1.3em;
            opacity: 0.8;
        ">{time_icon}</div>
        <div style="background-color:#2b2b2b; border:1px solid #444; border-radius:6px;
                    padding:1.2em; margin-bottom:1.2em; box-shadow:0 4px 12px rgba(0,0,0,0.5);
                    color:#f0f0f0; font-family:'Segoe UI', sans-serif;">
            <h4 style="margin-bottom:0.6em; color:#ffffff; font-size:1.2em;">{pokemon}</h4>
            <ul style="margin: 0.5em 0; padding-left: 1.2em;">{encounter_list}</ul>
        </div>
    """, unsafe_allow_html=True)

# Dual Column Render
def render_dual_column_card(pokemon, day_encounters, night_encounters, time_icon):
    def render(encounters):
        if not encounters:
            return "<p style='color: #888;'>—</p>"
        html = "<ul style='margin: 0.5em 0; padding-left: 1.2em;'>"
        for loc, lvl in encounters:
            html += f"<li><strong>{loc}</strong> — Level {lvl}</li>"
        html += "</ul>"
        return html

    left = render(day_encounters)
    right = render(night_encounters)

    st.markdown(f"""
         <div style="
            position: absolute;
            top: 0.5em;
            right: 0.7em;
            font-size: 1.3em;
            opacity: 0.8;
        ">{time_icon}</div>               
        <div style="background-color:#2b2b2b; border:1px solid #444; border-radius:6px;
                    padding:1.2em; margin-bottom:1.2em; box-shadow:0 4px 12px rgba(0,0,0,0.5);
                    color:#f0f0f0; font-family:'Segoe UI', sans-serif;">
            <h4 style="margin-bottom:1em; color:#ffffff; font-size:1.2em;">{pokemon}</h4>
            <div style="display: flex; gap: 2em;">
                <div style="flex: 1;">
                    <h5 style="margin: 0 0 0.5em;">☀️ Day</h5>{left}
                </div>
                <div style="width: 2px; background-color: #555;"></div>
                <div style="flex: 1;">
                    <h5 style="margin: 0 0 0.5em;">🌙 Night</h5>{right}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

