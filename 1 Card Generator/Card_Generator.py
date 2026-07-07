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
    parse_lines,
)
from generator_core.constants import (
    ABILITIES,
    APPEARANCE_BEHAVIOURS,
    CARD_COMPLEXITIES,
    EMOTION_TYPES,
    EVENT_NAMES,
    GEM_TYPES,
    META_CATEGORIES,
    SIGIL_BEHAVIOR_TEMPLATE,
    SPECIAL_STAT_ICONS,
    SPECIAL_TRIGGERED_ABILITIES,
    TEMPLES,
    TRAITS,
    TRIBES,
    VOICE_IDS,
)
from generator_core.schema_editor import JSONSchemaTextEditor
from generator_core.schemas import load_schema
from generator_core.scroll import ScrollableFrame
from generator_core.ui_helpers import (
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
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.form = ScrollableFrame(self)
        self.form.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        right = ttk.Frame(self)
        right.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        right.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)
        ttk.Label(right, text="JSON Preview", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=tk.W)
        self.preview = tk.Text(right, width=58, height=30, wrap=tk.NONE, state=tk.DISABLED)
        self.preview.grid(row=1, column=0, sticky="nsew", pady=(5, 5))
        ttk.Label(right, textvariable=self.status, foreground="#6a3b00", wraplength=520).grid(row=2, column=0, sticky=tk.W)

    def labeled_entry(self, parent, row, label, var, width=36):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Entry(parent, textvariable=var, width=width).grid(row=row, column=1, sticky=tk.W, pady=2)
        return row + 1

    def labeled_spin(self, parent, row, label, var, from_=0, to=99, increment=1, width=7):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Spinbox(parent, from_=from_, to=to, increment=increment, textvariable=var, width=width).grid(
            row=row, column=1, sticky=tk.W, pady=2
        )
        return row + 1

    def labeled_combo(self, parent, row, label, var, values, width=24):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Combobox(parent, textvariable=var, values=values, state="readonly", width=width).grid(
            row=row, column=1, sticky=tk.W, pady=2
        )
        return row + 1

    def image_entry(self, parent, row, label, var):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Entry(parent, textvariable=var, width=34).grid(row=row, column=1, sticky=tk.W, pady=2)
        ttk.Button(parent, text="Browse...", command=lambda: choose_image(var)).grid(row=row, column=2, sticky=tk.W, padx=5)
        return row + 1

    def action_buttons(self, parent, row, save_text):
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=20)
        ttk.Button(frame, text="Preview / Validate", command=self.refresh_preview).pack(side=tk.LEFT)
        ttk.Button(frame, text=save_text, command=self.save).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(frame, text="Reset Form", command=self.reset).pack(side=tk.LEFT, padx=(8, 0))

    def checkbox_group(self, parent, row, title, vars_by_key, columns=3, labels=None):
        ttk.Label(parent, text=title).grid(row=row, column=0, sticky=tk.NW, pady=(8, 2))
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=1, columnspan=2, sticky=tk.W, pady=(8, 2))
        for index, (key, var) in enumerate(vars_by_key.items()):
            text = labels.get(key, key) if labels else key
            cb = ttk.Checkbutton(frame, text=text, variable=var)
            cb.grid(row=index // columns, column=index % columns, sticky=tk.W, padx=(0, 12))
            if labels:
                ability = next((item for item in ABILITIES if item["internal"] == key), None)
                if ability:
                    ToolTip(cb, ability["desc"])
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

        row = 0
        ttk.Label(parent, text="Card Identity", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W)
        row += 1
        row = self.labeled_entry(parent, row, "Card ID", self.card_id)
        row = self.labeled_entry(parent, row, "Mod Prefix", self.mod_prefix, width=20)
        row = self.labeled_entry(parent, row, "Displayed Name", self.displayed_name)
        row = self.labeled_entry(parent, row, "Description", self.description, width=50)
        row = self.labeled_combo(parent, row, "Complexity", self.card_complexity, CARD_COMPLEXITIES)
        row = self.labeled_combo(parent, row, "Temple", self.temple, TEMPLES)

        ttk.Label(parent, text="Stats & Costs", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(10, 2))
        row += 1
        row = self.labeled_spin(parent, row, "Attack", self.base_attack)
        row = self.labeled_spin(parent, row, "Health", self.base_health, from_=1)
        row = self.labeled_spin(parent, row, "Blood Cost", self.blood_cost, to=10)
        row = self.labeled_spin(parent, row, "Bones Cost", self.bones_cost, to=30)
        row = self.labeled_spin(parent, row, "Energy Cost", self.energy_cost, to=10)
        ttk.Checkbutton(parent, text="Hide Attack and Health", variable=self.hide_attack_and_health).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        row = self.checkbox_group(parent, row, "Gems Cost", self.gems_cost)

        ttk.Label(parent, text="Categories", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(10, 2))
        row += 1
        row = self.checkbox_group(parent, row, "Tribes", self.tribe_vars, columns=3)
        row = self.checkbox_group(parent, row, "Traits", self.trait_vars, columns=3)
        row = self.labeled_combo(parent, row, "Special Stat Icon", self.special_stat_icon, ["None"] + SPECIAL_STAT_ICONS)
        row = self.checkbox_group(parent, row, "Appearance Behaviours", self.appearance_vars, columns=3)
        row = self.checkbox_group(parent, row, "Meta Categories", self.meta_categories, columns=4)
        row = self.checkbox_group(parent, row, "Abilities", self.ability_vars, columns=4, labels={a["internal"]: a["display"] for a in ABILITIES})
        row = self.checkbox_group(parent, row, "Special Abilities", self.special_ability_vars, columns=4)
        row = self.labeled_entry(parent, row, "Custom Special Abilities (comma-separated)", self.custom_special, width=50)

        ttk.Label(parent, text="Optional Card Links", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(10, 2))
        row += 1
        row = self.labeled_entry(parent, row, "Evolve Into Name", self.evolve_into_name)
        row = self.labeled_spin(parent, row, "Evolve Turns", self.evolve_turns, to=20)
        row = self.labeled_entry(parent, row, "Default Evolution Name", self.default_evolution_name)
        row = self.labeled_entry(parent, row, "Tail Name", self.tail_name)
        row = self.image_entry(parent, row, "Tail Lost Portrait", self.tail_lost_portrait)
        row = self.labeled_entry(parent, row, "Ice Cube Name", self.ice_cube_name)
        ttk.Checkbutton(parent, text="Flip Portrait For Strafe", variable=self.flip_portrait_for_strafe).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        ttk.Checkbutton(parent, text="One Per Deck", variable=self.one_per_deck).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1

        ttk.Label(parent, text="Textures", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(10, 2))
        row += 1
        row = self.image_entry(parent, row, "Texture", self.texture)
        row = self.image_entry(parent, row, "Emission Texture", self.emission_texture)
        row = self.image_entry(parent, row, "Alt Texture", self.alt_texture)
        row = self.image_entry(parent, row, "Alt Emission Texture", self.alt_emission_texture)
        row = self.image_entry(parent, row, "Pixel Texture", self.pixel_texture)
        row = self.image_entry(parent, row, "Title Graphic", self.title_graphic)
        row = self.labeled_entry(parent, row, "Decals (comma-separated)", self.decals, width=50)

        ttk.Label(parent, text="Extension Properties JSON", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(10, 2))
        row += 1
        self.extension_properties = tk.Text(parent, height=4, width=58)
        self.extension_properties.grid(row=row, column=0, columnspan=3, sticky=tk.W)
        row += 1
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
        row = 0
        ttk.Label(parent, text="Sigil Identity", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W)
        row += 1
        row = self.labeled_entry(parent, row, "Name", self.name)
        row = self.labeled_entry(parent, row, "GUID", self.guid)
        row = self.labeled_entry(parent, row, "Description", self.description, width=50)
        row = self.checkbox_group(parent, row, "Meta Categories", self.meta_categories, columns=4)
        row = self.image_entry(parent, row, "Texture", self.texture)
        row = self.image_entry(parent, row, "Pixel Texture", self.pixel_texture)
        row = self.labeled_spin(parent, row, "Power Level", self.power_level, to=99)
        row = self.labeled_spin(parent, row, "Priority", self.priority, to=99)
        ttk.Checkbutton(parent, text="Opponent Usable", variable=self.opponent_usable).grid(row=row, column=1, sticky=tk.W)
        row += 1
        ttk.Checkbutton(parent, text="Can Stack", variable=self.can_stack).grid(row=row, column=1, sticky=tk.W)
        row += 1
        ttk.Checkbutton(parent, text="Is Special Ability", variable=self.is_special_ability).grid(row=row, column=1, sticky=tk.W)
        row += 1

        ttk.Label(parent, text="Activation Cost", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(10, 2))
        row += 1
        row = self.labeled_spin(parent, row, "Bones", self.bones_cost, to=30)
        row = self.labeled_spin(parent, row, "Energy", self.energy_cost, to=10)
        row = self.labeled_spin(parent, row, "Blood", self.blood_cost, to=10)
        ttk.Label(parent, text="Gems").grid(row=row, column=0, sticky=tk.NW)
        gems = ttk.Frame(parent)
        gems.grid(row=row, column=1, sticky=tk.W)
        for gem, var in self.gems_cost.items():
            ttk.Checkbutton(gems, text=gem, variable=var).pack(side=tk.LEFT)
        row += 1

        ttk.Label(parent, text="Ability Behaviour Tree JSON", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(10, 2))
        row += 1
        self.behavior_editor = JSONSchemaTextEditor(parent, self.behavior_schema, [], height=18)
        self.behavior_editor.grid(row=row, column=0, columnspan=3, sticky="nsew")
        row += 1
        self.action_buttons(parent, row, "Save Sigil _sigil.jldr2")

    def selected_gems(self):
        return [gem for gem, var in self.gems_cost.items() if var.get()]

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
        row = 0
        ttk.Label(parent, text="Tribe Definition", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W)
        row += 1
        row = self.labeled_entry(parent, row, "Name", self.name)
        row = self.labeled_entry(parent, row, "GUID", self.guid)
        row = self.image_entry(parent, row, "Tribe Icon", self.tribe_icon)
        ttk.Checkbutton(parent, text="Appear In Tribe Choices", variable=self.appear).grid(row=row, column=1, sticky=tk.W)
        row += 1
        row = self.image_entry(parent, row, "Choice Card Back Texture", self.choice_back)
        ttk.Label(parent, text="Additional Tribes JSON Array", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(10, 2))
        row += 1
        self.extra_tribes = tk.Text(parent, height=8, width=58)
        self.extra_tribes.grid(row=row, column=0, columnspan=3, sticky=tk.W)
        row += 1
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
        row = 0
        ttk.Label(parent, text="Talking Card Sprites", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W)
        row += 1
        row = self.labeled_entry(parent, row, "Card Name", self.card_name)
        row = self.image_entry(parent, row, "Face Sprite", self.face_sprite)
        row = self.image_entry(parent, row, "Eye Open", self.eye_open)
        row = self.image_entry(parent, row, "Eye Closed", self.eye_closed)
        row = self.image_entry(parent, row, "Mouth Open", self.mouth_open)
        row = self.image_entry(parent, row, "Mouth Closed", self.mouth_closed)
        row = self.image_entry(parent, row, "Emission Open", self.emission_open)
        row = self.image_entry(parent, row, "Emission Closed", self.emission_closed)
        row = self.labeled_spin(parent, row, "Blink Rate", self.blink_rate, from_=0.1, to=10, increment=0.1)
        row = self.labeled_combo(parent, row, "Voice ID", self.voice_id, VOICE_IDS)
        row = self.labeled_spin(parent, row, "Voice Pitch", self.voice_pitch, from_=0.1, to=10, increment=0.1)
        ttk.Label(parent, text="Custom Voice").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Entry(parent, textvariable=self.custom_voice, width=34).grid(row=row, column=1, sticky=tk.W, pady=2)
        ttk.Button(parent, text="Browse...", command=lambda: choose_audio(self.custom_voice)).grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1

        ttk.Label(parent, text="Emotion Template", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(10, 2))
        row += 1
        row = self.labeled_combo(parent, row, "Emotion", self.emotion_choice, EMOTION_TYPES)
        ttk.Button(parent, text="Add Emotion", command=self.add_emotion_template).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1

        ttk.Label(parent, text="Emotions JSON Array", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(10, 2))
        row += 1
        self.emotions_editor = JSONSchemaTextEditor(parent, self.emotions_schema, [], height=8)
        self.emotions_editor.grid(row=row, column=0, columnspan=3, sticky="nsew")
        row += 1

        ttk.Label(parent, text="Dialogue Event Template", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(10, 2))
        row += 1
        row = self.labeled_combo(parent, row, "Event Name", self.event_choice, EVENT_NAMES, width=34)
        row = self.labeled_entry(parent, row, "Main Line", self.event_main_line, width=50)
        row = self.labeled_entry(parent, row, "Repeat Line", self.event_repeat_line, width=50)
        ttk.Button(parent, text="Add Dialogue Event", command=self.add_dialogue_event_template).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1

        ttk.Label(parent, text="Dialogue Events JSON Array", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(10, 2))
        row += 1
        self.events_editor = JSONSchemaTextEditor(parent, self.events_schema, [], height=12)
        self.events_editor.grid(row=row, column=0, columnspan=3, sticky="nsew")
        row += 1
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
        self.root.title("Inscryption JSONCardLoader Generator")
        self.root.geometry("1400x900")
        self.root.resizable(True, True)
        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        notebook.add(CardsTab(notebook), text="Cards")
        notebook.add(SigilsTab(notebook), text="Sigils")
        notebook.add(TribesTab(notebook), text="Tribes")
        notebook.add(TalkingCardsTab(notebook), text="Talking Cards")


def main():
    root = tk.Tk()
    JSONCardLoaderGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
