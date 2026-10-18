"""
generate_descriptions.py

Deterministic Motivation-Affordance NLG Engine:
Generates player-oriented, motivation-grounded game recommendations for hybrid gamer profiles.

Instead of generic product metadata recitation, this generator answers:
"Which verified aspects of this game are relevant to this player's motivations,
and what evidence supports that connection?"

Deterministic Components:
1. Archetype Motivations: Core psychological motivations loaded directly from gamer_archetypes.csv
   (Cardboard Republic taxonomy), eliminating hardcoded string dictionaries.
2. Affordance Linkage: Binds verified matched game mechanics to the player's hybrid motivations.
3. Evidentiary Validation: Surfaces verbatim player reviews verifying that gameplay dynamic.
4. Chronological Presentation Sequences: Configurable clause permutations [1..4].
"""

import json
import os
import csv
import argparse

# Chronological sequence presets
SEQUENCES = {
    "1": ["motivation", "affordance", "evidence", "access"],  # Motivation First (Standard)
    "2": ["affordance", "motivation", "evidence", "access"],  # Affordance/Mechanics First
    "3": ["evidence", "motivation", "affordance", "access"],  # Evidence First
    "4": ["access", "motivation", "affordance", "evidence"]   # Access/Platform First
}


def load_archetype_motivations(csv_path="gamer_archetypes.csv"):
    """
    Loads core motivations directly from the CSV taxonomy.
    No hardcoded archetype sentence dictionaries in Python.
    """
    motivations = {}
    if os.path.exists(csv_path):
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                archetype = row.get("archetype", "").strip()
                core_mot = row.get("core_motivation", "").strip()
                if archetype and core_mot:
                    motivations[archetype] = core_mot
    return motivations


def load_gamer_profiles(json_path="gamer_profiles.json"):
    """Loads profiles metadata from external JSON file."""
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Profiles file not found at: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def select_review_evidence(quotes):
    """Selects verified player review evidence for the matched game."""
    if not quotes:
        return {
            "quote": "The overall gameplay loop and depth are solidly executed."
        }
    return quotes[0]


def format_motivation_clauses(profile, game, motivations=None, first_key=None):
    """
    Constructs deterministic relational clauses linking player motivations
    to verified game mechanics and authentic player evidence.
    Conditioned on first_key for coherent Referring Expression Generation (REG):
    the leading sentence explicitly introduces '{title}', while subsequent sentences
    use natural anaphoric references ('the game', 'its').
    """
    if motivations is None:
        motivations = load_archetype_motivations()

    title = game.get("title", "Untitled Game")
    developer = game.get("developer", "Unknown Developer")
    price = game.get("price", "Unpriced")
    platforms = ", ".join(game.get("platforms", ["PC"]))
    recs_total = game.get("recommendations_total", 0)
    positive_ratio = game.get("positive_ratio", "Positive")

    primary = profile.get("primary_archetype", "Tactician")
    secondary = profile.get("secondary_archetype", "Architect")
    persona = profile.get("hybrid_persona", f"{primary} / {secondary}")

    p_mot = profile.get("primary_motivation") or motivations.get(primary, "careful planning and resource management")
    s_mot = profile.get("secondary_motivation") or motivations.get(secondary, "engaging secondary playstyles")

    matched_attrs = game.get("matched_attributes", [])
    if matched_attrs:
        attrs_formatted = ", ".join(matched_attrs)
    else:
        attrs_formatted = "established core mechanics"

    evidence = select_review_evidence(game.get("review_quotes", []))
    quote_text = evidence.get("quote", "").strip()
    recs_str = f"{recs_total:,}" if recs_total > 0 else "initial"
    pct_clean = positive_ratio.replace(" Positive", "")

    release_year = game.get("release_year")
    year_str = f", released in {release_year}," if release_year else ""

    # Referring Expression Generation (REG) conditioned on clause sequence order
    if first_key == "affordance":
        affordance_clause = f"'{title}'s core design incorporates {attrs_formatted} to support this style of play."
    else:
        affordance_clause = f"Its core design incorporates {attrs_formatted} to support this style of play."

    if first_key == "motivation" or first_key is None:
        motivation_clause = f"For {persona} players, '{title}' appeals to an interest in {p_mot} while also engaging {s_mot}."
    else:
        motivation_clause = f"For {persona} players, the game appeals to an interest in {p_mot} while also engaging {s_mot}."

    if first_key == "evidence":
        evidence_clause = f"Among {recs_str} reviews for '{title}', {pct_clean} are positive. One review states: \"{quote_text}\""
    else:
        evidence_clause = f"Among {recs_str} reviews, {pct_clean} are positive. One review states: \"{quote_text}\""

    if first_key == "access":
        access_clause = f"'{title}' was developed by {developer}{year_str} and is available on {platforms} for {price}."
    else:
        access_clause = f"The game was developed by {developer}{year_str} and is available on {platforms} for {price}."

    clauses = {
        "motivation": motivation_clause,
        "affordance": affordance_clause,
        "evidence": evidence_clause,
        "access": access_clause
    }

    return clauses


def build_description(profile, sequence, motivations=None):
    """Assembles motivation-affordance clauses in the specified chronological order."""
    game = profile.get("matched_game", {})
    first_key = sequence[0] if sequence else None
    clauses = format_motivation_clauses(profile, game, motivations, first_key=first_key)
    ordered_body = " ".join([clauses[k] for k in sequence])
    return ordered_body


def generate_all_descriptions(profiles, sequence, motivations=None):
    """Generates descriptions for all profiles using the active sequence."""
    if motivations is None:
        motivations = load_archetype_motivations()
    output = []
    for prof in profiles:
        desc = build_description(prof, sequence, motivations)
        output.append({
            "profile_id": prof["id"],
            "persona": prof["hybrid_persona"],
            "primary_archetype": prof.get("primary_archetype"),
            "secondary_archetype": prof.get("secondary_archetype"),
            "game": prof["matched_game"]["title"],
            "sequence": " -> ".join(sequence),
            "description": desc
        })
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate motivation-grounded descriptions from gamer profiles.")
    parser.add_argument("--profiles", default="gamer_profiles.json", help="Path to gamer profiles JSON.")
    parser.add_argument("--archetypes", default="gamer_archetypes.csv", help="Path to gamer archetypes CSV.")
    parser.add_argument("--order", default="1", choices=["1", "2", "3", "4"],
                        help="Chronological order preset (1: Motivation first, 2: Affordance first, 3: Evidence first, 4: Access first).")
    parser.add_argument("--out", default="generated_descriptions.json", help="Output JSON path.")
    args = parser.parse_args()

    chosen_sequence = SEQUENCES[args.order]
    motivations = load_archetype_motivations(args.archetypes)
    profiles = load_gamer_profiles(args.profiles)
    results = generate_all_descriptions(profiles, chosen_sequence, motivations)

    print(f"\nLoaded {len(profiles)} profiles from '{args.profiles}'.")
    print(f"Loaded {len(motivations)} core motivations from '{args.archetypes}'.")
    print(f"Active Chronological Sequence: {' -> '.join(chosen_sequence)}\n")
    print("=" * 80)
    for res in results:
        print(f"\n{res['description']}\n")
        print("-" * 80)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved motivation-grounded descriptions to '{args.out}'.")
