"""Module to render pokemon data as html cards"""

import utils
import constants

# Create a sprite look up to grab pokemon sprites
sprite_lookup = utils.load_sprite_lookup()


def get_sprite(pokemon, sprite_lookup):
    """
    Returns the HTML img tag for a given Pokémon.
    If the Pokémon is not found in sprite_lookup, uses the fallback URL.
    """
    sprite_url = sprite_lookup.get(pokemon)
    return f"<img src='{sprite_url}' class='sprite'>"


def build_card_content(location_badge, method_badge, range_badge):
    """
    Returns the content that goes within the card
    Contains location, method and levels/stars
    """

    return f"""
    <div class="data-row">
        <div class="data-item">{location_badge}</div>
        <div class="data-item">{method_badge}</div>
        <div class="data-item">{range_badge}</div>
    </div>
    """


def build_card(sprite, pokemon, content):
    """
    Builds the full card
    Adds header with name and sprite
    Adds all encounters to it
    """

    return f"""
    <div class="card">
        <div class="card-header">
            <span>
                {sprite}<span>{pokemon}</span>
            </span>
        </div>
        <div class="card-content">
            {content}
        </div>
    </div>
    """


def to_card(pokemon, encounter_list):
    """
    Function that turns encounters into cards for display
    Takes pokemon name (str) and encounter list (dict)
    Returns html with the full card for display
    """

    sprite = get_sprite(pokemon, sprite_lookup)  # Grab sprite for pokemon as img
    card_content = ""  # Initialize rows_html for the encounter data

    for encounter in encounter_list:
        # Grab location, method and level_range for each encounter
        location = encounter["Location"]
        method = encounter["Method"]
        level_range = encounter["LevelRange"]

        # Prepare a range value based on method
        range_value = (
            f"Level {level_range or '?'}"
            if method != "Raid"
            else f"{level_range or '?'} Raid"
        )

        # Grab color based on method
        color = constants.METHOD_COLORS.get(method, "#555")

        location_badge = f'<span class="loc-badge">{location}</span>'
        range_badge = f'<span class="range-badge">{range_value}</span>'
        method_badge = f'<span class="method-badge" style="background-color:{color}">{method}</span>'

        # Append to card content
        card_content += build_card_content(location_badge, range_badge, method_badge)

    return build_card(sprite, pokemon, card_content)
