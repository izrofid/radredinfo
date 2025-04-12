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


def to_card(pokemon, encounter_list, selected_location="All", selected_method="All"):
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
        if selected_location != "All" and location != selected_location:
            continue
        if selected_method != "All":
            if selected_method == "Walk" and encounter["Method"] not in [
                "Day",
                "Night",
                "Walk",
            ]:
                continue
            if selected_method == "Day" and encounter["Method"] not in ["Day", "Walk"]:
                continue
            if selected_method == "Night" and encounter["Method"] not in [
                "Night",
                "Walk",
            ]:
                continue
            elif selected_method == "Water" and encounter["Method"] not in [
                "Old Rod",
                "Good Rod",
                "Super Rod",
                "Surf",
            ]:
                continue
            elif (
                selected_method != "Walk"
                and selected_method != "Water"
                and selected_method != "Day"
                and selected_method != "Night"
                and encounter["Method"] != selected_method
            ):
                continue
        level_range = encounter["LevelRange"]

        # Prepare a range value based on method

        if method == "Raid":
            range_value = f"{level_range or '?'} Star Raid"
        if method == "Gift":
            range_value = f"{level_range or '?'}"
        if method not in ["Raid", "Gift"]:
            range_value = f"Level {level_range or '?'}"

        # Grab color based on method
        color = constants.METHOD_COLORS.get(method, "#555")

        location_badge = f'<span class="loc-badge">{location}</span>'
        method_badge = f'<span class="method-badge" style="background-color:{color}">{method}</span>'
        range_badge = f'<span class="range-badge">{range_value}</span>'

        # Append to card content
        card_content += build_card_content(location_badge, method_badge, range_badge)

    return build_card(sprite, pokemon, card_content)


def build_multiple_cards(complete_dict, selected_location="All", selected_method="All"):
    all_cards = ""
    for pokemon in complete_dict:
        data_for_card = to_card(
            pokemon, complete_dict[pokemon], selected_location, selected_method
        )
        all_cards += data_for_card
    return all_cards
