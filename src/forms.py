FORM_SUFFIXES = [
    "Alola",
    "Galar",
    "Hisuian",
    "Paldea",
]

def strip_form_suffix(name):
    for suffix in FORM_SUFFIXES:
        if name.endswith(f"-{suffix}"):
            return name.rsplit(f"-{suffix}", 1)[0]
    return name