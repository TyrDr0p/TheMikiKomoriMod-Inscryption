from __future__ import annotations

from .schemas import normalize_asset_path, sanitize_filename, split_csv


def maybe_set(data: dict, key: str, value):
    if value not in ("", None, [], {}):
        data[key] = value


def maybe_positive(data: dict, key: str, value: int):
    if value > 0:
        data[key] = value


def build_card_data(
    *,
    card_id: str,
    mod_prefix: str = "",
    displayed_name: str = "",
    description: str = "",
    meta_categories: list[str] | None = None,
    card_complexity: str = "Vanilla",
    temple: str = "Nature",
    base_attack: int = 0,
    base_health: int = 1,
    hide_attack_and_health: bool = False,
    blood_cost: int = 0,
    bones_cost: int = 0,
    energy_cost: int = 0,
    gems_cost: list[str] | None = None,
    special_stat_icon: str = "",
    tribes: list[str] | None = None,
    traits: list[str] | None = None,
    special_abilities: list[str] | None = None,
    abilities: list[str] | None = None,
    evolve_into_name: str = "",
    evolve_turns: int = 0,
    default_evolution_name: str = "",
    tail_name: str = "",
    tail_lost_portrait: str = "",
    ice_cube_name: str = "",
    flip_portrait_for_strafe: bool = False,
    one_per_deck: bool = False,
    appearance_behaviour: list[str] | None = None,
    texture: str = "",
    emission_texture: str = "",
    alt_texture: str = "",
    alt_emission_texture: str = "",
    pixel_texture: str = "",
    title_graphic: str = "",
    decals: list[str] | None = None,
    extension_properties: dict | None = None,
) -> dict:
    data = {"name": card_id}
    maybe_set(data, "modPrefix", mod_prefix)
    maybe_set(data, "displayedName", displayed_name)
    maybe_set(data, "description", description)
    maybe_set(data, "metaCategories", meta_categories or [])
    maybe_set(data, "cardComplexity", card_complexity)
    maybe_set(data, "temple", temple)
    data["baseAttack"] = base_attack
    data["baseHealth"] = base_health
    if hide_attack_and_health:
        data["hideAttackAndHealth"] = True
    maybe_positive(data, "bloodCost", blood_cost)
    maybe_positive(data, "bonesCost", bones_cost)
    maybe_positive(data, "energyCost", energy_cost)
    maybe_set(data, "gemsCost", gems_cost or [])
    maybe_set(data, "specialStatIcon", special_stat_icon)
    maybe_set(data, "tribes", tribes or [])
    maybe_set(data, "traits", traits or [])
    maybe_set(data, "specialAbilities", special_abilities or [])
    maybe_set(data, "abilities", abilities or [])
    maybe_set(data, "evolveIntoName", evolve_into_name)
    maybe_positive(data, "evolveTurns", evolve_turns)
    maybe_set(data, "defaultEvolutionName", default_evolution_name)
    maybe_set(data, "tailName", tail_name)
    maybe_set(data, "tailLostPortrait", normalize_asset_path(tail_lost_portrait))
    maybe_set(data, "iceCubeName", ice_cube_name)
    if flip_portrait_for_strafe:
        data["flipPortraitForStrafe"] = True
    if one_per_deck:
        data["onePerDeck"] = True
    maybe_set(data, "appearanceBehaviour", appearance_behaviour or [])
    maybe_set(data, "texture", normalize_asset_path(texture))
    maybe_set(data, "emissionTexture", normalize_asset_path(emission_texture))
    maybe_set(data, "altTexture", normalize_asset_path(alt_texture))
    maybe_set(data, "altEmissionTexture", normalize_asset_path(alt_emission_texture))
    maybe_set(data, "pixelTexture", normalize_asset_path(pixel_texture))
    maybe_set(data, "titleGraphic", normalize_asset_path(title_graphic))
    maybe_set(data, "decals", [normalize_asset_path(item) for item in decals or []])
    maybe_set(data, "extensionProperties", extension_properties or {})
    return data


def build_card_filename(card_id: str, mod_prefix: str = "") -> str:
    base = f"{mod_prefix}_{card_id}" if mod_prefix else card_id
    return f"{sanitize_filename(base, 'card')}.jldr2"


def build_sigil_data(
    *,
    name: str,
    guid: str,
    description: str = "",
    meta_categories: list[str] | None = None,
    texture: str = "",
    pixel_texture: str = "",
    power_level: int = 0,
    priority: int = 0,
    opponent_usable: bool = True,
    can_stack: bool = True,
    activation_bones: int = 0,
    activation_energy: int = 0,
    activation_blood: int = 0,
    activation_gems: list[str] | None = None,
    is_special_ability: bool = True,
    ability_behaviour: list | None = None,
) -> dict:
    data = {
        "name": name,
        "GUID": guid,
        "abilityBehaviour": ability_behaviour or [],
    }
    maybe_set(data, "description", description)
    maybe_set(data, "metaCategories", meta_categories or [])
    maybe_set(data, "texture", normalize_asset_path(texture))
    maybe_set(data, "pixelTexture", normalize_asset_path(pixel_texture))
    data["powerLevel"] = power_level
    data["priority"] = priority
    data["opponentUsable"] = opponent_usable
    data["canStack"] = can_stack
    activation = {}
    maybe_positive(activation, "bonesCost", activation_bones)
    maybe_positive(activation, "energyCost", activation_energy)
    maybe_positive(activation, "bloodCost", activation_blood)
    maybe_set(activation, "gemsCost", activation_gems or [])
    maybe_set(data, "activationCost", activation)
    data["isSpecialAbility"] = is_special_ability
    return data


def build_sigil_filename(name: str) -> str:
    return f"{sanitize_filename(name, 'sigil')}_sigil.jldr2"


def build_tribes_data(tribes: list[dict]) -> dict:
    normalized = []
    for tribe in tribes:
        item = {
            "name": tribe["name"],
            "guid": tribe["guid"],
            "tribeIcon": normalize_asset_path(tribe["tribeIcon"]),
            "appearInTribeChoices": tribe.get("appearInTribeChoices", True),
        }
        maybe_set(item, "choiceCardBackTexture", normalize_asset_path(tribe.get("choiceCardBackTexture", "")))
        normalized.append(item)
    return {"tribes": normalized}


def build_tribe_filename(name: str) -> str:
    return f"{sanitize_filename(name, 'tribes')}_tribe.jldr2"


def build_talking_card_data(
    *,
    card_name: str,
    face_sprite: str,
    eye_open: str,
    eye_closed: str,
    mouth_open: str,
    mouth_closed: str,
    emission_open: str,
    emission_closed: str,
    blink_rate: float = 1.5,
    voice_id: str = "None",
    voice_pitch: float = 1.0,
    custom_voice: str = "",
    emotions: list[dict] | None = None,
    dialogue_events: list[dict] | None = None,
) -> dict:
    face_info = {}
    if blink_rate != 1.5:
        face_info["blinkRate"] = blink_rate
    if voice_id and voice_id != "None":
        face_info["voiceId"] = voice_id
    if voice_pitch != 1.0:
        face_info["voiceSoundPitch"] = voice_pitch
    maybe_set(face_info, "customVoice", normalize_asset_path(custom_voice))

    data = {
        "cardName": card_name,
        "faceSprite": normalize_asset_path(face_sprite),
        "eyeSprites": {"open": normalize_asset_path(eye_open), "closed": normalize_asset_path(eye_closed)},
        "mouthSprites": {"open": normalize_asset_path(mouth_open), "closed": normalize_asset_path(mouth_closed)},
        "emissionSprites": {"open": normalize_asset_path(emission_open), "closed": normalize_asset_path(emission_closed)},
        "faceInfo": face_info,
        "dialogueEvents": dialogue_events or [],
    }
    maybe_set(data, "emotions", emotions or [])
    return data


def build_talking_filename(card_name: str) -> str:
    return f"{sanitize_filename(card_name, 'talking_card')}_talk.jldr2"


def parse_lines(value: str) -> list[str]:
    return [line.strip() for line in value.splitlines() if line.strip()]


def parse_csv(value: str) -> list[str]:
    return split_csv(value)

