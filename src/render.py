import streamlit as st
import pandas as pd
import paths
from constants import METHOD_COLORS


@st.cache_data
def load_sprite_lookup():
    return pd.read_csv(paths.sprites, index_col="Pokemon")["SpriteURL"].to_dict()


sprite_lookup = load_sprite_lookup()


def render_all_cards(card_html_list):
    full_html = "\n".join(card_html_list)
    st.html(full_html)


def build_fancy_card_html(pokemon, encounters, time_icon=""):

    sprite = f"<img src='{sprite_lookup.get(pokemon)}' class='sprite'>"
    rows_html = ""
    for loc, val, method in encounters:
        prefix = f"Level {val or '?'}" if method != "Raid" else f"{val or '?'} Star"
        color = METHOD_COLORS.get(method, "#555")
        loc_badge = f'<span class="loc-badge">{loc}</span>'
        range_badge = f'<span class="range-badge">{prefix}</span>'
        method_badge = f'<span class="method-badge" style="background-color:{color}">{method}</span>'

        rows_html += f"""
        <div class="data-row">
            <div class="data-item">{loc_badge}</div>
            <div class="data-item">{method_badge}</div>
            <div class="data-item">{range_badge}</div>
        </div>
        """

    return f"""
    <div class="card">
        <div class="card-header">
            <span class="left-header">
                {sprite}<span>{pokemon}</span>
            </span>
            <span class="time-icon">{time_icon}</span>
        </div>
        <div class="card-content">
            {rows_html}
        </div>
    </div>
    """
