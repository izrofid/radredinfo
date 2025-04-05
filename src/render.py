import streamlit as st


def _render_encounter_list(encounters):
    """Render a list of (location, level) tuples into HTML list items."""
    if not encounters:
        return "<p style='color: #888;'>—</p>"
    html = "<ul style='margin: 0.5em 0; padding-left: 1.2em;'>"
    for loc, lvl in encounters:
        html += f"<li><strong>{loc}</strong> — Level {lvl}</li>"
    html += "</ul>"
    return html


def _render_card(pokemon, content_html, time_icon=None):
    """Wraps content inside a styled card box with optional time icon."""
    icon_html = (
        f"""
        <div style="
            position: absolute;
            top: 0.5em;
            right: 0.7em;
            font-size: 1.3em;
            opacity: 0.8;
        ">{time_icon}</div>
        """
        if time_icon
        else ""
    )

    card_html = f"""
        {icon_html}
        <div style="background-color:#2b2b2b; border:1px solid #444; border-radius:6px;
                    padding:1.2em; margin-bottom:1.2em; box-shadow:0 4px 12px rgba(0,0,0,0.5);
                    color:#f0f0f0; font-family:'Segoe UI', sans-serif;">
            <h4 style="margin-bottom:0.6em; color:#ffffff; font-size:1em;">{pokemon}</h4>
            {content_html}
        </div>
    """
    return card_html


def render_single_column_card(pokemon, encounters, time_icon):
    encounter_list = _render_encounter_list(encounters)
    card = _render_card(pokemon, encounter_list, time_icon)
    st.markdown(card, unsafe_allow_html=True)


def render_dual_column_card(pokemon, day_encounters, night_encounters, time_icon):
    left = _render_encounter_list(day_encounters)
    right = _render_encounter_list(night_encounters)

    content = f"""
        <div style="display: flex; gap: 2em;">
            <div style="flex: 1;">
                <h5 style="margin: 0 0 0.5em;">☀️ Day</h5>{left}
            </div>
            <div style="width: 2px; background-color: #555;"></div>
            <div style="flex: 1;">
                <h5 style="margin: 0 0 0.5em;">🌙 Night</h5>{right}
            </div>
        </div>
    """
    card = _render_card(pokemon, content, time_icon)
    st.markdown(card, unsafe_allow_html=True)
