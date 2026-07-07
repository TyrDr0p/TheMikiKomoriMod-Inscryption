from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "1 Card Generator"))

from generator_core.builders import (  # noqa: E402
    build_card_data,
    build_card_filename,
    build_sigil_data,
    build_sigil_filename,
    build_talking_card_data,
    build_talking_filename,
    build_tribe_filename,
    build_tribes_data,
)
from generator_core.constants import (  # noqa: E402
    ABILITY_OPTIONS,
    ABILITY_TOOLTIPS,
    APPEARANCE_BEHAVIOUR_TOOLTIPS,
    APPEARANCE_BEHAVIOURS,
    CARD_COMPLEXITY_TOOLTIPS,
    META_CATEGORIES,
    META_CATEGORY_TOOLTIPS,
    SPECIAL_ABILITY_TOOLTIPS,
    SPECIAL_STAT_ICON_TOOLTIPS,
    TEMPLE_TOOLTIPS,
    TRAIT_TOOLTIPS,
    TRAITS,
)
from generator_core.scroll import mousewheel_units  # noqa: E402
from generator_core.schemas import validate_output  # noqa: E402
from generator_core.sigil_behavior import build_action, build_behavior_entry, merge_action  # noqa: E402


class BuilderValidationTests(unittest.TestCase):
    def assert_valid(self, kind: str, data: dict) -> None:
        errors = validate_output(kind, data)
        self.assertEqual([], errors)

    def test_phish_known_good_card_matches(self):
        actual = build_card_data(
            card_id="Phish",
            mod_prefix="TMK",
            displayed_name="All That Dwells In The Sea",
            description="This creature is odd... Maybe one of wolf's pack? Certainly not the angler's.",
            meta_categories=["ChoiceNode", "TraderOffer"],
            card_complexity="Vanilla",
            temple="Nature",
            base_attack=2,
            base_health=2,
            blood_cost=2,
            tribes=["Reptile"],
            traits=["SatisfiesRingTrial"],
            abilities=["Submerge", "StrafeSwap"],
            texture="PhishCard.png",
        )

        self.assertEqual(
            {
                "name": "Phish",
                "modPrefix": "TMK",
                "displayedName": "All That Dwells In The Sea",
                "description": "This creature is odd... Maybe one of wolf's pack? Certainly not the angler's.",
                "metaCategories": ["ChoiceNode", "TraderOffer"],
                "cardComplexity": "Vanilla",
                "temple": "Nature",
                "baseAttack": 2,
                "baseHealth": 2,
                "bloodCost": 2,
                "tribes": ["Reptile"],
                "traits": ["SatisfiesRingTrial"],
                "abilities": ["Submerge", "StrafeSwap"],
                "texture": "PhishCard.png",
            },
            actual,
        )
        self.assert_valid("cards", actual)

    def test_minimal_outputs_validate_against_local_schemas(self):
        self.assert_valid("cards", build_card_data(card_id="CardOne", base_health=1))

        self.assert_valid(
            "sigils",
            build_sigil_data(name="MySigil", guid="MyMod", ability_behaviour=[]),
        )

        self.assert_valid(
            "tribes",
            build_tribes_data([
                {
                    "name": "MyTribe",
                    "guid": "MyMod",
                    "tribeIcon": "MyTribe.png",
                    "appearInTribeChoices": True,
                }
            ]),
        )

        self.assert_valid(
            "talking_cards",
            build_talking_card_data(
                card_name="MyMod_CardOne",
                face_sprite="Face.png",
                eye_open="EyeOpen.png",
                eye_closed="EyeClosed.png",
                mouth_open="MouthOpen.png",
                mouth_closed="MouthClosed.png",
                emission_open="EmissionOpen.png",
                emission_closed="EmissionClosed.png",
                dialogue_events=[
                    {
                        "eventName": "OnDrawn",
                        "mainLines": ["Hello."],
                        "repeatLines": [["Hello again."]],
                    }
                ],
            ),
        )

    def test_optional_defaults_are_omitted_when_schema_safe(self):
        card = build_card_data(card_id="NoCosts", base_health=1)
        for key in ("bloodCost", "bonesCost", "energyCost", "gemsCost", "specialStatIcon"):
            self.assertNotIn(key, card)
        self.assert_valid("cards", card)

    def test_filename_suffixes(self):
        self.assertEqual("TMK_Phish.jldr2", build_card_filename("Phish", "TMK"))
        self.assertEqual("Hook_sigil.jldr2", build_sigil_filename("Hook"))
        self.assertEqual("Fish_troupe_tribe.jldr2", build_tribe_filename("Fish troupe"))
        self.assertEqual("TMK_Phish_talk.jldr2", build_talking_filename("TMK_Phish"))


class ScrollTests(unittest.TestCase):
    def test_mousewheel_units_windows_and_macos(self):
        self.assertEqual(-1, mousewheel_units(SimpleNamespace(delta=120)))
        self.assertEqual(1, mousewheel_units(SimpleNamespace(delta=-120)))
        self.assertEqual(-1, mousewheel_units(SimpleNamespace(delta=1)))
        self.assertEqual(1, mousewheel_units(SimpleNamespace(delta=-1)))

    def test_mousewheel_units_linux_buttons(self):
        self.assertEqual(-3, mousewheel_units(SimpleNamespace(num=4, delta=0)))
        self.assertEqual(3, mousewheel_units(SimpleNamespace(num=5, delta=0)))
        self.assertEqual(0, mousewheel_units(SimpleNamespace(delta=0)))


class EnumOptionTests(unittest.TestCase):
    def test_vanilla_enum_options_include_saxby_values(self):
        for ability in ("ActivatedDealDamage", "Deathtouch", "GuardDog", "SplitStrike", "DrawRabbits"):
            self.assertIn(ability, ABILITY_OPTIONS)
        self.assertNotIn("TouchOfDeath", ABILITY_OPTIONS)
        self.assertNotIn("Guardian", ABILITY_OPTIONS)
        self.assertIn("Lice", TRAITS)
        self.assertIn("MoonParticleEffects", APPEARANCE_BEHAVIOURS)
        self.assertIn("AscensionUnlock", META_CATEGORIES)

    def test_tooltips_are_present_only_for_described_enum_values(self):
        self.assertEqual("Defines the card to be a choice option.", META_CATEGORY_TOOLTIPS["ChoiceNode"])
        self.assertNotIn("AscensionUnlock", META_CATEGORY_TOOLTIPS)
        self.assertEqual("Will always be a learned card.", CARD_COMPLEXITY_TOOLTIPS["Vanilla"])
        self.assertEqual("Will show up in act 3 and Tech card packs.", TEMPLE_TOOLTIPS["Tech"])
        self.assertIn("attack and health", SPECIAL_STAT_ICON_TOOLTIPS["Bones"])
        self.assertIn("Pelt Lice", TRAIT_TOOLTIPS["Lice"])
        self.assertIn("opposing card", ABILITY_TOOLTIPS["ActivatedDealDamage"])
        self.assertNotIn("ActivatedRandomPowerBone", ABILITY_TOOLTIPS)
        self.assertIn("distance from the bell", SPECIAL_ABILITY_TOOLTIPS["BellProximity"])
        self.assertIn("rare background", APPEARANCE_BEHAVIOUR_TOOLTIPS["RareCardBackground"])


class SigilBehaviorBuilderTests(unittest.TestCase):
    def test_place_card_template_validates_as_sigil_behaviour(self):
        behaviour = build_behavior_entry(
            trigger_type="OnResolveOnBoard",
            trigger_condition="[BaseCard.Health] > 0",
            action_order=["placeCards"],
            action_type="placeCards",
            fields={
                "slot_index": "([BaseCard.Slot.Index] + 1)",
                "slot_opponent": False,
                "card_name": "Rabbit",
                "retain_mods": True,
                "replace": False,
            },
        )
        sigil = build_sigil_data(name="RabbitMaker", guid="MyMod", ability_behaviour=[behaviour])

        self.assertEqual("OnResolveOnBoard", behaviour["trigger"]["triggerType"])
        self.assertEqual("Rabbit", behaviour["placeCards"][0]["card"]["name"])
        self.assertEqual([], validate_output("sigils", sigil))

    def test_merge_action_adds_common_actions_to_existing_behaviour(self):
        entry = {"trigger": {"triggerType": "OnActivate"}}
        merge_action(
            entry,
            build_action(
                "gainCurrency",
                {"condition": "", "bones": "1", "energy": "", "foils": ""},
            ),
        )
        merge_action(
            entry,
            build_action(
                "showMessage",
                {
                    "message": "Bones gained.",
                    "message_length": "2",
                    "message_emotion": "Neutral",
                    "letter_animation": "None",
                    "speaker": "Leshy",
                },
            ),
        )

        self.assertEqual("1", entry["gainCurrency"]["bones"])
        self.assertEqual("Bones gained.", entry["showMessage"]["message"])
        self.assertEqual([], validate_output("sigils", build_sigil_data(name="BoneTalk", guid="MyMod", ability_behaviour=[entry])))


if __name__ == "__main__":
    unittest.main()
