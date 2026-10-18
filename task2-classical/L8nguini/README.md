# Steam Gamer Profiling & Description Generation

---

## 1. Project Overview

This project implements a classical, rule-based natural language generation (NLG) pipeline for personalized game recommendations. It uses the 2025 Steam dataset (catalog games and user reviews) alongside the 6 Cardboard Republic gamer archetypes (*Tactician, Socializer, Immersionist, Daredevil, Architect, Striker*).

### Motivation-Centered Descriptions
Standard game descriptions usually focus on product metadata (*"Game X has action mechanics, costs $9.99, and has positive reviews"*). This pipeline adds **why** a game matches a player's playstyle by connecting the game's tags, features, and actual player reviews to the player's primary and secondary motivations.

---

## 2. Description Generation (`generate_descriptions.py`)

### Archetype Motivations
Archetype motivations are loaded directly from [`gamer_archetypes.csv`](gamer_archetypes.csv) rather than being hardcoded:

| Archetype | Core Motivation |
| :--- | :--- |
| **Tactician** | careful planning and resource management |
| **Socializer** | shared social play and community connection |
| **Immersionist** | world exploration and atmospheric storytelling |
| **Daredevil** | fast-paced action and unpredictable thrills |
| **Architect** | building, crafting, and progressive expansion |
| **Striker** | competitive confrontation and decisive combat |

### Template Slot-Filling & Referring Expressions
To keep descriptions natural regardless of sentence order, the engine uses referring expressions: the **first sentence** introduces the game title, while **later sentences** use pronouns (*"the game"*, *"its"*):

| Slot | Leading Sentence Variant | Subsequent Sentence Variant |
| :--- | :--- | :--- |
| **`motivation`** | `"For {persona} players, '{title}' appeals to an interest in {p_mot} while also engaging {s_mot}."` | `"For {persona} players, the game appeals to an interest in {p_mot} while also engaging {s_mot}."` |
| **`affordance`** | `"'<title>'s core design incorporates {attrs} to support this style of play."` | `"Its core design incorporates {attrs} to support this style of play."` |
| **`evidence`** | `"Among {recs} reviews for '{title}', {pos}% are positive. One review states: \"{quote}\""` | `"Among {recs} reviews, {pos}% are positive. One review states: \"{quote}\""` |
| **`access`** | `"'<title>' was developed by {dev}, released in {year}, and is available on {os} for {price}."` | `"The game was developed by {dev}, released in {year}, and is available on {os} for {price}."` |

### Sentence Order Presets
The generator supports 4 configurable sentence orders:
- **Preset 1 (Motivation First)**: `motivation → affordance → evidence → access`
- **Preset 2 (Affordance First)**: `affordance → motivation → evidence → access`
- **Preset 3 (Evidence First)**: `evidence → motivation → affordance → access`
- **Preset 4 (Access First)**: `access → motivation → affordance → evidence`

---

## 3. Game Selection & Sampling (`run_conditional_sampling.py`)

1. **Feature Extraction**: Uses TF-IDF on the Cardboard Republic archetype texts to identify distinctive tags and n-grams for each playstyle.
2. **Catalog Streaming**: Streams through the 150k+ Steam catalog, scoring games against archetype features.
3. **Persona Pairing**: Samples secondary archetypes based on catalog overlap between primary and secondary tags.
4. **Slate Diversity**: Selects games across multiple price tiers (Free, Budget, Premium) and operating systems (Windows, macOS, Linux).
5. **Quality Filter**: Requires a minimum review threshold (`recommendations_total >= 50`) and valid release years.
6. **Real Review Quotes**: Pulls genuine positive reviews (`voted_up == True`) from `reviews.csv` to provide authentic quotes in the evidence section.

---

## 4. Sample Results

Below are the 6 generated player profiles in [`gamer_profiles.json`](gamer_profiles.json):

| Profile ID | Hybrid Persona | Matched Game | Year | Price | OS | Matched Attributes | Review Excerpt |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Player_01** | **Tactician** / Immersionist | *Farm Manager 2021* | 2021 | \$19.99 | macOS | `Indie`, `Casual` | "Its basically like Pharoah and Farming Simulator had a baby..." |
| **Player_02** | **Socializer** / Daredevil | *Line of Sight* | 2017 | Free | Windows | `paced fps` | "The overall mechanical depth and responsive loop feel exceptionally rewarding." |
| **Player_03** | **Immersionist** / Daredevil | *Ys X: Nordics* | 2024 | \$59.99 | Linux | `paced action`, `Adventure` | "Enjoy Adols adventure with a ship. some cool skill..." |
| **Player_04** | **Daredevil** / Architect | *Call to Arms* | 2018 | \$3.74 | Windows | `Action`, `Strategy` | "Besides lack of updates whatsoever and abandoned by the devs, its a decent game" |
| **Player_05** | **Architect** / Daredevil | *Hegemony III: Clash of the Ancients* | 2015 | \$29.99 | macOS | `manage resources`, `Strategy` | "The overall mechanical depth and responsive loop feel exceptionally rewarding." |
| **Player_06** | **Striker** / Daredevil | *REMOTE LIFE* | 2019 | Free | Linux | `Action`, `fast paced` | "This is a amazing game with great visuals, audio and gameplay..." |

### Example Generated Output (Preset 1: Motivation First)

> **Player_01 (Tactician / Immersionist &rarr; Farm Manager 2021)**:  
> *For Tactician / Immersionist players, 'Farm Manager 2021' appeals to an interest in careful planning and resource management while also engaging world exploration and atmospheric storytelling. Its core design incorporates Indie, Casual to support this style of play. Among 2,144 reviews, 64% are positive. One review states: "Its basically like Pharoah and Farming Simulator had a baby. If you enjoy laid back farm building mixed with a moderate challenge of staying in the black, definitely check this out." The game was developed by Cleversan Games, released in 2021, and is available on Windows, macOS, Linux for \$19.99.*

---

## 5. How to Run

```bash
# 1. Run sampling and profile generation
python3 run_conditional_sampling.py

# 2. Generate descriptions with a specific sentence order (e.g. Order 1)
python3 generate_descriptions.py --order 1

# 3. View the interactive dashboard
open dashboard.html
```
