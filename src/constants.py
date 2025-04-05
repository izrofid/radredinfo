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
