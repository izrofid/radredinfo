"""Module providing constant definitions"""

FORM_SUFFIXES = [
    "Alola",
    "Galar",
    "Hisui",
    "Paldea",
]

METHOD_COLORS = {
    "Grass": "#3e7a38",
    "Surf": "#6390F0",
    "Old Rod": "#B8A038",
    "Good Rod": "#A040A0",
    "Super Rod": "#705898",
    "Raid": "#9e2828",
    "Game Corner": "#c95b94",
}

TIME_ICONS = {
    frozenset({"Day"}): "☀️",
    frozenset({"Night"}): "🌙",
    frozenset({"Day", "Night"}): "🌓",
    frozenset({"All"}): "🌓",
}

REQUIRED_FIELDS = ["Pokemon", "Location", "LevelRange", "Time", "Method"]

SPRITE_FIXES = {
    'aegislash': 'aegislash-shield',
    'basculegion': 'basculegion-male',
    'basculin': 'basculin-red-striped',
    'basculin-blue': 'basculin-blue-striped',
    'darmanitan-galar': 'darmanitan-galar-standard',
    'eiscue': 'eiscue-noice',
    'flabebe': 'flabebe',
    'gourgeist-su': 'gourgeist-super',
    'indeedee': 'indeedee-male',
    'indeedee-f': 'indeedee-female',
    'meloetta': 'meloetta-pirouette',
    'mime-jr.': 'mime-jr',
    'morpeko': 'morpeko-full-belly',
    'mr.-mime-galar': 'mr-mime-galar',
    'nidoranm': 'nidoran-m',
    'oricorio': 'oricorio-baile',
    'pumpkaboo': 'pumpkaboo-average',
    'pumpkaboo-la': 'pumpkaboo-large',
    'pumpkaboo-sm': 'pumpkaboo-small',
    'pumpkaboo-su': 'pumpkaboo-super',
    'shaymin': 'shaymin-sky',
    'shellos-east': 'shellos',
    'squawkabilly-g': 'squawkabilly-green-plumage',
    'squawkabilly-w': 'squawkabilly-white-plumage',
    'tatsugiri': 'tatsugiri-curly',
    'toxtricity': 'toxtricity-low-key',
    'type:-null': 'type-null',
    'wishiwashi': 'wishiwashi-school',
    'zygarde': 'zygarde-complete'
}
