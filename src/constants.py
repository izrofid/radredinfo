"""Module providing constant definitions"""

FORM_SUFFIXES = [
    "Alola",
    "Galar",
    "Hisui",
    "Paldea",
]

TIME_ICONS = {
    frozenset({"Day"}): "☀️",
    frozenset({"Night"}): "🌙",
    frozenset({"Day", "Night"}): "🌓",
    frozenset({"All"}): "🌓",
}

REQUIRED_FIELDS = ["Pokemon", "Location", "LevelRange", "Time", "Method"]

SPRITE_FIXES = {
    "aegislash": "aegislash-shield",
    "basculegion": "basculegion-male",
    "basculin": "basculin-red-striped",
    "basculin-blue": "basculin-blue-striped",
    "darmanitan-galar": "darmanitan-galar-standard",
    "eiscue": "eiscue-noice",
    "flabebe": "flabebe",
    "gourgeist-su": "gourgeist-super",
    "indeedee": "indeedee-male",
    "indeedee-f": "indeedee-female",
    "meloetta": "meloetta-pirouette",
    "mime-jr.": "mime-jr",
    "morpeko": "morpeko-full-belly",
    "mr.-mime-galar": "mr-mime-galar",
    "nidoranm": "nidoran-m",
    "oricorio": "oricorio-baile",
    "pumpkaboo": "pumpkaboo-average",
    "pumpkaboo-la": "pumpkaboo-large",
    "pumpkaboo-sm": "pumpkaboo-small",
    "pumpkaboo-su": "pumpkaboo-super",
    "shaymin": "shaymin-sky",
    "shellos-east": "shellos",
    "squawkabilly-g": "squawkabilly-green-plumage",
    "squawkabilly-w": "squawkabilly-white-plumage",
    "tatsugiri": "tatsugiri-curly",
    "toxtricity": "toxtricity-low-key",
    "type:-null": "type-null",
    "wishiwashi": "wishiwashi-school",
    "zygarde": "zygarde-complete",
}

METHOD_MAP = {
    "day encounters": "Day",
    "night encounters": "Night",
    "surf encounters": "Surf",
    "oldRod encounters": "Old Rod",
    "goodRod encounters": "Good Rod",
    "superRod encounters": "Super Rod",
    "1 star raid": "Raid",
    "2 star raid": "Raid",
    "3 star raid": "Raid",
    "4 star raid": "Raid",
    "5 star raid": "Raid",
    "6 star raid": "Raid",
    "gift pokemon": "Gift",
    "trade pokemon": "Trade",
    "roaming pokemon": "Roaming",
    "overworld pokemon": "Overworld",
}

METHOD_COLORS = {
    "Walk": "#2E8B57",  # SeaGreen
    "Day": "#ba8304",  # Gold
    "Night": "#483D8B",  # DarkSlateBlue
    "Surf": "#1a5feb",  # DodgerBlue
    "Old Rod": "#228a85",  # Firebrick
    "Good Rod": "#8B008B",  # DarkMagenta
    "Super Rod": "#4B0082",  # Indigo
    "Raid": "#9e2828",  # Dark Red
    "Game Corner": "#c95b94",  # Purple-pink
    "Gift": "#FF8C00",  # DarkOrange
    "Trade": "#20B2AA",  # LightSeaGreen
    "Roaming": "#A0522D",  # Sienna
    "Overworld": "#556B2F",  # DarkOliveGreen
}

FALLBACK_SPRITE = (
    "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png"
)
