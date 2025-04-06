import json

with open("structured_encounters.json", "r", encoding="utf-8") as f:
    encounters = json.load(f)


def list_methods(location_name):
    return list(encounters.get(location_name, {}).keys())


def get_pokemon_at_location(location_name):
    methods = encounters.get(location_name, {})
    pokemon = []

    for method, entries in methods.items():
        if isinstance(entries, list):
            for entry in entries:
                if isinstance(entry, dict) and "Pokemon" in entry:
                    pokemon.append(entry["Pokemon"])
                elif isinstance(entry, str):  # fallback for unstructured
                    pokemon.append(entry.strip())
    return sorted(set(pokemon))


def get_raids_at_location(location_name):
    methods = encounters.get(location_name, {})
    raids = {}

    for method, entries in methods.items():
        if "raid" in method.lower():
            raids[method] = []
            for entry in entries:
                if isinstance(entry, dict):
                    raids[method].append(
                        {
                            "Pokemon": entry["Pokemon"],
                            "Rewards": entry.get("Rewards", []),
                        }
                    )
    return raids


def find_pokemon_locations(pokemon_name):
    matches = []

    for location, methods in encounters.items():
        for method, entries in methods.items():
            for entry in entries:
                if (
                    isinstance(entry, dict)
                    and entry.get("Pokemon", "").lower() == pokemon_name.lower()
                ):
                    matches.append((location, method, entry))
                elif isinstance(entry, str) and pokemon_name.lower() in entry.lower():
                    matches.append((location, method, entry))
    return matches


def list_all_locations():
    return sorted(encounters.keys())


if __name__ == "__main__":
    print("All methods at Route 2:", list_methods("Route 2"))
    print("All Pokémon at Route 2:", get_pokemon_at_location("Route 2"))

    print("\nWhere is Bidoof?")
    for loc, method, entry in find_pokemon_locations("Bidoof"):
        print(f"{loc} - {method}: {entry}")
