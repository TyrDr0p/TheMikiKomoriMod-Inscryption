import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None

# ------------------------------------------------------------
# ENUMS & DATA
# ------------------------------------------------------------
META_CATEGORIES = [
    "ChoiceNode", "GBCPack", "GBCPlayable", "Part3Random", "Rare",
    "TraderOffer", "AscensionUnlock", "Part1Rulebook", "Part1Modular",
    "Part3Rulebook", "Part3Modular", "BountyHunter", "GrimoraRulebook",
    "MagnificusRulebook", "Part3BuildACard", "AscensionUnlocked"
]
TEMPLES = ["Nature", "Undead", "Tech", "Wizard"]
TRIBES = ["Bird", "Canine", "Hooved", "Insect", "Reptile", "Squirrel"]
GEM_TYPES = ["Blue", "Green", "Orange"]
SPECIAL_STAT_ICONS = ["Ants", "Bell", "Bones", "CardsInHand", "GreenGems", "Mirror", "SacrificesThisTurn"]
TRAITS = [
    "Ant", "Bear", "Blind", "DeathcardCreationNonOption", "EatsWarrens",
    "FeedsStoat", "Fused", "Gem", "Giant", "Goat", "Juvenile",
    "KillsSurvivors", "Lice", "LikesHoney", "Pelt", "ProtectsCub",
    "SatisfiesRingTrial", "Structure", "Terrain", "Uncuttable", "Undead", "Wolf"
]
ABILITIES = [
    {"display": "Airborne", "internal": "Flying", "desc": "Attacks directly over opposing creatures."},
    {"display": "Mighty Leap", "internal": "Reach", "desc": "Blocks Airborne creatures."},
    {"display": "Touch of Death", "internal": "TouchOfDeath", "desc": "Instantly kills any creature it damages."},
    {"display": "Many Lives", "internal": "ManyLives", "desc": "Does not perish when sacrificed."},
    {"display": "Fledgling", "internal": "Fledgling", "desc": "Grows into a stronger form after one turn."},
    {"display": "Bifurcated Strike", "internal": "BifurcatedStrike", "desc": "Strikes left and right spaces."},
    {"display": "Trifurcated Strike", "internal": "TriStrike", "desc": "Strikes left, right, and center."},
    {"display": "Waterborne", "internal": "Waterborne", "desc": "Submerges on opponent's turn."},
    {"display": "Unkillable", "internal": "Unkillable", "desc": "Returns to hand when it perishes."},
    {"display": "Guardian", "internal": "Guardian", "desc": "Moves to block an empty space."},
    {"display": "Sharp Quills", "internal": "Sharp", "desc": "Deals 1 damage to its attacker."},
    {"display": "Worthy Sacrifice", "internal": "TripleBlood", "desc": "Counts as 3 blood when sacrificed."},
    {"display": "Sentry", "internal": "Sentry", "desc": "Deals 1 damage to the opposing creature when played."},
    {"display": "Stinky", "internal": "Stinky", "desc": "Reduces the attack of opposing creatures by 1."},
    {"display": "Ant Spawner", "internal": "AntSpawner", "desc": "Spawns an Ant in your hand when played."},
    {"display": "Rabbit Hole", "internal": "RabbitHole", "desc": "Spawns a Rabbit in your hand when played."},
    {"display": "Beehive", "internal": "Beehive", "desc": "Spawns a Bee in your hand when damaged."},
    {"display": "Fecundity", "internal": "Fecundity", "desc": "When played, create a copy of this card in your hand."},
    {"display": "Bone Digger", "internal": "BoneDigger", "desc": "Gain 1 bone when this card perishes."},
    {"display": "Brittle", "internal": "Brittle", "desc": "Dies after attacking."},
    {"display": "Broken", "internal": "Broken", "desc": "Has no attack."},
    {"display": "Burrower", "internal": "Burrower", "desc": "Moves to a random space when attacked."},
    {"display": "Deathburst", "internal": "ExplodeOnDeath", "desc": "Deals 1 damage to all opposing creatures when it perishes."},
    {"display": "Sniper", "internal": "Sniper", "desc": "Can attack any space on the opponent's side."},
    {"display": "Double Strike", "internal": "DoubleStrike", "desc": "Attacks twice."},
    {"display": "Lone Wolf", "internal": "LoneWolf", "desc": "Gains +1 attack if it's the only creature on your side."},
    {"display": "Morsel", "internal": "Morsel", "desc": "When sacrificed, grants its stats to the creature it was sacrificed to."},
    {"display": "Pack Rat", "internal": "PackRat", "desc": "When played, adds a random item to your inventory."},
    {"display": "Pathfinder", "internal": "Pathfinder", "desc": "Moves to a random empty space at the start of your turn."},
    {"display": "Sprinter", "internal": "Sprinter", "desc": "Moves to the rightmost empty space at the start of your turn."},
    {"display": "Steel Trap", "internal": "SteelTrap", "desc": "When an opposing creature moves into this card's space, it is destroyed."},
    {"display": "Submerge", "internal": "Submerge", "desc": "Cannot be attacked until it attacks."},
    {"display": "Thick Hide", "internal": "ThickHide", "desc": "Reduces damage taken by 1."},
    {"display": "Corpse Eater", "internal": "CorpseEater", "desc": "When another creature dies, this card takes its place."},
    {"display": "Loot", "internal": "Loot", "desc": "When dealing damage, draw cards equal to the damage dealt."},
    {"display": "Made of Stone", "internal": "MadeOfStone", "desc": "Immune to Stinky and Touch of Death."},
    {"display": "Bees on Hit", "internal": "BeesOnHit", "desc": "When damaged, add a Bee to your hand."},
    {"display": "Quadruple Bones", "internal": "QuadrupleBones", "desc": "When it perishes, gain 4 bones."},
    {"display": "Skeleton Strafe", "internal": "SkeletonStrafe", "desc": "Moves at end of turn and spawns a Skeleton in its old spot."},
    {"display": "Squirrel Strafe", "internal": "SquirrelStrafe", "desc": "Moves at end of turn and spawns a Squirrel in its old spot."},
    {"display": "Strafe", "internal": "Strafe", "desc": "Moves to a random empty space at the end of your turn."},
    {"display": "Strafe Push", "internal": "StrafePush", "desc": "Strafe but pushes adjacent creatures along."},
    {"display": "Strafe Swap", "internal": "StrafeSwap", "desc": "Strafe but swaps with the adjacent creature."},
    {"display": "Submerge Squid", "internal": "SubmergeSquid", "desc": "Submerges and resurfaced as a random Tentacle."},
    {"display": "Swap Stats", "internal": "SwapStats", "desc": "When damaged, swaps its Attack and Health."},
    {"display": "Tail on Hit", "internal": "TailOnHit", "desc": "When damaged, moves and spawns a tail creature."},
    {"display": "Transformer", "internal": "Transformer", "desc": "Evolves after a set number of turns."},
    {"display": "Whack a Mole", "internal": "WhackAMole", "desc": "Moves to an empty slot when that slot is attacked."},
    {"display": "Conduit (Energy)", "internal": "ConduitEnergy", "desc": "When completing a circuit, energy does not deplete."},
    {"display": "Conduit (Factory)", "internal": "ConduitFactory", "desc": "When completing a circuit, spawns Leepbots at end of turn."},
    {"display": "Conduit (Heal)", "internal": "ConduitHeal", "desc": "When completing a circuit, heals all cards in the circuit."},
    {"display": "Conduit (Null)", "internal": "ConduitNull", "desc": "Counts as a conduit for circuits."},
    {"display": "Conduit (Buff Attack)", "internal": "ConduitBuffAttack", "desc": "When completing a circuit, gives +1 attack to all cards in circuit."},
    {"display": "Conduit (Spawn Gems)", "internal": "ConduitSpawnGems", "desc": "When completing a circuit, spawns gems at end of turn."},
    {"display": "Cell Buff Self", "internal": "CellBuffSelf", "desc": "If in a circuit, +2 attack."},
    {"display": "Cell Draw Random Card on Death", "internal": "CellDrawRandomCardOnDeath", "desc": "If in a circuit, draw a random card on death."},
    {"display": "Cell Tri Strike", "internal": "CellTriStrike", "desc": "If in a circuit, gains trifurcated strike."},
    {"display": "Gem Dependant", "internal": "GemDependant", "desc": "Dies if you control no gems at start of turn."},
    {"display": "Gain Blue Gem", "internal": "GainGemBlue", "desc": "Counts as a Blue Gem in play."},
    {"display": "Gain Green Gem", "internal": "GainGemGreen", "desc": "Counts as a Green Gem in play."},
    {"display": "Gain Orange Gem", "internal": "GainGemOrange", "desc": "Counts as an Orange Gem in play."},
    {"display": "Gain Triple Gem", "internal": "GainGemTriple", "desc": "Counts as all three gems in play."},
    {"display": "Explode Gems", "internal": "ExplodeGems", "desc": "When a card with the Gem trait dies, it explodes."},
    {"display": "Shield Gems", "internal": "ShieldGems", "desc": "When played, gives Death Shield to all cards with the Gem trait."},
    {"display": "Drop Ruby on Death", "internal": "DropRubyOnDeath", "desc": "When it perishes, spawns a Ruby Mox."},
    {"display": "Spawn Bombs", "internal": "BombSpawner", "desc": "When played, spawns Bombs in all empty slots."},
    {"display": "Create Dams", "internal": "CreateDams", "desc": "When played, spawns Dams in adjacent slots."},
    {"display": "Create Bells", "internal": "CreateBells", "desc": "When played, spawns Bell cards in adjacent slots."},
]
SPECIAL_TRIGGERED_ABILITIES = [
    "Ant", "BellProximity", "BountyHunter", "BrokenCoinLeft", "BrokenCoinRight",
    "CagedWolf", "CardsInHand", "Cat", "Daus", "GiantCard", "GiantMoon",
    "GiantShip", "GreenMage", "JerseyDevil", "Lammergeier", "Mirror",
    "Ouroboros", "PackMule", "RandomCard", "SacrificesThisTurn",
    "ShapeShifter", "SpawnLice", "TalkingCardChooser", "TrapSpawner"
]
APPEARANCE_BEHAVIOURS = [
    "AddSnelkDecals", "AlternatingBloodDecal", "AnimatedPortrait",
    "DynamicPortrait", "FullCardPortrait", "GiantAnimatedPortrait",
    "GoldEmission", "HologramPortrait", "RareCardBackground",
    "RareCardColors", "SexyGoat", "StaticGlitch", "TerrainBackground",
    "TerrainLayout", "RedEmission", "DefaultEmission", "MoonParticleEffects"
]


def normalize_texture_path(texture_path):
    if not texture_path:
        return ""
    normalized = texture_path.strip().replace("\\", "/")
    if os.path.isabs(normalized):
        return os.path.basename(normalized)
    return normalized


def build_card_data(
    card_id,
    mod_prefix,
    displayed_name,
    description,
    base_attack,
    base_health,
    blood_cost,
    bones_cost,
    energy_cost,
    gem_cost,
    tribe,
    temple,
    trait,
    special_stat_icon,
    appearance_behaviour,
    portrait_path,
    meta_categories,
    abilities,
    special_abilities,
):
    card_data = {"name": card_id}

    if mod_prefix:
        card_data["modPrefix"] = mod_prefix

    card_data.update({
        "displayedName": displayed_name,
        "description": description,
    })

    if meta_categories:
        card_data["metaCategories"] = meta_categories

    card_data.update({
        "cardComplexity": "Vanilla",
        "temple": temple if temple else "Nature",
        "baseAttack": base_attack,
        "baseHealth": base_health,
    })

    if blood_cost > 0:
        card_data["bloodCost"] = blood_cost
    if bones_cost > 0:
        card_data["bonesCost"] = bones_cost
    if energy_cost > 0:
        card_data["energyCost"] = energy_cost
    if gem_cost and gem_cost != "None":
        card_data["gemsCost"] = [gem_cost]
    if special_stat_icon and special_stat_icon != "None":
        card_data["specialStatIcon"] = special_stat_icon
    if tribe and tribe != "None":
        card_data["tribes"] = [tribe]
    if trait and trait != "None":
        card_data["traits"] = [trait]
    if special_abilities:
        card_data["specialAbilities"] = special_abilities
    if abilities:
        card_data["abilities"] = abilities
    if appearance_behaviour and appearance_behaviour != "None":
        card_data["appearanceBehaviour"] = [appearance_behaviour]

    texture = normalize_texture_path(portrait_path)
    if texture:
        card_data["texture"] = texture

    return card_data


# Talking Card enums
VOICE_IDS = ["None", "female1_voice", "kobold_voice", "cat_voice"]
EMOTION_TYPES = ["Laughter", "Anger", "Quiet", "Surprise", "Curious"]
EVENT_NAMES = [
    "OnDrawn", "OnPlayFromHand", "OnAttacked", "OnBecomeSelectablePositive",
    "OnBecomeSelectableNegative", "OnSacrificed", "OnSelectedForDeckTrial",
    "OnSelectedForCardMerge", "OnSelectedForCardRemove", "OnDiscoveredInExploration",
    "ProspectorBoss", "AnglerBoss", "TrapperTraderBoss", "LeshyBoss",
    "RoyalBoss", "DefaultOpponent"
]

# ------------------------------------------------------------
# TOOLTIP CLASS
# ------------------------------------------------------------
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind('<Enter>', self.show)
        widget.bind('<Leave>', self.hide)

    def show(self, event=None):
        if self.tip_window or not self.text:
            return
        if event is not None:
            x = event.x_root + 15
            y = event.y_root + 15
        else:
            x = self.widget.winfo_pointerx() + 15
            y = self.widget.winfo_pointery() + 15
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("Arial", 9))
        label.pack()

    def hide(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

# ------------------------------------------------------------
# MAIN APP WITH TABS
# ------------------------------------------------------------
class CardGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inscryption Card Generator - Card & Talking Card Editor")
        self.root.geometry("1300x900")
        self.root.resizable(True, True)

        # Main notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create tabs
        self.card_tab = ttk.Frame(self.notebook)
        self.talking_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.card_tab, text="Card Editor")
        self.notebook.add(self.talking_tab, text="Talking Card Editor")

        # Build each tab
        self.build_card_tab()
        self.build_talking_tab()

    # ------------------------------------------------------------
    # CARD TAB (with mod prefix)
    # ------------------------------------------------------------
    def build_card_tab(self):
        # Variables
        self.card_id = tk.StringVar(value="Stoat")
        self.mod_prefix = tk.StringVar(value="MyMod")
        self.displayed_name = tk.StringVar(value="Stoat")
        self.description = tk.StringVar(value="A cunning creature.")
        self.base_attack = tk.IntVar(value=2)
        self.base_health = tk.IntVar(value=2)
        self.blood_cost = tk.IntVar(value=0)
        self.bones_cost = tk.IntVar(value=0)
        self.energy_cost = tk.IntVar(value=0)
        self.gem_cost = tk.StringVar(value="None")
        self.tribe = tk.StringVar(value="None")
        self.temple = tk.StringVar(value="Nature")
        self.special_stat_icon = tk.StringVar(value="None")
        self.trait = tk.StringVar(value="None")
        self.appearance_behaviour = tk.StringVar(value="None")
        self.portrait_path = tk.StringVar(value="")
        self.meta_categories = {cat: tk.BooleanVar(value=False) for cat in META_CATEGORIES}
        self.ability_vars = {}
        self.special_triggered_vars = {}

        # Layout: left panel (form) and right panel (preview)
        main_frame = ttk.Frame(self.card_tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,10))

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Scrollable left form
        canvas = tk.Canvas(left_frame, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Form fields
        row = 0

        # Mod prefix
        ttk.Label(scrollable_frame, text="Mod Prefix (optional, no spaces)", font=("Arial", 10, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(10,2))
        row += 1
        ttk.Label(scrollable_frame, text="Prefix").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.mod_prefix, width=20).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1

        # Card ID (without prefix)
        ttk.Label(scrollable_frame, text="Card ID (unique, no spaces)", font=("Arial", 10, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(10,2))
        row += 1
        ttk.Label(scrollable_frame, text="Card ID").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.card_id, width=35).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1

        # Displayed name
        ttk.Label(scrollable_frame, text="Displayed Name").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.displayed_name, width=35).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1

        # Description
        ttk.Label(scrollable_frame, text="Description").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.description, width=45).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1

        # Stats & Costs
        ttk.Label(scrollable_frame, text="Stats & Costs", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(10,5))
        row += 1
        ttk.Label(scrollable_frame, text="Attack").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Spinbox(scrollable_frame, from_=0, to=99, textvariable=self.base_attack, width=5).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        ttk.Label(scrollable_frame, text="Health").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Spinbox(scrollable_frame, from_=0, to=99, textvariable=self.base_health, width=5).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        ttk.Label(scrollable_frame, text="Blood Cost").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Spinbox(scrollable_frame, from_=0, to=10, textvariable=self.blood_cost, width=5).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        ttk.Label(scrollable_frame, text="Bones Cost").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Spinbox(scrollable_frame, from_=0, to=10, textvariable=self.bones_cost, width=5).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        ttk.Label(scrollable_frame, text="Energy Cost").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Spinbox(scrollable_frame, from_=0, to=10, textvariable=self.energy_cost, width=5).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        ttk.Label(scrollable_frame, text="Gem Cost").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Combobox(scrollable_frame, textvariable=self.gem_cost, values=["None"] + GEM_TYPES, state="readonly", width=15).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1

        # Categories
        ttk.Label(scrollable_frame, text="Categories", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(10,5))
        row += 1
        ttk.Label(scrollable_frame, text="Tribe").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Combobox(scrollable_frame, textvariable=self.tribe, values=["None"] + TRIBES, state="readonly", width=20).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        ttk.Label(scrollable_frame, text="Temple").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Combobox(scrollable_frame, textvariable=self.temple, values=TEMPLES, state="readonly", width=20).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        ttk.Label(scrollable_frame, text="Trait").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Combobox(scrollable_frame, textvariable=self.trait, values=["None"] + TRAITS, state="readonly", width=25).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        ttk.Label(scrollable_frame, text="Special Stat Icon").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Combobox(scrollable_frame, textvariable=self.special_stat_icon, values=["None"] + SPECIAL_STAT_ICONS, state="readonly", width=20).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        ttk.Label(scrollable_frame, text="Appearance Behaviour").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Combobox(scrollable_frame, textvariable=self.appearance_behaviour, values=["None"] + APPEARANCE_BEHAVIOURS, state="readonly", width=25).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1

        # Meta Categories
        ttk.Label(scrollable_frame, text="Meta Categories", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(10,5))
        row += 1
        meta_frame = ttk.Frame(scrollable_frame)
        meta_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        col = 0
        for cat, var in self.meta_categories.items():
            ttk.Checkbutton(meta_frame, text=cat, variable=var).grid(row=col//4, column=col%4, sticky=tk.W, padx=2)
            col += 1
        row += 1

        # Abilities
        ttk.Label(scrollable_frame, text="Abilities (Sigils)", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(10,5))
        row += 1
        ability_frame = ttk.Frame(scrollable_frame)
        ability_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        col = 0
        row_inner = 0
        for ability in ABILITIES:
            var = tk.BooleanVar(value=False)
            self.ability_vars[ability["internal"]] = var
            cb = ttk.Checkbutton(ability_frame, text=ability["display"], variable=var)
            cb.grid(row=row_inner, column=col, sticky=tk.W, padx=2)
            ToolTip(cb, ability["desc"])
            col += 1
            if col > 3:
                col = 0
                row_inner += 1
        row += row_inner + 1

        # Special Triggered
        ttk.Label(scrollable_frame, text="Special Triggered Abilities", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(10,5))
        row += 1
        special_frame = ttk.Frame(scrollable_frame)
        special_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        col = 0
        row_inner = 0
        for sta in SPECIAL_TRIGGERED_ABILITIES:
            var = tk.BooleanVar(value=False)
            self.special_triggered_vars[sta] = var
            cb = ttk.Checkbutton(special_frame, text=sta, variable=var)
            cb.grid(row=row_inner, column=col, sticky=tk.W, padx=2)
            col += 1
            if col > 3:
                col = 0
                row_inner += 1
        row += row_inner + 1

        # Custom Special Abilities
        ttk.Label(scrollable_frame, text="Custom Special Abilities (mod-added, comma-separated)").grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(10,5))
        row += 1
        self.special_abilities = tk.StringVar(value="")
        ttk.Entry(scrollable_frame, textvariable=self.special_abilities, width=50).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        row += 1

        # Portrait
        ttk.Label(scrollable_frame, text="Portrait Image", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(10,5))
        row += 1
        ttk.Label(scrollable_frame, text="Image Path").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.portrait_path, width=35).grid(row=row, column=1, sticky=tk.W, pady=2)
        ttk.Button(scrollable_frame, text="Browse...", command=lambda: self.browse_image(self.portrait_path)).grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1

        # Generate button
        ttk.Button(scrollable_frame, text="Generate .jldr2 File", command=self.generate_card_json).grid(row=row, column=0, columnspan=2, pady=20)

        # Bind updates
        self.card_id.trace('w', self.update_card_preview)
        self.mod_prefix.trace('w', self.update_card_preview)
        self.displayed_name.trace('w', self.update_card_preview)
        self.description.trace('w', self.update_card_preview)
        self.base_attack.trace('w', self.update_card_preview)
        self.base_health.trace('w', self.update_card_preview)
        self.blood_cost.trace('w', self.update_card_preview)
        self.bones_cost.trace('w', self.update_card_preview)
        self.energy_cost.trace('w', self.update_card_preview)
        self.gem_cost.trace('w', self.update_card_preview)
        self.tribe.trace('w', self.update_card_preview)
        self.temple.trace('w', self.update_card_preview)
        self.trait.trace('w', self.update_card_preview)
        self.special_stat_icon.trace('w', self.update_card_preview)
        self.appearance_behaviour.trace('w', self.update_card_preview)
        self.portrait_path.trace('w', self.update_card_preview)
        for var in self.meta_categories.values():
            var.trace('w', self.update_card_preview)
        for var in self.ability_vars.values():
            var.trace('w', self.update_card_preview)
        for var in self.special_triggered_vars.values():
            var.trace('w', self.update_card_preview)

        # Card preview canvas
        self.card_preview_canvas = tk.Canvas(right_frame, width=350, height=520, bg="#f0e6d3")
        self.card_preview_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.card_portrait_image = None
        self.update_card_preview()

    def browse_image(self, path_var):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")]
        )
        if file_path:
            path_var.set(file_path)

    def update_card_preview(self, *args):
        canvas = self.card_preview_canvas
        canvas.delete("all")

        w = 320
        h = 460
        x0 = (canvas.winfo_width() - w) // 2 if canvas.winfo_width() > w else 20
        y0 = 20
        x1 = x0 + w
        y1 = y0 + h

        # Background
        canvas.create_rectangle(x0, y0, x1, y1, fill="#e8d6b5", outline="#4a3520", width=3)

        # Portrait
        img_path = self.portrait_path.get()
        if img_path and (Image is None or ImageTk is None):
            canvas.create_text(
                x0 + w//2,
                y0 + 130,
                text="Install Pillow to preview portraits.",
                font=("Arial", 10),
                fill="#7a3325",
                width=w-50
            )
        elif img_path and os.path.exists(img_path):
            try:
                pil_img = Image.open(img_path)
                pil_img.thumbnail((150, 150))
                self.card_portrait_image = ImageTk.PhotoImage(pil_img)
                canvas.create_image(x0 + w//2, y0 + 120, image=self.card_portrait_image)
            except Exception:
                pass

        # Name
        name = self.displayed_name.get() or "Card Name"
        canvas.create_text(x0 + w//2, y0 + 30, text=name, font=("Arial", 16, "bold"), fill="#2b1a0a")

        # Description
        desc = self.description.get() or "Description"
        canvas.create_text(x0 + w//2, y0 + 70, text=desc, font=("Arial", 10), fill="#2b1a0a", width=w-40)

        # Costs
        blood = self.blood_cost.get()
        if blood > 0:
            cx = x0 + 30
            cy = y1 - 30
            canvas.create_oval(cx-12, cy-12, cx+12, cy+12, fill="red", outline="darkred")
            canvas.create_text(cx, cy, text=str(blood), font=("Arial", 14, "bold"), fill="white")

        bones = self.bones_cost.get()
        if bones > 0:
            cx = x0 + 30 + 40
            cy = y1 - 30
            canvas.create_polygon(cx-10, cy+10, cx-5, cy-10, cx, cy+5, cx+5, cy-10, cx+10, cy+10, fill="white", outline="black")
            canvas.create_text(cx, cy+2, text=str(bones), font=("Arial", 10, "bold"), fill="black")

        energy = self.energy_cost.get()
        if energy > 0:
            cx = x0 + 30 + 80
            cy = y1 - 30
            canvas.create_rectangle(cx-10, cy-10, cx+10, cy+10, fill="yellow", outline="orange")
            canvas.create_text(cx, cy, text=str(energy), font=("Arial", 12, "bold"), fill="black")

        gem = self.gem_cost.get()
        if gem != "None" and gem:
            cx = x0 + 30 + 120
            cy = y1 - 30
            colors = {"Blue": "blue", "Green": "green", "Orange": "orange"}
            canvas.create_oval(cx-8, cy-8, cx+8, cy+8, fill=colors.get(gem, "gray"), outline="black")
            canvas.create_text(cx, cy, text="G", font=("Arial", 8, "bold"), fill="white")

        # Attack / Health
        atk = self.base_attack.get()
        cx = x1 - 30
        cy = y1 - 20
        canvas.create_line(cx-8, cy+8, cx+8, cy-8, fill="black", width=3)
        canvas.create_line(cx-8, cy+8, cx-12, cy+12, fill="black", width=3)
        canvas.create_line(cx+8, cy-8, cx+12, cy-12, fill="black", width=3)
        canvas.create_text(cx, cy, text=str(atk), font=("Arial", 14, "bold"), fill="black")

        hp = self.base_health.get()
        cx = x1 - 70
        cy = y1 - 20
        canvas.create_polygon(cx-12, cy+10, cx, cy-12, cx+12, cy+10, fill="lightblue", outline="blue")
        canvas.create_text(cx, cy, text=str(hp), font=("Arial", 14, "bold"), fill="black")

        # Tribe, Temple, Stat Icon
        tribe = self.tribe.get()
        if tribe != "None" and tribe:
            canvas.create_text(x0 + w - 30, y0 + 10, text=tribe, font=("Arial", 10, "bold"), fill="#4a3520")
        temple = self.temple.get()
        if temple:
            canvas.create_text(x0 + 30, y0 + 10, text=temple, font=("Arial", 10, "bold"), fill="#4a3520")
        stat_icon = self.special_stat_icon.get()
        if stat_icon != "None" and stat_icon:
            canvas.create_text(x0 + w//2, y1 - 50, text=f"[{stat_icon}]", font=("Arial", 10), fill="#4a3520")

        # Abilities (icons)
        selected_abilities = [name for name, var in self.ability_vars.items() if var.get()]
        if selected_abilities:
            icon_size = 26
            spacing = 8
            max_display = 6
            total_width = min(len(selected_abilities), max_display) * (icon_size + spacing) - spacing
            start_x = x0 + (w - total_width) // 2
            y_icon = y0 + 280
            for i, ab_internal in enumerate(selected_abilities[:max_display]):
                ab_display = next((a["display"] for a in ABILITIES if a["internal"] == ab_internal), ab_internal)
                cx = start_x + i * (icon_size + spacing) + icon_size//2
                canvas.create_rectangle(cx-icon_size//2, y_icon-icon_size//2,
                                        cx+icon_size//2, y_icon+icon_size//2,
                                        fill="#d4b48c", outline="#4a3520")
                abbr = ab_display[:2].upper()
                canvas.create_text(cx, y_icon, text=abbr, font=("Arial", 8, "bold"), fill="black")

        # Special Triggered
        selected_sta = [name for name, var in self.special_triggered_vars.items() if var.get()]
        if selected_sta:
            sta_text = "STA: " + ", ".join(selected_sta[:3])
            canvas.create_text(x0 + w//2, y0 + 320, text=sta_text, font=("Arial", 8), fill="#4a3520")

    def generate_card_json(self):
        card_id = self.card_id.get().strip()
        if not card_id:
            messagebox.showerror("Error", "Card ID is required.")
            return
        if " " in card_id:
            messagebox.showerror("Error", "Card ID must not contain spaces.")
            return

        prefix = self.mod_prefix.get().strip()
        if prefix:
            if " " in prefix:
                messagebox.showerror("Error", "Mod prefix must not contain spaces.")
                return
            suggested_filename = f"{prefix}_{card_id}"
        else:
            suggested_filename = card_id

        displayed_name = self.displayed_name.get().strip() or "Unnamed"
        description = self.description.get().strip() or ""
        attack = self.base_attack.get()
        health = self.base_health.get()
        blood = self.blood_cost.get()
        bones = self.bones_cost.get()
        energy = self.energy_cost.get()
        gem = self.gem_cost.get()
        tribe = self.tribe.get()
        temple = self.temple.get()
        trait = self.trait.get()
        stat_icon = self.special_stat_icon.get()
        appearance = self.appearance_behaviour.get()
        portrait = self.portrait_path.get().strip()

        meta_categories = [cat for cat, var in self.meta_categories.items() if var.get()]
        abilities = [ab_internal for ab_internal, var in self.ability_vars.items() if var.get()]
        special_triggered = [sta for sta, var in self.special_triggered_vars.items() if var.get()]
        custom_special = [s.strip() for s in self.special_abilities.get().split(",") if s.strip()]

        special_abilities = special_triggered + custom_special

        card_data = build_card_data(
            card_id=card_id,
            mod_prefix=prefix,
            displayed_name=displayed_name,
            description=description,
            base_attack=attack,
            base_health=health,
            blood_cost=blood,
            bones_cost=bones,
            energy_cost=energy,
            gem_cost=gem,
            tribe=tribe,
            temple=temple,
            trait=trait,
            special_stat_icon=stat_icon,
            appearance_behaviour=appearance,
            portrait_path=portrait,
            meta_categories=meta_categories,
            abilities=abilities,
            special_abilities=special_abilities,
        )

        file_path = filedialog.asksaveasfilename(
            defaultextension=".jldr2",
            filetypes=[("JSON Card Loader 2", "*.jldr2"), ("All Files", "*.*")],
            initialfile=f"{suggested_filename}.jldr2"
        )
        if not file_path:
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(card_data, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Success", f"Card saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

    # ------------------------------------------------------------
    # TALKING CARD TAB
    # ------------------------------------------------------------
    def build_talking_tab(self):
        # Variables
        self.talk_card_name = tk.StringVar(value="MyMod_Stoat")
        self.talk_face_sprite = tk.StringVar(value="")
        self.talk_eye_open = tk.StringVar(value="")
        self.talk_eye_closed = tk.StringVar(value="")
        self.talk_mouth_open = tk.StringVar(value="")
        self.talk_mouth_closed = tk.StringVar(value="")
        self.talk_emission_open = tk.StringVar(value="")
        self.talk_emission_closed = tk.StringVar(value="")
        self.talk_blink_rate = tk.DoubleVar(value=1.5)
        self.talk_voice_id = tk.StringVar(value="None")
        self.talk_voice_pitch = tk.DoubleVar(value=1.0)
        self.talk_custom_voice = tk.StringVar(value="")
        # Emotions: list of dicts
        self.emotions = []
        # Dialogue events: list of dicts with eventName, mainLines, repeatLines
        self.dialogue_events = []

        # Layout: form on left, preview on right (text summary)
        main_frame = ttk.Frame(self.talking_tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,10))

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Scrollable left form
        canvas = tk.Canvas(left_frame, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        row = 0

        # Card Name
        ttk.Label(scrollable_frame, text="Target Card Name (full ID)", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(10,5))
        row += 1
        ttk.Label(scrollable_frame, text="Card Name").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.talk_card_name, width=40).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1

        # Face Sprite
        ttk.Label(scrollable_frame, text="Face Sprite", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(10,5))
        row += 1
        ttk.Label(scrollable_frame, text="Face").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.talk_face_sprite, width=30).grid(row=row, column=1, sticky=tk.W, pady=2)
        ttk.Button(scrollable_frame, text="Browse...", command=lambda: self.browse_image(self.talk_face_sprite)).grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1

        # Eye Sprites
        ttk.Label(scrollable_frame, text="Eye Sprites", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(10,5))
        row += 1
        ttk.Label(scrollable_frame, text="Open").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.talk_eye_open, width=30).grid(row=row, column=1, sticky=tk.W, pady=2)
        ttk.Button(scrollable_frame, text="Browse...", command=lambda: self.browse_image(self.talk_eye_open)).grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1
        ttk.Label(scrollable_frame, text="Closed").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.talk_eye_closed, width=30).grid(row=row, column=1, sticky=tk.W, pady=2)
        ttk.Button(scrollable_frame, text="Browse...", command=lambda: self.browse_image(self.talk_eye_closed)).grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1

        # Mouth Sprites
        ttk.Label(scrollable_frame, text="Mouth Sprites", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(10,5))
        row += 1
        ttk.Label(scrollable_frame, text="Open").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.talk_mouth_open, width=30).grid(row=row, column=1, sticky=tk.W, pady=2)
        ttk.Button(scrollable_frame, text="Browse...", command=lambda: self.browse_image(self.talk_mouth_open)).grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1
        ttk.Label(scrollable_frame, text="Closed").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.talk_mouth_closed, width=30).grid(row=row, column=1, sticky=tk.W, pady=2)
        ttk.Button(scrollable_frame, text="Browse...", command=lambda: self.browse_image(self.talk_mouth_closed)).grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1

        # Emission Sprites
        ttk.Label(scrollable_frame, text="Emission Sprites", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(10,5))
        row += 1
        ttk.Label(scrollable_frame, text="Open").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.talk_emission_open, width=30).grid(row=row, column=1, sticky=tk.W, pady=2)
        ttk.Button(scrollable_frame, text="Browse...", command=lambda: self.browse_image(self.talk_emission_open)).grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1
        ttk.Label(scrollable_frame, text="Closed").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.talk_emission_closed, width=30).grid(row=row, column=1, sticky=tk.W, pady=2)
        ttk.Button(scrollable_frame, text="Browse...", command=lambda: self.browse_image(self.talk_emission_closed)).grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1

        # Face Info
        ttk.Label(scrollable_frame, text="Face Info", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(10,5))
        row += 1
        ttk.Label(scrollable_frame, text="Blink Rate (0.1-10)").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Spinbox(scrollable_frame, from_=0.1, to=10.0, increment=0.1, textvariable=self.talk_blink_rate, width=10).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        ttk.Label(scrollable_frame, text="Voice ID (select None to omit)").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Combobox(scrollable_frame, textvariable=self.talk_voice_id, values=VOICE_IDS, state="readonly", width=20).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        ttk.Label(scrollable_frame, text="Voice Pitch (0.1-10)").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Spinbox(scrollable_frame, from_=0.1, to=10.0, increment=0.1, textvariable=self.talk_voice_pitch, width=10).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        ttk.Label(scrollable_frame, text="Custom Voice (audio file)").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Entry(scrollable_frame, textvariable=self.talk_custom_voice, width=30).grid(row=row, column=1, sticky=tk.W, pady=2)
        ttk.Button(scrollable_frame, text="Browse...", command=lambda: self.browse_audio(self.talk_custom_voice)).grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1

        # Emotions (simple list management)
        ttk.Label(scrollable_frame, text="Emotions (optional)", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(10,5))
        row += 1
        self.emotions_frame = ttk.Frame(scrollable_frame)
        self.emotions_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        ttk.Button(scrollable_frame, text="Add Emotion", command=self.add_emotion).grid(row=row+1, column=0, sticky=tk.W, pady=5)
        row += 2

        # Dialogue Events
        ttk.Label(scrollable_frame, text="Dialogue Events", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(10,5))
        row += 1
        self.events_frame = ttk.Frame(scrollable_frame)
        self.events_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        ttk.Button(scrollable_frame, text="Add Dialogue Event", command=self.add_dialogue_event).grid(row=row+1, column=0, sticky=tk.W, pady=5)
        row += 2

        # Generate button
        ttk.Button(scrollable_frame, text="Generate .jldr2 File", command=self.generate_talking_json).grid(row=row, column=0, columnspan=2, pady=20)

        # Preview (right side) - just a text summary
        self.talk_preview_text = tk.Text(right_frame, height=30, width=50, state=tk.DISABLED)
        self.talk_preview_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.update_talking_preview()

        # Bind updates
        self.talk_card_name.trace('w', self.update_talking_preview)
        self.talk_face_sprite.trace('w', self.update_talking_preview)
        self.talk_eye_open.trace('w', self.update_talking_preview)
        self.talk_eye_closed.trace('w', self.update_talking_preview)
        self.talk_mouth_open.trace('w', self.update_talking_preview)
        self.talk_mouth_closed.trace('w', self.update_talking_preview)
        self.talk_emission_open.trace('w', self.update_talking_preview)
        self.talk_emission_closed.trace('w', self.update_talking_preview)
        self.talk_blink_rate.trace('w', self.update_talking_preview)
        self.talk_voice_id.trace('w', self.update_talking_preview)
        self.talk_voice_pitch.trace('w', self.update_talking_preview)
        self.talk_custom_voice.trace('w', self.update_talking_preview)

    def browse_audio(self, path_var):
        file_path = filedialog.askopenfilename(
            filetypes=[("Audio files", "*.mp3 *.wav *.ogg *.aiff *.aif"), ("All files", "*.*")]
        )
        if file_path:
            path_var.set(file_path)

    # ---- Emotions management ----
    def add_emotion(self):
        emotion_data = {
            "emotion": tk.StringVar(value="Laughter"),
            "faceSprite": tk.StringVar(value=""),
            "eyeOpen": tk.StringVar(value=""),
            "eyeClosed": tk.StringVar(value=""),
            "mouthOpen": tk.StringVar(value=""),
            "mouthClosed": tk.StringVar(value=""),
            "emissionOpen": tk.StringVar(value=""),
            "emissionClosed": tk.StringVar(value=""),
        }
        self.emotions.append(emotion_data)
        self.redraw_emotions()

    def remove_emotion(self, index):
        del self.emotions[index]
        self.redraw_emotions()

    def redraw_emotions(self):
        for widget in self.emotions_frame.winfo_children():
            widget.destroy()

        for i, ed in enumerate(self.emotions):
            frame = ttk.Frame(self.emotions_frame, relief=tk.GROOVE, borderwidth=2)
            frame.pack(fill=tk.X, pady=5)
            ttk.Label(frame, text="Emotion:").grid(row=0, column=0, sticky=tk.W)
            ttk.Combobox(frame, textvariable=ed["emotion"], values=EMOTION_TYPES, state="readonly", width=12).grid(row=0, column=1, sticky=tk.W, padx=5)
            ttk.Label(frame, text="Face:").grid(row=0, column=2, sticky=tk.W, padx=(10,0))
            ttk.Entry(frame, textvariable=ed["faceSprite"], width=15).grid(row=0, column=3, sticky=tk.W, padx=2)
            ttk.Button(frame, text="...", width=2, command=lambda v=ed["faceSprite"]: self.browse_image(v)).grid(row=0, column=4)
            ttk.Label(frame, text="Eye Open:").grid(row=1, column=0, sticky=tk.W)
            ttk.Entry(frame, textvariable=ed["eyeOpen"], width=15).grid(row=1, column=1, sticky=tk.W, padx=5)
            ttk.Button(frame, text="...", width=2, command=lambda v=ed["eyeOpen"]: self.browse_image(v)).grid(row=1, column=2)
            ttk.Label(frame, text="Closed:").grid(row=1, column=3, sticky=tk.W)
            ttk.Entry(frame, textvariable=ed["eyeClosed"], width=15).grid(row=1, column=4, sticky=tk.W, padx=2)
            ttk.Button(frame, text="...", width=2, command=lambda v=ed["eyeClosed"]: self.browse_image(v)).grid(row=1, column=5)
            ttk.Label(frame, text="Mouth Open:").grid(row=2, column=0, sticky=tk.W)
            ttk.Entry(frame, textvariable=ed["mouthOpen"], width=15).grid(row=2, column=1, sticky=tk.W, padx=5)
            ttk.Button(frame, text="...", width=2, command=lambda v=ed["mouthOpen"]: self.browse_image(v)).grid(row=2, column=2)
            ttk.Label(frame, text="Closed:").grid(row=2, column=3, sticky=tk.W)
            ttk.Entry(frame, textvariable=ed["mouthClosed"], width=15).grid(row=2, column=4, sticky=tk.W, padx=2)
            ttk.Button(frame, text="...", width=2, command=lambda v=ed["mouthClosed"]: self.browse_image(v)).grid(row=2, column=5)
            ttk.Label(frame, text="Emission Open:").grid(row=3, column=0, sticky=tk.W)
            ttk.Entry(frame, textvariable=ed["emissionOpen"], width=15).grid(row=3, column=1, sticky=tk.W, padx=5)
            ttk.Button(frame, text="...", width=2, command=lambda v=ed["emissionOpen"]: self.browse_image(v)).grid(row=3, column=2)
            ttk.Label(frame, text="Closed:").grid(row=3, column=3, sticky=tk.W)
            ttk.Entry(frame, textvariable=ed["emissionClosed"], width=15).grid(row=3, column=4, sticky=tk.W, padx=2)
            ttk.Button(frame, text="...", width=2, command=lambda v=ed["emissionClosed"]: self.browse_image(v)).grid(row=3, column=5)
            ttk.Button(frame, text="Remove Emotion", command=lambda idx=i: self.remove_emotion(idx)).grid(row=4, column=0, columnspan=6, pady=5)

        self.update_talking_preview()

    # ---- Dialogue Events management ----
    def add_dialogue_event(self):
        event_data = {
            "eventName": tk.StringVar(value="OnDrawn"),
            "mainLines": tk.StringVar(value=""),
            "repeatLines": []  # list of StringVar for each repeat set
        }
        self.dialogue_events.append(event_data)
        self.redraw_events()

    def remove_dialogue_event(self, index):
        del self.dialogue_events[index]
        self.redraw_events()

    def add_repeat_line_set(self, event_idx):
        self.dialogue_events[event_idx]["repeatLines"].append(tk.StringVar(value=""))
        self.redraw_events()

    def remove_repeat_line_set(self, event_idx, repeat_idx):
        del self.dialogue_events[event_idx]["repeatLines"][repeat_idx]
        self.redraw_events()

    def redraw_events(self):
        for widget in self.events_frame.winfo_children():
            widget.destroy()

        for i, ev in enumerate(self.dialogue_events):
            frame = ttk.Frame(self.events_frame, relief=tk.GROOVE, borderwidth=2)
            frame.pack(fill=tk.X, pady=5)

            ttk.Label(frame, text="Event:").grid(row=0, column=0, sticky=tk.W)
            ttk.Combobox(frame, textvariable=ev["eventName"], values=EVENT_NAMES, state="readonly", width=20).grid(row=0, column=1, sticky=tk.W, padx=5)

            ttk.Label(frame, text="Main Lines (one per line):").grid(row=1, column=0, sticky=tk.NW, padx=(0,5))
            main_text = tk.Text(frame, height=3, width=30)
            main_text.grid(row=1, column=1, columnspan=3, sticky=tk.W, pady=2)
            if ev["mainLines"].get():
                main_text.insert("1.0", ev["mainLines"].get())
            def update_main(event, idx=i):
                self.dialogue_events[idx]["mainLines"].set(main_text.get("1.0", tk.END).strip())
            main_text.bind("<KeyRelease>", update_main)

            ttk.Label(frame, text="Repeat Lines (sets):").grid(row=2, column=0, sticky=tk.NW, padx=(0,5))
            repeat_frame = ttk.Frame(frame)
            repeat_frame.grid(row=2, column=1, columnspan=3, sticky=tk.W)
            for j, rvar in enumerate(ev["repeatLines"]):
                rframe = ttk.Frame(repeat_frame)
                rframe.pack(fill=tk.X, pady=2)
                ttk.Label(rframe, text=f"Set {j+1}:").pack(side=tk.LEFT, padx=2)
                rentry = ttk.Entry(rframe, textvariable=rvar, width=40)
                rentry.pack(side=tk.LEFT, padx=2)
                ttk.Button(rframe, text="X", width=2, command=lambda idx_i=i, idx_j=j: self.remove_repeat_line_set(idx_i, idx_j)).pack(side=tk.LEFT, padx=2)
            ttk.Button(repeat_frame, text="Add Repeat Line Set", command=lambda idx=i: self.add_repeat_line_set(idx)).pack(pady=2)

            ttk.Button(frame, text="Remove Event", command=lambda idx=i: self.remove_dialogue_event(idx)).grid(row=3, column=0, columnspan=4, pady=5)

        self.update_talking_preview()

    def update_talking_preview(self, *args):
        summary = []
        summary.append("=== Talking Card Configuration ===\n")
        summary.append(f"Card Name: {self.talk_card_name.get()}")
        summary.append(f"Face Sprite: {self.talk_face_sprite.get()}")
        summary.append(f"Eye Open: {self.talk_eye_open.get()}")
        summary.append(f"Eye Closed: {self.talk_eye_closed.get()}")
        summary.append(f"Mouth Open: {self.talk_mouth_open.get()}")
        summary.append(f"Mouth Closed: {self.talk_mouth_closed.get()}")
        summary.append(f"Emission Open: {self.talk_emission_open.get()}")
        summary.append(f"Emission Closed: {self.talk_emission_closed.get()}")
        summary.append(f"Blink Rate: {self.talk_blink_rate.get()}")
        voice_id = self.talk_voice_id.get()
        summary.append(f"Voice ID: {voice_id if voice_id != 'None' else '(omitted)'}")
        summary.append(f"Voice Pitch: {self.talk_voice_pitch.get()}")
        summary.append(f"Custom Voice: {self.talk_custom_voice.get()}")
        summary.append("\n--- Emotions ---")
        if self.emotions:
            for i, ed in enumerate(self.emotions):
                summary.append(f"Emotion {i+1}: {ed['emotion'].get()}")
                summary.append(f"  Face: {ed['faceSprite'].get()}")
                summary.append(f"  Eye Open: {ed['eyeOpen'].get()}, Closed: {ed['eyeClosed'].get()}")
                summary.append(f"  Mouth Open: {ed['mouthOpen'].get()}, Closed: {ed['mouthClosed'].get()}")
                summary.append(f"  Emission Open: {ed['emissionOpen'].get()}, Closed: {ed['emissionClosed'].get()}")
        else:
            summary.append("None")
        summary.append("\n--- Dialogue Events ---")
        if self.dialogue_events:
            for i, ev in enumerate(self.dialogue_events):
                summary.append(f"Event {i+1}: {ev['eventName'].get()}")
                main_lines = ev["mainLines"].get().splitlines()
                summary.append("  Main Lines:")
                for line in main_lines:
                    if line.strip():
                        summary.append(f"    \"{line}\"")
                if ev["repeatLines"]:
                    summary.append("  Repeat Line Sets:")
                    for j, rvar in enumerate(ev["repeatLines"]):
                        lines = [l.strip() for l in rvar.get().splitlines() if l.strip()]
                        summary.append(f"    Set {j+1}: {lines}")
                else:
                    summary.append("  Repeat Lines: None")
        else:
            summary.append("None")

        self.talk_preview_text.config(state=tk.NORMAL)
        self.talk_preview_text.delete("1.0", tk.END)
        self.talk_preview_text.insert("1.0", "\n".join(summary))
        self.talk_preview_text.config(state=tk.DISABLED)

    def generate_talking_json(self):
        # Validate required fields
        card_name = self.talk_card_name.get().strip()
        if not card_name:
            messagebox.showerror("Error", "Card Name is required.")
            return
        face_sprite = self.talk_face_sprite.get().strip()
        if not face_sprite:
            messagebox.showerror("Error", "Face Sprite is required.")
            return
        eye_open = self.talk_eye_open.get().strip()
        eye_closed = self.talk_eye_closed.get().strip()
        if not eye_open or not eye_closed:
            messagebox.showerror("Error", "Both Eye Open and Closed sprites are required.")
            return
        mouth_open = self.talk_mouth_open.get().strip()
        mouth_closed = self.talk_mouth_closed.get().strip()
        if not mouth_open or not mouth_closed:
            messagebox.showerror("Error", "Both Mouth Open and Closed sprites are required.")
            return
        emission_open = self.talk_emission_open.get().strip()
        emission_closed = self.talk_emission_closed.get().strip()
        if not emission_open or not emission_closed:
            messagebox.showerror("Error", "Both Emission Open and Closed sprites are required.")
            return

        # Build JSON
        talking_data = {
            "cardName": card_name,
            "faceSprite": face_sprite,
            "eyeSprites": {
                "open": eye_open,
                "closed": eye_closed
            },
            "mouthSprites": {
                "open": mouth_open,
                "closed": mouth_closed
            },
            "emissionSprites": {
                "open": emission_open,
                "closed": emission_closed
            },
            "faceInfo": {}
        }

        # Optional faceInfo fields – only include if set (and not "None")
        if self.talk_blink_rate.get() != 1.5:  # default
            talking_data["faceInfo"]["blinkRate"] = self.talk_blink_rate.get()
        voice_id = self.talk_voice_id.get()
        if voice_id != "None":
            talking_data["faceInfo"]["voiceId"] = voice_id
        if self.talk_voice_pitch.get() != 1.0:
            talking_data["faceInfo"]["voiceSoundPitch"] = self.talk_voice_pitch.get()
        if self.talk_custom_voice.get().strip():
            talking_data["faceInfo"]["customVoice"] = self.talk_custom_voice.get().strip()

        # If faceInfo is empty, remove it
        if not talking_data["faceInfo"]:
            del talking_data["faceInfo"]

        # Emotions
        emotions_list = []
        for ed in self.emotions:
            emotion = ed["emotion"].get()
            if not emotion:
                continue
            emotion_obj = {"emotion": emotion}
            if ed["faceSprite"].get().strip():
                emotion_obj["faceSprite"] = ed["faceSprite"].get().strip()
            if ed["eyeOpen"].get().strip() and ed["eyeClosed"].get().strip():
                emotion_obj["eyeSprites"] = {
                    "open": ed["eyeOpen"].get().strip(),
                    "closed": ed["eyeClosed"].get().strip()
                }
            if ed["mouthOpen"].get().strip() and ed["mouthClosed"].get().strip():
                emotion_obj["mouthSprites"] = {
                    "open": ed["mouthOpen"].get().strip(),
                    "closed": ed["mouthClosed"].get().strip()
                }
            if ed["emissionOpen"].get().strip() and ed["emissionClosed"].get().strip():
                emotion_obj["emissionSprites"] = {
                    "open": ed["emissionOpen"].get().strip(),
                    "closed": ed["emissionClosed"].get().strip()
                }
            emotions_list.append(emotion_obj)
        if emotions_list:
            talking_data["emotions"] = emotions_list

        # Dialogue Events
        events_list = []
        for ev in self.dialogue_events:
            event_name = ev["eventName"].get()
            if not event_name:
                continue
            main_lines = [l.strip() for l in ev["mainLines"].get().splitlines() if l.strip()]
            if not main_lines:
                continue
            repeat_lines = []
            for rvar in ev["repeatLines"]:
                lines = [l.strip() for l in rvar.get().splitlines() if l.strip()]
                if lines:
                    repeat_lines.append(lines)
            # The schema requires at least one repeatLines set, even if empty? Actually minItems: 1, but can be empty string? Better to ensure at least one set with empty lines.
            if not repeat_lines:
                # Provide one empty set to satisfy minItems
                repeat_lines = [[]]
            event_obj = {
                "eventName": event_name,
                "mainLines": main_lines,
                "repeatLines": repeat_lines
            }
            events_list.append(event_obj)
        if not events_list:
            messagebox.showerror("Error", "At least one Dialogue Event with main lines is required.")
            return
        talking_data["dialogueEvents"] = events_list

        # Save file – now .jldr2
        file_path = filedialog.asksaveasfilename(
            defaultextension=".jldr2",
            filetypes=[("JSON Card Loader 2", "*.jldr2"), ("All Files", "*.*")],
            initialfile=f"Talking_{card_name}.jldr2"
        )
        if not file_path:
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(talking_data, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Success", f"Talking card saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
def main():
    root = tk.Tk()
    app = CardGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
