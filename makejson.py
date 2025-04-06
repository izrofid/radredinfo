import ast
import json
import re


# -----------------------
# 📦 Encounter parser
# -----------------------
def parse_encounter(line):
    match = re.match(r"\s*(\d+)%\s+(.+?)\s+(\d+)(?:-(\d+))?", line)
    if not match:
        return {"raw": line}
    rarity = int(match.group(1))
    name = match.group(2).strip()
    min_level = int(match.group(3))
    max_level = int(match.group(4)) if match.group(4) else min_level
    return {
        "Pokemon": name,
        "Rarity": rarity,
        "MinLevel": min_level,
        "MaxLevel": max_level,
    }


# -----------------------
# 🧾 Raid reward parser
# -----------------------
def parse_raid_reward(line):
    match = re.match(r"\s*(\d+)%\s+(.+)", line)
    if not match:
        return {"raw": line}
    return {"Item": match.group(2).strip(), "Chance": int(match.group(1))}


# -----------------------
# 🧱 Raid block parser
# -----------------------

def parse_raid_block(entries):
    parsed = []
    i = 0
    while i < len(entries) - 1:
        pokemon = entries[i]
        rewards = entries[i + 1]

        if not isinstance(rewards, list):
            # Something went wrong — skip this one
            i += 1
            continue

        parsed.append({
            "Pokemon": pokemon,
            "Rewards": [parse_raid_reward(r) for r in rewards]
        })
        i += 2
    return parsed

# -----------------------
# 📥 Load encounters.txt
# -----------------------
with open("RR 4.1 encounters.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

data = ast.literal_eval(raw_text)

# -----------------------
# 🔄 Convert to JSON structure
# -----------------------
json_data = {}
unstructured_keywords = {"gift", "trade"}

for i in range(0, len(data), 2):
    location = data[i]
    method_data = data[i + 1]

    method_dict = {}
    for j in range(0, len(method_data), 2):
        method = method_data[j]
        entries = method_data[j + 1]

        if "raid" in method.lower():
            method_dict[method] = parse_raid_block(entries)

        elif any(keyword in method.lower() for keyword in unstructured_keywords):
            method_dict[method] = entries

        else:
            method_dict[method] = [parse_encounter(line) for line in entries]

    json_data[location] = method_dict

# -----------------------
# 💾 Save as structured JSON
# -----------------------
with open("structured_encounters.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=2)

print("✅ Conversion complete. Saved to structured_encounters.json")
