from __future__ import annotations

import copy
import logging


logger = logging.getLogger(__name__)


ARRAY_ACTIONS = {
    "placeCards", "buffCards", "transformCards", "damageSlots", "attackSlots",
    "extraAttacks", "drawCards", "chooseSlots", "moveCards",
}


def maybe_set(data: dict, key: str, value):
    if value not in ("", None, [], {}):
        data[key] = value


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def slot(index: str = "", is_opponent: bool = False) -> dict:
    data = {}
    maybe_set(data, "index", index.strip())
    data["isOpponentSlot"] = bool_text(is_opponent)
    return data


def card(name: str = "", retain_mods: bool = False) -> dict:
    data = {}
    maybe_set(data, "name", name.strip())
    if retain_mods:
        data["retainMods"] = "true"
    return data


def with_condition(data: dict, condition: str) -> dict:
    maybe_set(data, "runOnCondition", condition.strip())
    return data


def build_trigger(trigger_type: str, condition: str = "", health_level: str = "") -> dict:
    trigger = {"triggerType": trigger_type}
    maybe_set(trigger, "activatesForCardsWithCondition", condition.strip())
    maybe_set(trigger, "amountOfHealth", health_level.strip())
    logger.debug("Built Configils trigger=%s", trigger)
    return trigger


def build_behavior_entry(
    *,
    trigger_type: str,
    trigger_condition: str = "",
    health_level: str = "",
    action_order: list[str] | None = None,
    action_type: str,
    fields: dict,
) -> dict:
    logger.debug(
        "Building Configils behavior trigger_type=%s action_type=%s action_order=%s fields=%s",
        trigger_type,
        action_type,
        action_order,
        fields,
    )
    entry = {"trigger": build_trigger(trigger_type, trigger_condition, health_level)}
    maybe_set(entry, "actionOrder", action_order or [])
    merge_action(entry, build_action(action_type, fields))
    logger.debug("Built Configils behavior entry=%s", entry)
    return entry


def build_action(action_type: str, fields: dict) -> dict:
    logger.debug("Building Configils action action_type=%s fields=%s", action_type, fields)
    condition = fields.get("condition", "")
    primary_slot = slot(fields.get("slot_index", ""), fields.get("slot_opponent", False))
    secondary_slot = slot(fields.get("secondary_slot_index", ""), fields.get("secondary_slot_opponent", False))
    named_card = card(fields.get("card_name", ""), fields.get("retain_mods", False))

    if action_type == "placeCards":
        item = with_condition({"slot": primary_slot, "card": named_card}, condition)
        if fields.get("replace"):
            item["replace"] = "true"
        action = {"placeCards": [item]}
        logger.debug("Built Configils action=%s", action)
        return action

    if action_type == "buffCards":
        item = with_condition({"slot": primary_slot}, condition)
        maybe_set(item, "targetCard", fields.get("target_card", "").strip())
        maybe_set(item, "heal", fields.get("heal", "").strip())
        maybe_set(item, "addStats", fields.get("add_stats", "").strip())
        maybe_set(item, "setStats", fields.get("set_stats", "").strip())
        add_ability = fields.get("add_ability", "").strip()
        if add_ability:
            item["addAbilities"] = [{"name": add_ability, "infused": bool_text(fields.get("infused", False))}]
        remove_ability = fields.get("remove_ability", "").strip()
        if remove_ability:
            item["removeAbilities"] = [remove_ability]
        action = {"buffCards": [item]}
        logger.debug("Built Configils action=%s", action)
        return action

    if action_type == "transformCards":
        item = with_condition({"slot": primary_slot, "card": named_card}, condition)
        maybe_set(item, "targetCard", fields.get("target_card", "").strip())
        action = {"transformCards": [item]}
        logger.debug("Built Configils action=%s", action)
        return action

    if action_type == "damageSlots":
        item = with_condition({"slot": primary_slot}, condition)
        maybe_set(item, "damage", fields.get("damage", "").strip())
        action = {"damageSlots": [item]}
        logger.debug("Built Configils action=%s", action)
        return action

    if action_type == "attackSlots":
        item = with_condition({"attackerSlot": primary_slot, "victimSlot": secondary_slot}, condition)
        action = {"attackSlots": [item]}
        logger.debug("Built Configils action=%s", action)
        return action

    if action_type == "extraAttacks":
        item = {"attackingSlot": primary_slot, "slotsToAttack": [secondary_slot]}
        action = {"extraAttacks": [item]}
        logger.debug("Built Configils action=%s", action)
        return action

    if action_type == "gainCurrency":
        item = with_condition({}, condition)
        maybe_set(item, "bones", fields.get("bones", "").strip())
        maybe_set(item, "energy", fields.get("energy", "").strip())
        maybe_set(item, "foils", fields.get("foils", "").strip())
        action = {"gainCurrency": item}
        logger.debug("Built Configils action=%s", action)
        return action

    if action_type == "dealScaleDamage":
        item = with_condition({}, condition)
        maybe_set(item, "damage", fields.get("damage", "").strip())
        action = {"dealScaleDamage": item}
        logger.debug("Built Configils action=%s", action)
        return action

    if action_type == "drawCards":
        action = {"drawCards": [with_condition({"card": named_card}, condition)]}
        logger.debug("Built Configils action=%s", action)
        return action

    if action_type == "chooseSlots":
        item = {}
        maybe_set(item, "slotChooseableOnCondition", condition.strip())
        action = {"chooseSlots": [item]}
        logger.debug("Built Configils action=%s", action)
        return action

    if action_type == "moveCards":
        item = with_condition({"moveFromSlot": primary_slot, "moveToSlot": secondary_slot}, condition)
        direction = fields.get("strafe_direction", "")
        if direction:
            item["strafe"] = {"direction": direction, "flipSigil": bool_text(fields.get("flip_sigil", False))}
        if fields.get("replace"):
            item["replace"] = "true"
        action = {"moveCards": [item]}
        logger.debug("Built Configils action=%s", action)
        return action

    if action_type == "showMessage":
        item = {}
        maybe_set(item, "message", fields.get("message", "").strip())
        maybe_set(item, "length", fields.get("message_length", "").strip())
        maybe_set(item, "emotion", fields.get("message_emotion", "").strip())
        maybe_set(item, "letterAnimation", fields.get("letter_animation", "").strip())
        maybe_set(item, "speaker", fields.get("speaker", "").strip())
        action = {"showMessage": item}
        logger.debug("Built Configils action=%s", action)
        return action

    logger.error("Unknown Configils action type: %s", action_type)
    raise ValueError(f"Unknown Configils action type: {action_type}")


def merge_action(entry: dict, action: dict) -> dict:
    logger.debug("Merging Configils action into entry action=%s before=%s", action, entry)
    for key, value in action.items():
        if key in ARRAY_ACTIONS:
            entry.setdefault(key, [])
            entry[key].extend(copy.deepcopy(value))
        elif isinstance(value, dict) and isinstance(entry.get(key), dict):
            entry[key].update(copy.deepcopy(value))
        else:
            entry[key] = copy.deepcopy(value)
    logger.debug("Merged Configils entry=%s", entry)
    return entry
