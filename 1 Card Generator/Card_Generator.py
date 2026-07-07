from __future__ import annotations

import json
import tkinter as tk
from tkinter import ttk, messagebox

from generator_core.builders import (
    build_card_data,
    build_card_filename,
    build_sigil_data,
    build_sigil_filename,
    build_talking_card_data,
    build_talking_filename,
    build_tribe_filename,
    build_tribes_data,
    parse_csv,
)
from generator_core.constants import (
    ABILITIES,
    ABILITY_TOOLTIPS,
    APPEARANCE_BEHAVIOURS,
    APPEARANCE_BEHAVIOUR_TOOLTIPS,
    CARD_COMPLEXITIES,
    CARD_COMPLEXITY_TOOLTIPS,
    CONFIGIL_ACTION_ORDER,
    CONFIGIL_ACTION_TOOLTIPS,
    CONFIGIL_ACTION_TYPES,
    CONFIGIL_FIELD_TOOLTIPS,
    CONFIGIL_LETTER_ANIMATIONS,
    CONFIGIL_MESSAGE_EMOTIONS,
    CONFIGIL_SPEAKERS,
    CONFIGIL_STRAFE_DIRECTIONS,
    CONFIGIL_TRIGGER_TOOLTIPS,
    CONFIGIL_TRIGGER_TYPES,
    EMOTION_TYPES,
    EVENT_NAMES,
    GEM_TYPES,
    META_CATEGORIES,
    META_CATEGORY_TOOLTIPS,
    SPECIAL_ABILITY_TOOLTIPS,
    SIGIL_BEHAVIOR_TEMPLATE,
    SPECIAL_STAT_ICONS,
    SPECIAL_STAT_ICON_TOOLTIPS,
    SPECIAL_TRIGGERED_ABILITIES,
    TEMPLE_TOOLTIPS,
    TEMPLES,
    TRAIT_TOOLTIPS,
    TRAITS,
    TRIBES,
    VOICE_IDS,
)
from generator_core.appearance import AppearanceManager
from generator_core.schema_editor import JSONSchemaTextEditor
from generator_core.schemas import load_schema
from generator_core.scroll import ScrollableFrame
from generator_core.sigil_behavior import build_action, build_behavior_entry, merge_action
from generator_core.ui_helpers import (
    CollapsibleSection,
    ResponsiveCheckboxGroup,
    ToolTip,
    choose_audio,
    choose_image,
    save_json_file,
    update_json_preview,
)


class GeneratorTab(ttk.Frame):
    schema_kind = ""

    def __init__(self, master):
        super().__init__(master)
        self.status = tk.StringVar(value="")
        self._build_layout()

    def _build_layout(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.panes = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.panes.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.form = ScrollableFrame(self.panes)
        self.panes.add(self.form, weight=3)

        right = ttk.Frame(self.panes)
        self.panes.add(right, weight=2)
        right.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)
        ttk.Label(right, text="JSON Preview", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=tk.W)
        preview_frame = ttk.Frame(right)
        preview_frame.grid(row=1, column=0, sticky="nsew", pady=(5, 5))
        preview_frame.rowconfigure(0, weight=1)
        preview_frame.columnconfigure(0, weight=1)
        self.preview = tk.Text(preview_frame, width=58, height=30, wrap=tk.NONE, state=tk.DISABLED)
        preview_y = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=self.preview.yview)
        preview_x = ttk.Scrollbar(preview_frame, orient=tk.HORIZONTAL, command=self.preview.xview)
        self.preview.configure(yscrollcommand=preview_y.set, xscrollcommand=preview_x.set)
        self.preview.grid(row=0, column=0, sticky="nsew")
        preview_y.grid(row=0, column=1, sticky="ns")
        preview_x.grid(row=1, column=0, sticky="ew")
        ttk.Label(right, textvariable=self.status, style="Status.TLabel", wraplength=520).grid(
            row=2, column=0, sticky=tk.W
        )

    def section(self, parent, row, title, expanded=True):
        section = CollapsibleSection(parent, title, expanded=expanded)
        section.grid(row=row, column=0, columnspan=3, sticky="ew")
        section.body.columnconfigure(1, weight=1)
        return section.body, row + 1

    def labeled_entry(self, parent, row, label, var, width=36, tooltip=None):
        label_widget = ttk.Label(parent, text=label)
        label_widget.grid(row=row, column=0, sticky=tk.W, pady=2)
        if tooltip:
            ToolTip(label_widget, tooltip)
        ttk.Entry(parent, textvariable=var, width=width).grid(row=row, column=1, sticky="ew", pady=2)
        return row + 1

    def labeled_spin(self, parent, row, label, var, from_=0, to=99, increment=1, width=7, tooltip=None):
        label_widget = ttk.Label(parent, text=label)
        label_widget.grid(row=row, column=0, sticky=tk.W, pady=2)
        if tooltip:
            ToolTip(label_widget, tooltip)
        ttk.Spinbox(parent, from_=from_, to=to, increment=increment, textvariable=var, width=width).grid(
            row=row, column=1, sticky=tk.W, pady=2
        )
        return row + 1

    def labeled_combo(self, parent, row, label, var, values, width=24, tooltips=None, tooltip=None):
        label_widget = ttk.Label(parent, text=label)
        label_widget.grid(row=row, column=0, sticky=tk.W, pady=2)
        if tooltip:
            ToolTip(label_widget, tooltip)
        combo = ttk.Combobox(parent, textvariable=var, values=values, state="readonly", width=width)
        combo.grid(row=row, column=1, sticky="ew", pady=2)
        if tooltips:
            tooltip = ToolTip(combo, tooltips.get(var.get(), ""))
            var.trace_add("write", lambda *_args: setattr(tooltip, "text", tooltips.get(var.get(), "")))
        return row + 1

    def image_entry(self, parent, row, label, var, tooltip=None):
        label_widget = ttk.Label(parent, text=label)
        label_widget.grid(row=row, column=0, sticky=tk.W, pady=2)
        if tooltip:
            ToolTip(label_widget, tooltip)
        ttk.Entry(parent, textvariable=var, width=34).grid(row=row, column=1, sticky="ew", pady=2)
        ttk.Button(parent, text="Browse...", command=lambda: choose_image(var)).grid(row=row, column=2, sticky=tk.W, padx=5)
        return row + 1

    def action_buttons(self, parent, row, save_text):
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=20)
        ttk.Button(frame, text="Preview / Validate", command=self.refresh_preview).pack(side=tk.LEFT)
        ttk.Button(frame, text=save_text, command=self.save).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(frame, text="Reset Form", command=self.reset).pack(side=tk.LEFT, padx=(8, 0))

    def checkbox_group(self, parent, row, title, vars_by_key, columns=3, labels=None, tooltips=None):
        ttk.Label(parent, text=title).grid(row=row, column=0, sticky=tk.NW, pady=(8, 2))
        group = ResponsiveCheckboxGroup(
            parent,
            vars_by_key,
            labels=labels,
            tooltips=tooltips,
            preferred_columns=columns,
        )
        group.grid(row=row, column=1, columnspan=2, sticky="ew", pady=(8, 2))
        return row + 1

    def selected(self, vars_by_key):
        return [key for key, var in vars_by_key.items() if var.get()]

    def preview_data(self, data):
        return update_json_preview(self.preview, self.status, self.schema_kind, data)


class CardsTab(GeneratorTab):
    schema_kind = "cards"

    def __init__(self, master):
        super().__init__(master)
        self.reset()

    def _build_layout(self):
        super()._build_layout()
        parent = self.form.content
        self.card_id = tk.StringVar()
        self.mod_prefix = tk.StringVar()
        self.displayed_name = tk.StringVar()
        self.description = tk.StringVar()
        self.card_complexity = tk.StringVar()
        self.temple = tk.StringVar()
        self.base_attack = tk.IntVar()
        self.base_health = tk.IntVar()
        self.hide_attack_and_health = tk.BooleanVar()
        self.blood_cost = tk.IntVar()
        self.bones_cost = tk.IntVar()
        self.energy_cost = tk.IntVar()
        self.gems_cost = {gem: tk.BooleanVar(value=False) for gem in GEM_TYPES}
        self.special_stat_icon = tk.StringVar()
        self.tribe_vars = {tribe: tk.BooleanVar(value=False) for tribe in TRIBES}
        self.trait_vars = {trait: tk.BooleanVar(value=False) for trait in TRAITS}
        self.appearance_vars = {appearance: tk.BooleanVar(value=False) for appearance in APPEARANCE_BEHAVIOURS}
        self.meta_categories = {cat: tk.BooleanVar(value=False) for cat in META_CATEGORIES}
        self.ability_vars = {ability["internal"]: tk.BooleanVar(value=False) for ability in ABILITIES}
        self.special_ability_vars = {name: tk.BooleanVar(value=False) for name in SPECIAL_TRIGGERED_ABILITIES}
        self.custom_special = tk.StringVar()
        self.evolve_into_name = tk.StringVar()
        self.evolve_turns = tk.IntVar()
        self.default_evolution_name = tk.StringVar()
        self.tail_name = tk.StringVar()
        self.tail_lost_portrait = tk.StringVar()
        self.ice_cube_name = tk.StringVar()
        self.flip_portrait_for_strafe = tk.BooleanVar()
        self.one_per_deck = tk.BooleanVar()
        self.texture = tk.StringVar()
        self.emission_texture = tk.StringVar()
        self.alt_texture = tk.StringVar()
        self.alt_emission_texture = tk.StringVar()
        self.pixel_texture = tk.StringVar()
        self.title_graphic = tk.StringVar()
        self.decals = tk.StringVar()

        parent.columnconfigure(0, weight=1)
        row = 0

        section, row = self.section(parent, row, "Card Identity")
        section_row = 0
        section_row = self.labeled_entry(section, section_row, "Card ID", self.card_id)
        section_row = self.labeled_entry(section, section_row, "Mod Prefix", self.mod_prefix, width=20)
        section_row = self.labeled_entry(section, section_row, "Displayed Name", self.displayed_name)
        section_row = self.labeled_entry(section, section_row, "Description", self.description, width=50)
        section_row = self.labeled_combo(section, section_row, "Complexity", self.card_complexity, CARD_COMPLEXITIES, tooltips=CARD_COMPLEXITY_TOOLTIPS)
        section_row = self.labeled_combo(section, section_row, "Temple", self.temple, TEMPLES, tooltips=TEMPLE_TOOLTIPS)

        section, row = self.section(parent, row, "Stats & Costs")
        section_row = 0
        section_row = self.labeled_spin(section, section_row, "Attack", self.base_attack)
        section_row = self.labeled_spin(section, section_row, "Health", self.base_health, from_=1)
        section_row = self.labeled_spin(section, section_row, "Blood Cost", self.blood_cost, to=10)
        section_row = self.labeled_spin(section, section_row, "Bones Cost", self.bones_cost, to=30)
        section_row = self.labeled_spin(section, section_row, "Energy Cost", self.energy_cost, to=10)
        ttk.Checkbutton(section, text="Hide Attack and Health", variable=self.hide_attack_and_health).grid(row=section_row, column=1, sticky=tk.W, pady=2)
        section_row += 1
        section_row = self.checkbox_group(section, section_row, "Gems Cost", self.gems_cost)

        section, row = self.section(parent, row, "Categories")
        section_row = 0
        section_row = self.checkbox_group(section, section_row, "Tribes", self.tribe_vars, columns=3)
        section_row = self.checkbox_group(section, section_row, "Traits", self.trait_vars, columns=3, tooltips=TRAIT_TOOLTIPS)
        section_row = self.labeled_combo(
            section, section_row, "Special Stat Icon", self.special_stat_icon, ["None"] + SPECIAL_STAT_ICONS,
            tooltips=SPECIAL_STAT_ICON_TOOLTIPS,
        )
        section_row = self.checkbox_group(section, section_row, "Appearance Behaviours", self.appearance_vars, columns=3, tooltips=APPEARANCE_BEHAVIOUR_TOOLTIPS)
        section_row = self.checkbox_group(section, section_row, "Meta Categories", self.meta_categories, columns=4, tooltips=META_CATEGORY_TOOLTIPS)
        section_row = self.checkbox_group(
            section, section_row, "Abilities", self.ability_vars, columns=4,
            labels={a["internal"]: a["display"] for a in ABILITIES},
            tooltips=ABILITY_TOOLTIPS,
        )
        section_row = self.checkbox_group(section, section_row, "Special Abilities", self.special_ability_vars, columns=4, tooltips=SPECIAL_ABILITY_TOOLTIPS)
        section_row = self.labeled_entry(section, section_row, "Custom Special Abilities (comma-separated)", self.custom_special, width=50)

        section, row = self.section(parent, row, "Optional Card Links", expanded=False)
        section_row = 0
        section_row = self.labeled_entry(section, section_row, "Evolve Into Name", self.evolve_into_name)
        section_row = self.labeled_spin(section, section_row, "Evolve Turns", self.evolve_turns, to=20)
        section_row = self.labeled_entry(section, section_row, "Default Evolution Name", self.default_evolution_name)
        section_row = self.labeled_entry(section, section_row, "Tail Name", self.tail_name)
        section_row = self.image_entry(section, section_row, "Tail Lost Portrait", self.tail_lost_portrait)
        section_row = self.labeled_entry(section, section_row, "Ice Cube Name", self.ice_cube_name)
        ttk.Checkbutton(section, text="Flip Portrait For Strafe", variable=self.flip_portrait_for_strafe).grid(row=section_row, column=1, sticky=tk.W, pady=2)
        section_row += 1
        ttk.Checkbutton(section, text="One Per Deck", variable=self.one_per_deck).grid(row=section_row, column=1, sticky=tk.W, pady=2)

        section, row = self.section(parent, row, "Textures", expanded=False)
        section_row = 0
        section_row = self.image_entry(section, section_row, "Texture", self.texture)
        section_row = self.image_entry(section, section_row, "Emission Texture", self.emission_texture)
        section_row = self.image_entry(section, section_row, "Alt Texture", self.alt_texture)
        section_row = self.image_entry(section, section_row, "Alt Emission Texture", self.alt_emission_texture)
        section_row = self.image_entry(section, section_row, "Pixel Texture", self.pixel_texture)
        section_row = self.image_entry(section, section_row, "Title Graphic", self.title_graphic)
        section_row = self.labeled_entry(section, section_row, "Decals (comma-separated)", self.decals, width=50)

        section, row = self.section(parent, row, "Extension Properties JSON", expanded=False)
        self.extension_properties = tk.Text(section, height=4, width=58)
        self.extension_properties.grid(row=0, column=0, columnspan=3, sticky="ew")
        self.action_buttons(parent, row, "Save Card .jldr2")

    def data(self):
        extension_text = self.extension_properties.get("1.0", tk.END).strip()
        extension_properties = json.loads(extension_text) if extension_text else {}
        return build_card_data(
            card_id=self.card_id.get().strip(),
            mod_prefix=self.mod_prefix.get().strip(),
            displayed_name=self.displayed_name.get().strip(),
            description=self.description.get().strip(),
            meta_categories=self.selected(self.meta_categories),
            card_complexity=self.card_complexity.get(),
            temple=self.temple.get(),
            base_attack=self.base_attack.get(),
            base_health=self.base_health.get(),
            hide_attack_and_health=self.hide_attack_and_health.get(),
            blood_cost=self.blood_cost.get(),
            bones_cost=self.bones_cost.get(),
            energy_cost=self.energy_cost.get(),
            gems_cost=self.selected(self.gems_cost),
            special_stat_icon="" if self.special_stat_icon.get() == "None" else self.special_stat_icon.get(),
            tribes=self.selected(self.tribe_vars),
            traits=self.selected(self.trait_vars),
            special_abilities=self.selected(self.special_ability_vars) + parse_csv(self.custom_special.get()),
            abilities=self.selected(self.ability_vars),
            evolve_into_name=self.evolve_into_name.get().strip(),
            evolve_turns=self.evolve_turns.get(),
            default_evolution_name=self.default_evolution_name.get().strip(),
            tail_name=self.tail_name.get().strip(),
            tail_lost_portrait=self.tail_lost_portrait.get().strip(),
            ice_cube_name=self.ice_cube_name.get().strip(),
            flip_portrait_for_strafe=self.flip_portrait_for_strafe.get(),
            one_per_deck=self.one_per_deck.get(),
            appearance_behaviour=self.selected(self.appearance_vars),
            texture=self.texture.get().strip(),
            emission_texture=self.emission_texture.get().strip(),
            alt_texture=self.alt_texture.get().strip(),
            alt_emission_texture=self.alt_emission_texture.get().strip(),
            pixel_texture=self.pixel_texture.get().strip(),
            title_graphic=self.title_graphic.get().strip(),
            decals=parse_csv(self.decals.get()),
            extension_properties=extension_properties,
        )

    def refresh_preview(self):
        try:
            data = self.data()
        except json.JSONDecodeError as exc:
            self.status.set(f"Extension Properties JSON parse error: {exc}")
            return
        self.preview_data(data)

    def save(self):
        try:
            data = self.data()
        except json.JSONDecodeError as exc:
            messagebox.showerror("JSON Error", f"Extension Properties JSON parse error: {exc}")
            return
        save_json_file("cards", data, build_card_filename(self.card_id.get(), self.mod_prefix.get()), "Card")

    def reset(self):
        self.card_id.set("Stoat")
        self.mod_prefix.set("MyMod")
        self.displayed_name.set("Stoat")
        self.description.set("A cunning creature.")
        self.card_complexity.set("Vanilla")
        self.temple.set("Nature")
        self.base_attack.set(2)
        self.base_health.set(2)
        self.hide_attack_and_health.set(False)
        self.blood_cost.set(0)
        self.bones_cost.set(0)
        self.energy_cost.set(0)
        self.special_stat_icon.set("None")
        for group in (
            self.gems_cost, self.tribe_vars, self.trait_vars, self.appearance_vars,
            self.meta_categories, self.ability_vars, self.special_ability_vars,
        ):
            for var in group.values():
                var.set(False)
        for var in (
            self.custom_special, self.evolve_into_name, self.default_evolution_name, self.tail_name,
            self.tail_lost_portrait, self.ice_cube_name, self.texture, self.emission_texture,
            self.alt_texture, self.alt_emission_texture, self.pixel_texture, self.title_graphic, self.decals,
        ):
            var.set("")
        self.evolve_turns.set(0)
        self.flip_portrait_for_strafe.set(False)
        self.one_per_deck.set(False)
        self.extension_properties.delete("1.0", tk.END)
        self.form.scroll_to_top()
        self.refresh_preview()


class SigilsTab(GeneratorTab):
    schema_kind = "sigils"

    def __init__(self, master):
        self.behavior_schema = load_schema("sigils")["properties"]["abilityBehaviour"]
        super().__init__(master)
        self.reset()

    def _build_layout(self):
        super()._build_layout()
        parent = self.form.content
        self.name = tk.StringVar()
        self.guid = tk.StringVar()
        self.description = tk.StringVar()
        self.meta_categories = {cat: tk.BooleanVar(value=False) for cat in META_CATEGORIES}
        self.texture = tk.StringVar()
        self.pixel_texture = tk.StringVar()
        self.power_level = tk.IntVar()
        self.priority = tk.IntVar()
        self.opponent_usable = tk.BooleanVar()
        self.can_stack = tk.BooleanVar()
        self.is_special_ability = tk.BooleanVar()
        self.bones_cost = tk.IntVar()
        self.energy_cost = tk.IntVar()
        self.blood_cost = tk.IntVar()
        self.gems_cost = {gem: tk.BooleanVar(value=False) for gem in GEM_TYPES}
        self.trigger_type = tk.StringVar()
        self.trigger_condition = tk.StringVar()
        self.trigger_health_level = tk.StringVar()
        self.action_order_vars = {name: tk.BooleanVar(value=False) for name in CONFIGIL_ACTION_ORDER}
        self.action_type = tk.StringVar()
        self.action_condition = tk.StringVar()
        self.slot_index = tk.StringVar()
        self.slot_opponent = tk.BooleanVar()
        self.secondary_slot_index = tk.StringVar()
        self.secondary_slot_opponent = tk.BooleanVar()
        self.action_card_name = tk.StringVar()
        self.action_target_card = tk.StringVar()
        self.retain_mods = tk.BooleanVar()
        self.replace_action = tk.BooleanVar()
        self.heal_amount = tk.StringVar()
        self.add_stats = tk.StringVar()
        self.set_stats = tk.StringVar()
        self.add_ability = tk.StringVar()
        self.remove_ability = tk.StringVar()
        self.infused_ability = tk.BooleanVar()
        self.damage_amount = tk.StringVar()
        self.gain_bones = tk.StringVar()
        self.gain_energy = tk.StringVar()
        self.gain_foils = tk.StringVar()
        self.strafe_direction = tk.StringVar()
        self.flip_sigil = tk.BooleanVar()
        self.message_text = tk.StringVar()
        self.message_length = tk.StringVar()
        self.message_emotion = tk.StringVar()
        self.letter_animation = tk.StringVar()
        self.speaker = tk.StringVar()
        parent.columnconfigure(0, weight=1)
        row = 0

        section, row = self.section(parent, row, "Sigil Identity")
        section_row = 0
        section_row = self.labeled_entry(section, section_row, "Name", self.name, tooltip="Required string for the name of your sigil.")
        section_row = self.labeled_entry(section, section_row, "GUID", self.guid, tooltip="Required string that identifies the sigil.")
        section_row = self.labeled_entry(section, section_row, "Description", self.description, width=50, tooltip="Optional rulebook description for the sigil.")
        section_row = self.checkbox_group(section, section_row, "Meta Categories", self.meta_categories, columns=4, tooltips=META_CATEGORY_TOOLTIPS)
        section_row = self.image_entry(section, section_row, "Texture", self.texture, tooltip="Optional sigil artwork. Configils expects a 49x49 .png.")
        section_row = self.image_entry(section, section_row, "Pixel Texture", self.pixel_texture, tooltip="Optional pixel sigil artwork. Configils expects a 17x17 .png.")
        section_row = self.labeled_spin(section, section_row, "Power Level", self.power_level, to=99, tooltip="Affects rarity in cave trials, sigil nodes, and Leshy's totem battles.")
        section_row = self.labeled_spin(section, section_row, "Priority", self.priority, to=99, tooltip="Controls activation order. Lower priority sigils activate before higher priority sigils.")
        opponent_usable = ttk.Checkbutton(section, text="Opponent Usable", variable=self.opponent_usable)
        opponent_usable.grid(row=section_row, column=1, sticky=tk.W)
        ToolTip(opponent_usable, "Determines whether the sigil can appear on Leshy's totems.")
        section_row += 1
        can_stack = ttk.Checkbutton(section, text="Can Stack", variable=self.can_stack)
        can_stack.grid(row=section_row, column=1, sticky=tk.W)
        ToolTip(can_stack, "Determines whether multiple copies of this sigil can stack on one card.")
        section_row += 1
        is_special = ttk.Checkbutton(section, text="Is Special Ability", variable=self.is_special_ability)
        is_special.grid(row=section_row, column=1, sticky=tk.W)
        ToolTip(is_special, "If true, Configils treats this as a special ability and several rulebook fields are no longer required.")

        section, row = self.section(parent, row, "Activation Cost", expanded=False)
        section_row = 0
        section_row = self.labeled_spin(section, section_row, "Bones", self.bones_cost, to=30, tooltip="Bone token cost to activate the sigil.")
        section_row = self.labeled_spin(section, section_row, "Energy", self.energy_cost, to=10, tooltip="Energy cost to activate the sigil.")
        section_row = self.labeled_spin(section, section_row, "Blood", self.blood_cost, to=10, tooltip="Number of creatures that must be sacrificed to activate the sigil.")
        ttk.Label(section, text="Gems").grid(row=section_row, column=0, sticky=tk.NW)
        gems = ttk.Frame(section)
        gems.grid(row=section_row, column=1, sticky=tk.W)
        for gem, var in self.gems_cost.items():
            ttk.Checkbutton(gems, text=gem, variable=var).pack(side=tk.LEFT)

        section, row = self.section(parent, row, "Ability Behaviour Builder")
        section_row = 0
        section_row = self.labeled_combo(
            section, section_row, "Trigger", self.trigger_type, CONFIGIL_TRIGGER_TYPES, width=28,
            tooltips=CONFIGIL_TRIGGER_TOOLTIPS,
        )
        section_row = self.labeled_entry(
            section, section_row, "Trigger Condition", self.trigger_condition, width=52,
            tooltip="Optional condition that must evaluate to true for the sigil to activate.",
        )
        section_row = self.labeled_entry(
            section, section_row, "Health Level", self.trigger_health_level, width=12,
            tooltip="Used by OnHealthLevel. The trigger fires when health is reduced to this value or lower.",
        )
        section_row = self.checkbox_group(section, section_row, "Action Order", self.action_order_vars, columns=4, tooltips=CONFIGIL_ACTION_TOOLTIPS)

        section_row = self.labeled_combo(
            section, section_row, "Action Template", self.action_type, CONFIGIL_ACTION_TYPES, width=28,
            tooltips=CONFIGIL_ACTION_TOOLTIPS,
        )
        section_row = self.labeled_entry(section, section_row, "Action Condition", self.action_condition, width=52, tooltip=CONFIGIL_FIELD_TOOLTIPS["condition"])
        section_row = self.labeled_entry(section, section_row, "Primary Slot Index", self.slot_index, width=20, tooltip=CONFIGIL_FIELD_TOOLTIPS["slot"])
        ttk.Checkbutton(section, text="Primary Slot Is Opponent Slot", variable=self.slot_opponent).grid(row=section_row, column=1, sticky=tk.W, pady=2)
        section_row += 1
        section_row = self.labeled_entry(section, section_row, "Secondary Slot Index", self.secondary_slot_index, width=20, tooltip=CONFIGIL_FIELD_TOOLTIPS["slot"])
        ttk.Checkbutton(section, text="Secondary Slot Is Opponent Slot", variable=self.secondary_slot_opponent).grid(row=section_row, column=1, sticky=tk.W, pady=2)
        section_row += 1
        section_row = self.labeled_entry(section, section_row, "Card Name", self.action_card_name, width=36, tooltip=CONFIGIL_FIELD_TOOLTIPS["card"])
        section_row = self.labeled_entry(section, section_row, "Target Card", self.action_target_card, width=36, tooltip=CONFIGIL_FIELD_TOOLTIPS["targetCard"])
        ttk.Checkbutton(section, text="Retain Mods", variable=self.retain_mods).grid(row=section_row, column=1, sticky=tk.W, pady=2)
        section_row += 1
        ttk.Checkbutton(section, text="Replace Existing Card", variable=self.replace_action).grid(row=section_row, column=1, sticky=tk.W, pady=2)
        section_row += 1

        section_row = self.labeled_entry(section, section_row, "Heal Amount", self.heal_amount, width=20)
        section_row = self.labeled_entry(section, section_row, "Add Stats", self.add_stats, width=20, tooltip=CONFIGIL_FIELD_TOOLTIPS["stats"])
        section_row = self.labeled_entry(section, section_row, "Set Stats", self.set_stats, width=20, tooltip=CONFIGIL_FIELD_TOOLTIPS["stats"])
        section_row = self.labeled_entry(section, section_row, "Add Ability", self.add_ability, width=36)
        section_row = self.labeled_entry(section, section_row, "Remove Ability", self.remove_ability, width=36)
        ttk.Checkbutton(section, text="Added Ability Is Infused", variable=self.infused_ability).grid(row=section_row, column=1, sticky=tk.W, pady=2)
        section_row += 1
        section_row = self.labeled_entry(section, section_row, "Damage", self.damage_amount, width=20, tooltip=CONFIGIL_FIELD_TOOLTIPS["damage"])
        section_row = self.labeled_entry(section, section_row, "Gain Bones", self.gain_bones, width=20, tooltip=CONFIGIL_FIELD_TOOLTIPS["currency"])
        section_row = self.labeled_entry(section, section_row, "Gain Energy", self.gain_energy, width=20, tooltip=CONFIGIL_FIELD_TOOLTIPS["currency"])
        section_row = self.labeled_entry(section, section_row, "Gain Foils", self.gain_foils, width=20, tooltip=CONFIGIL_FIELD_TOOLTIPS["currency"])
        section_row = self.labeled_combo(section, section_row, "Strafe Direction", self.strafe_direction, ["None"] + CONFIGIL_STRAFE_DIRECTIONS, width=16)
        ttk.Checkbutton(section, text="Flip Sigil On Bounce", variable=self.flip_sigil).grid(row=section_row, column=1, sticky=tk.W, pady=2)
        section_row += 1
        section_row = self.labeled_entry(section, section_row, "Message", self.message_text, width=52)
        section_row = self.labeled_entry(section, section_row, "Message Length", self.message_length, width=12, tooltip=CONFIGIL_FIELD_TOOLTIPS["messageLength"])
        section_row = self.labeled_combo(section, section_row, "Message Emotion", self.message_emotion, CONFIGIL_MESSAGE_EMOTIONS, width=18)
        section_row = self.labeled_combo(section, section_row, "Letter Animation", self.letter_animation, CONFIGIL_LETTER_ANIMATIONS, width=18)
        section_row = self.labeled_combo(section, section_row, "Speaker", self.speaker, CONFIGIL_SPEAKERS, width=28)

        builder_buttons = ttk.Frame(section)
        builder_buttons.grid(row=section_row, column=0, columnspan=3, sticky=tk.W, pady=(8, 4))
        ttk.Button(builder_buttons, text="Replace Behavior With Template", command=self.replace_behavior_from_builder).pack(side=tk.LEFT)
        ttk.Button(builder_buttons, text="Append New Triggered Behavior", command=self.append_behavior_from_builder).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(builder_buttons, text="Add Action To First Behavior", command=self.add_action_to_first_behavior).pack(side=tk.LEFT, padx=(8, 0))

        section, row = self.section(parent, row, "Advanced Ability Behaviour JSON", expanded=False)
        self.behavior_editor = JSONSchemaTextEditor(section, self.behavior_schema, [], height=18)
        self.behavior_editor.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.action_buttons(parent, row, "Save Sigil _sigil.jldr2")

    def selected_gems(self):
        return [gem for gem, var in self.gems_cost.items() if var.get()]

    def selected_action_order(self):
        return self.selected(self.action_order_vars)

    def action_fields(self):
        strafe_direction = "" if self.strafe_direction.get() == "None" else self.strafe_direction.get()
        return {
            "condition": self.action_condition.get().strip(),
            "slot_index": self.slot_index.get().strip(),
            "slot_opponent": self.slot_opponent.get(),
            "secondary_slot_index": self.secondary_slot_index.get().strip(),
            "secondary_slot_opponent": self.secondary_slot_opponent.get(),
            "card_name": self.action_card_name.get().strip(),
            "target_card": self.action_target_card.get().strip(),
            "retain_mods": self.retain_mods.get(),
            "replace": self.replace_action.get(),
            "heal": self.heal_amount.get().strip(),
            "add_stats": self.add_stats.get().strip(),
            "set_stats": self.set_stats.get().strip(),
            "add_ability": self.add_ability.get().strip(),
            "remove_ability": self.remove_ability.get().strip(),
            "infused": self.infused_ability.get(),
            "damage": self.damage_amount.get().strip(),
            "bones": self.gain_bones.get().strip(),
            "energy": self.gain_energy.get().strip(),
            "foils": self.gain_foils.get().strip(),
            "strafe_direction": strafe_direction,
            "flip_sigil": self.flip_sigil.get(),
            "message": self.message_text.get().strip(),
            "message_length": self.message_length.get().strip(),
            "message_emotion": self.message_emotion.get(),
            "letter_animation": self.letter_animation.get(),
            "speaker": self.speaker.get(),
        }

    def behavior_from_builder(self):
        return build_behavior_entry(
            trigger_type=self.trigger_type.get(),
            trigger_condition=self.trigger_condition.get().strip(),
            health_level=self.trigger_health_level.get().strip(),
            action_order=self.selected_action_order(),
            action_type=self.action_type.get(),
            fields=self.action_fields(),
        )

    def current_behavior(self):
        value = self.behavior_editor.get_value()
        if not isinstance(value, list):
            raise ValueError("Ability Behaviour JSON must be an array.")
        return value

    def set_behavior(self, value):
        self.behavior_editor.set_value(value)
        self.refresh_preview()

    def replace_behavior_from_builder(self):
        try:
            self.set_behavior([self.behavior_from_builder()])
        except (json.JSONDecodeError, ValueError) as exc:
            self.status.set(f"Behavior builder error: {exc}")

    def append_behavior_from_builder(self):
        try:
            behavior = self.current_behavior()
            behavior.append(self.behavior_from_builder())
            self.set_behavior(behavior)
        except (json.JSONDecodeError, ValueError) as exc:
            self.status.set(f"Behavior builder error: {exc}")

    def add_action_to_first_behavior(self):
        try:
            behavior = self.current_behavior()
            if not behavior:
                behavior.append({"trigger": {"triggerType": self.trigger_type.get()}})
            merge_action(behavior[0], build_action(self.action_type.get(), self.action_fields()))
            order = self.selected_action_order()
            if order:
                behavior[0]["actionOrder"] = order
            self.set_behavior(behavior)
        except (json.JSONDecodeError, ValueError) as exc:
            self.status.set(f"Behavior builder error: {exc}")

    def data(self):
        return build_sigil_data(
            name=self.name.get().strip(),
            guid=self.guid.get().strip(),
            description=self.description.get().strip(),
            meta_categories=self.selected(self.meta_categories),
            texture=self.texture.get().strip(),
            pixel_texture=self.pixel_texture.get().strip(),
            power_level=self.power_level.get(),
            priority=self.priority.get(),
            opponent_usable=self.opponent_usable.get(),
            can_stack=self.can_stack.get(),
            activation_bones=self.bones_cost.get(),
            activation_energy=self.energy_cost.get(),
            activation_blood=self.blood_cost.get(),
            activation_gems=self.selected_gems(),
            is_special_ability=self.is_special_ability.get(),
            ability_behaviour=self.behavior_editor.get_value(),
        )

    def refresh_preview(self):
        try:
            self.preview_data(self.data())
        except json.JSONDecodeError as exc:
            self.status.set(f"Ability Behaviour JSON parse error: {exc}")

    def save(self):
        try:
            data = self.data()
        except json.JSONDecodeError as exc:
            messagebox.showerror("JSON Error", f"Ability Behaviour JSON parse error: {exc}")
            return
        save_json_file("sigils", data, build_sigil_filename(self.name.get()), "Sigil")

    def reset(self):
        self.name.set("MySigil")
        self.guid.set("MyMod")
        self.description.set("")
        self.texture.set("MySigil.png")
        self.pixel_texture.set("")
        self.power_level.set(0)
        self.priority.set(0)
        self.opponent_usable.set(True)
        self.can_stack.set(True)
        self.is_special_ability.set(True)
        self.bones_cost.set(0)
        self.energy_cost.set(0)
        self.blood_cost.set(0)
        for var in self.meta_categories.values():
            var.set(False)
        for var in self.gems_cost.values():
            var.set(False)
        self.trigger_type.set("OnResolveOnBoard")
        self.trigger_condition.set("")
        self.trigger_health_level.set("")
        self.action_type.set("placeCards")
        self.action_condition.set("")
        self.slot_index.set("[BaseCard.Slot.Index]")
        self.slot_opponent.set(False)
        self.secondary_slot_index.set("")
        self.secondary_slot_opponent.set(False)
        self.action_card_name.set("Rabbit")
        self.action_target_card.set("")
        self.retain_mods.set(False)
        self.replace_action.set(False)
        self.heal_amount.set("")
        self.add_stats.set("")
        self.set_stats.set("")
        self.add_ability.set("")
        self.remove_ability.set("")
        self.infused_ability.set(False)
        self.damage_amount.set("1")
        self.gain_bones.set("")
        self.gain_energy.set("")
        self.gain_foils.set("")
        self.strafe_direction.set("None")
        self.flip_sigil.set(False)
        self.message_text.set("A sigil effect activates.")
        self.message_length.set("2")
        self.message_emotion.set("Neutral")
        self.letter_animation.set("None")
        self.speaker.set("Leshy")
        for var in self.action_order_vars.values():
            var.set(False)
        self.behavior_editor.set_value(SIGIL_BEHAVIOR_TEMPLATE)
        self.form.scroll_to_top()
        self.refresh_preview()


class TribesTab(GeneratorTab):
    schema_kind = "tribes"

    def __init__(self, master):
        super().__init__(master)
        self.reset()

    def _build_layout(self):
        super()._build_layout()
        parent = self.form.content
        self.name = tk.StringVar()
        self.guid = tk.StringVar()
        self.tribe_icon = tk.StringVar()
        self.appear = tk.BooleanVar()
        self.choice_back = tk.StringVar()
        parent.columnconfigure(0, weight=1)
        row = 0
        section, row = self.section(parent, row, "Tribe Definition")
        section_row = 0
        section_row = self.labeled_entry(section, section_row, "Name", self.name)
        section_row = self.labeled_entry(section, section_row, "GUID", self.guid)
        section_row = self.image_entry(section, section_row, "Tribe Icon", self.tribe_icon)
        ttk.Checkbutton(section, text="Appear In Tribe Choices", variable=self.appear).grid(row=section_row, column=1, sticky=tk.W)
        section_row += 1
        section_row = self.image_entry(section, section_row, "Choice Card Back Texture", self.choice_back)

        section, row = self.section(parent, row, "Additional Tribes JSON Array", expanded=False)
        self.extra_tribes = tk.Text(section, height=8, width=58)
        self.extra_tribes.grid(row=0, column=0, columnspan=3, sticky="ew")
        self.action_buttons(parent, row, "Save Tribe _tribe.jldr2")

    def data(self):
        tribes = [{
            "name": self.name.get().strip(),
            "guid": self.guid.get().strip(),
            "tribeIcon": self.tribe_icon.get().strip(),
            "appearInTribeChoices": self.appear.get(),
            "choiceCardBackTexture": self.choice_back.get().strip(),
        }]
        extra = self.extra_tribes.get("1.0", tk.END).strip()
        if extra:
            tribes.extend(json.loads(extra))
        return build_tribes_data(tribes)

    def refresh_preview(self):
        try:
            self.preview_data(self.data())
        except json.JSONDecodeError as exc:
            self.status.set(f"Additional Tribes JSON parse error: {exc}")

    def save(self):
        try:
            data = self.data()
        except json.JSONDecodeError as exc:
            messagebox.showerror("JSON Error", f"Additional Tribes JSON parse error: {exc}")
            return
        save_json_file("tribes", data, build_tribe_filename(self.name.get()), "Tribe")

    def reset(self):
        self.name.set("MyTribe")
        self.guid.set("MyMod")
        self.tribe_icon.set("MyTribe.png")
        self.appear.set(True)
        self.choice_back.set("")
        self.extra_tribes.delete("1.0", tk.END)
        self.form.scroll_to_top()
        self.refresh_preview()


class TalkingCardsTab(GeneratorTab):
    schema_kind = "talking_cards"

    def __init__(self, master):
        schema = load_schema("talking_cards")
        self.emotions_schema = schema["properties"]["emotions"]
        self.events_schema = schema["properties"]["dialogueEvents"]
        super().__init__(master)
        self.reset()

    def _build_layout(self):
        super()._build_layout()
        parent = self.form.content
        self.card_name = tk.StringVar()
        self.face_sprite = tk.StringVar()
        self.eye_open = tk.StringVar()
        self.eye_closed = tk.StringVar()
        self.mouth_open = tk.StringVar()
        self.mouth_closed = tk.StringVar()
        self.emission_open = tk.StringVar()
        self.emission_closed = tk.StringVar()
        self.blink_rate = tk.DoubleVar()
        self.voice_id = tk.StringVar()
        self.voice_pitch = tk.DoubleVar()
        self.custom_voice = tk.StringVar()
        self.emotion_choice = tk.StringVar()
        self.event_choice = tk.StringVar()
        self.event_main_line = tk.StringVar()
        self.event_repeat_line = tk.StringVar()
        parent.columnconfigure(0, weight=1)
        row = 0

        section, row = self.section(parent, row, "Talking Card Sprites")
        section_row = 0
        section_row = self.labeled_entry(section, section_row, "Card Name", self.card_name)
        section_row = self.image_entry(section, section_row, "Face Sprite", self.face_sprite)
        section_row = self.image_entry(section, section_row, "Eye Open", self.eye_open)
        section_row = self.image_entry(section, section_row, "Eye Closed", self.eye_closed)
        section_row = self.image_entry(section, section_row, "Mouth Open", self.mouth_open)
        section_row = self.image_entry(section, section_row, "Mouth Closed", self.mouth_closed)
        section_row = self.image_entry(section, section_row, "Emission Open", self.emission_open)
        section_row = self.image_entry(section, section_row, "Emission Closed", self.emission_closed)
        section_row = self.labeled_spin(section, section_row, "Blink Rate", self.blink_rate, from_=0.1, to=10, increment=0.1)
        section_row = self.labeled_combo(section, section_row, "Voice ID", self.voice_id, VOICE_IDS)
        section_row = self.labeled_spin(section, section_row, "Voice Pitch", self.voice_pitch, from_=0.1, to=10, increment=0.1)
        ttk.Label(section, text="Custom Voice").grid(row=section_row, column=0, sticky=tk.W, pady=2)
        ttk.Entry(section, textvariable=self.custom_voice, width=34).grid(row=section_row, column=1, sticky="ew", pady=2)
        ttk.Button(section, text="Browse...", command=lambda: choose_audio(self.custom_voice)).grid(row=section_row, column=2, sticky=tk.W, padx=5)

        section, row = self.section(parent, row, "Emotion Template", expanded=False)
        section_row = 0
        section_row = self.labeled_combo(section, section_row, "Emotion", self.emotion_choice, EMOTION_TYPES)
        ttk.Button(section, text="Add Emotion", command=self.add_emotion_template).grid(row=section_row, column=1, sticky=tk.W, pady=2)

        section, row = self.section(parent, row, "Emotions JSON Array", expanded=False)
        self.emotions_editor = JSONSchemaTextEditor(section, self.emotions_schema, [], height=8)
        self.emotions_editor.grid(row=0, column=0, columnspan=3, sticky="nsew")

        section, row = self.section(parent, row, "Dialogue Event Template")
        section_row = 0
        section_row = self.labeled_combo(section, section_row, "Event Name", self.event_choice, EVENT_NAMES, width=34)
        section_row = self.labeled_entry(section, section_row, "Main Line", self.event_main_line, width=50)
        section_row = self.labeled_entry(section, section_row, "Repeat Line", self.event_repeat_line, width=50)
        ttk.Button(section, text="Add Dialogue Event", command=self.add_dialogue_event_template).grid(row=section_row, column=1, sticky=tk.W, pady=2)

        section, row = self.section(parent, row, "Dialogue Events JSON Array", expanded=False)
        self.events_editor = JSONSchemaTextEditor(section, self.events_schema, [], height=12)
        self.events_editor.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.action_buttons(parent, row, "Save Talking Card _talk.jldr2")

    def data(self):
        return build_talking_card_data(
            card_name=self.card_name.get().strip(),
            face_sprite=self.face_sprite.get().strip(),
            eye_open=self.eye_open.get().strip(),
            eye_closed=self.eye_closed.get().strip(),
            mouth_open=self.mouth_open.get().strip(),
            mouth_closed=self.mouth_closed.get().strip(),
            emission_open=self.emission_open.get().strip(),
            emission_closed=self.emission_closed.get().strip(),
            blink_rate=self.blink_rate.get(),
            voice_id=self.voice_id.get(),
            voice_pitch=self.voice_pitch.get(),
            custom_voice=self.custom_voice.get().strip(),
            emotions=self.emotions_editor.get_value(),
            dialogue_events=self.events_editor.get_value(),
        )

    def append_editor_item(self, editor, item, label):
        try:
            value = editor.get_value()
        except json.JSONDecodeError as exc:
            self.status.set(f"{label} JSON parse error: {exc}")
            return
        if not isinstance(value, list):
            self.status.set(f"{label} JSON must be an array.")
            return
        value.append(item)
        editor.set_value(value)
        self.refresh_preview()

    def add_emotion_template(self):
        self.append_editor_item(self.emotions_editor, {"emotion": self.emotion_choice.get()}, "Emotions")

    def add_dialogue_event_template(self):
        main_line = self.event_main_line.get().strip() or "Hello."
        repeat_line = self.event_repeat_line.get().strip() or main_line
        self.append_editor_item(
            self.events_editor,
            {"eventName": self.event_choice.get(), "mainLines": [main_line], "repeatLines": [[repeat_line]]},
            "Dialogue Events",
        )

    def refresh_preview(self):
        try:
            self.preview_data(self.data())
        except json.JSONDecodeError as exc:
            self.status.set(f"Nested JSON parse error: {exc}")

    def save(self):
        try:
            data = self.data()
        except json.JSONDecodeError as exc:
            messagebox.showerror("JSON Error", f"Nested JSON parse error: {exc}")
            return
        save_json_file("talking_cards", data, build_talking_filename(self.card_name.get()), "Talking card")

    def reset(self):
        self.card_name.set("MyMod_Stoat")
        self.face_sprite.set("Face.png")
        self.eye_open.set("EyeOpen.png")
        self.eye_closed.set("EyeClosed.png")
        self.mouth_open.set("MouthOpen.png")
        self.mouth_closed.set("MouthClosed.png")
        self.emission_open.set("EmissionOpen.png")
        self.emission_closed.set("EmissionClosed.png")
        self.blink_rate.set(1.5)
        self.voice_id.set("None")
        self.voice_pitch.set(1.0)
        self.custom_voice.set("")
        self.emotion_choice.set(EMOTION_TYPES[0])
        self.event_choice.set(EVENT_NAMES[0])
        self.event_main_line.set("Hello.")
        self.event_repeat_line.set("Hello again.")
        self.emotions_editor.set_value([])
        self.events_editor.set_value([
            {"eventName": "OnDrawn", "mainLines": ["Hello."], "repeatLines": [["Hello again."]]}
        ])
        self.form.scroll_to_top()
        self.refresh_preview()


class JSONCardLoaderGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.appearance = AppearanceManager(root)
        self.dark_mode = tk.BooleanVar(value=False)
        self.root.title("Inscryption JSONCardLoader Generator")
        self.root.geometry("1400x900")
        self.root.resizable(True, True)

        toolbar = ttk.Frame(root, style="Toolbar.TFrame")
        toolbar.pack(fill=tk.X, padx=5, pady=(5, 0))
        ttk.Checkbutton(toolbar, text="Dark Mode", variable=self.dark_mode, command=self.toggle_theme).pack(
            side=tk.RIGHT
        )

        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        notebook.add(CardsTab(notebook), text="Cards")
        notebook.add(SigilsTab(notebook), text="Sigils")
        notebook.add(TribesTab(notebook), text="Tribes")
        notebook.add(TalkingCardsTab(notebook), text="Talking Cards")
        self.appearance.apply("light")

    def toggle_theme(self):
        self.appearance.apply("dark" if self.dark_mode.get() else "light")


def main():
    root = tk.Tk()
    JSONCardLoaderGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
