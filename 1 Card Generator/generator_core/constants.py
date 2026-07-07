META_CATEGORIES = [
    "ChoiceNode", "GBCPack", "GBCPlayable", "Part3Random", "Rare",
    "TraderOffer", "AscensionUnlock", "Part1Rulebook", "Part1Modular",
    "Part3Rulebook", "Part3Modular", "BountyHunter", "GrimoraRulebook",
    "MagnificusRulebook", "Part3BuildACard", "AscensionUnlocked",
]

TEMPLES = ["Nature", "Undead", "Tech", "Wizard"]
TRIBES = ["Bird", "Canine", "Hooved", "Insect", "Reptile", "Squirrel"]
GEM_TYPES = ["Blue", "Green", "Orange"]
CARD_COMPLEXITIES = ["Vanilla", "Simple", "Intermediate", "Advanced"]
SPECIAL_STAT_ICONS = ["Ants", "Bell", "Bones", "CardsInHand", "GreenGems", "Mirror", "SacrificesThisTurn"]
TRAITS = [
    "Ant", "Bear", "Blind", "DeathcardCreationNonOption", "EatsWarrens",
    "FeedsStoat", "Fused", "Gem", "Giant", "Goat", "Juvenile",
    "KillsSurvivors", "Lice", "LikesHoney", "Pelt", "ProtectsCub",
    "SatisfiesRingTrial", "Structure", "Terrain", "Uncuttable", "Undead", "Wolf",
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
    {"display": "Squirrel Strafe", "internal": "SquirrelStrafe", "desc": "Moves at end of turn and spawns a Squirrel."},
    {"display": "Strafe", "internal": "Strafe", "desc": "Moves to a random empty space at the end of your turn."},
    {"display": "Strafe Push", "internal": "StrafePush", "desc": "Strafe but pushes adjacent creatures along."},
    {"display": "Strafe Swap", "internal": "StrafeSwap", "desc": "Strafe but swaps with the adjacent creature."},
    {"display": "Submerge Squid", "internal": "SubmergeSquid", "desc": "Submerges and resurfaces as a random Tentacle."},
    {"display": "Swap Stats", "internal": "SwapStats", "desc": "When damaged, swaps Attack and Health."},
    {"display": "Tail on Hit", "internal": "TailOnHit", "desc": "When damaged, moves and spawns a tail creature."},
    {"display": "Transformer", "internal": "Transformer", "desc": "Evolves after a set number of turns."},
    {"display": "Whack a Mole", "internal": "WhackAMole", "desc": "Moves to an empty slot when that slot is attacked."},
    {"display": "Conduit (Energy)", "internal": "ConduitEnergy", "desc": "When completing a circuit, energy does not deplete."},
    {"display": "Conduit (Factory)", "internal": "ConduitFactory", "desc": "When completing a circuit, spawns Leepbots."},
    {"display": "Conduit (Heal)", "internal": "ConduitHeal", "desc": "When completing a circuit, heals cards."},
    {"display": "Conduit (Null)", "internal": "ConduitNull", "desc": "Counts as a conduit for circuits."},
    {"display": "Conduit (Buff Attack)", "internal": "ConduitBuffAttack", "desc": "Gives +1 attack to cards in circuit."},
    {"display": "Conduit (Spawn Gems)", "internal": "ConduitSpawnGems", "desc": "Spawns gems at end of turn."},
    {"display": "Cell Buff Self", "internal": "CellBuffSelf", "desc": "If in a circuit, +2 attack."},
    {"display": "Cell Draw Random Card on Death", "internal": "CellDrawRandomCardOnDeath", "desc": "If in a circuit, draw a random card on death."},
    {"display": "Cell Tri Strike", "internal": "CellTriStrike", "desc": "If in a circuit, gains trifurcated strike."},
    {"display": "Gem Dependant", "internal": "GemDependant", "desc": "Dies if you control no gems."},
    {"display": "Gain Blue Gem", "internal": "GainGemBlue", "desc": "Counts as a Blue Gem in play."},
    {"display": "Gain Green Gem", "internal": "GainGemGreen", "desc": "Counts as a Green Gem in play."},
    {"display": "Gain Orange Gem", "internal": "GainGemOrange", "desc": "Counts as an Orange Gem in play."},
    {"display": "Gain Triple Gem", "internal": "GainGemTriple", "desc": "Counts as all three gems in play."},
    {"display": "Explode Gems", "internal": "ExplodeGems", "desc": "When a Gem trait card dies, it explodes."},
    {"display": "Shield Gems", "internal": "ShieldGems", "desc": "Gives Death Shield to Gem trait cards."},
    {"display": "Drop Ruby on Death", "internal": "DropRubyOnDeath", "desc": "Spawns a Ruby Mox on death."},
    {"display": "Spawn Bombs", "internal": "BombSpawner", "desc": "Spawns Bombs in empty slots."},
    {"display": "Create Dams", "internal": "CreateDams", "desc": "Spawns Dams in adjacent slots."},
    {"display": "Create Bells", "internal": "CreateBells", "desc": "Spawns Bell cards in adjacent slots."},
]

SPECIAL_TRIGGERED_ABILITIES = [
    "Ant", "BellProximity", "BountyHunter", "BrokenCoinLeft", "BrokenCoinRight",
    "CagedWolf", "CardsInHand", "Cat", "Daus", "GiantCard", "GiantMoon",
    "GiantShip", "GreenMage", "JerseyDevil", "Lammergeier", "Mirror",
    "Ouroboros", "PackMule", "RandomCard", "SacrificesThisTurn",
    "ShapeShifter", "SpawnLice", "TalkingCardChooser", "TrapSpawner",
]

APPEARANCE_BEHAVIOURS = [
    "AddSnelkDecals", "AlternatingBloodDecal", "AnimatedPortrait",
    "DynamicPortrait", "FullCardPortrait", "GiantAnimatedPortrait",
    "GoldEmission", "HologramPortrait", "RareCardBackground",
    "RareCardColors", "SexyGoat", "StaticGlitch", "TerrainBackground",
    "TerrainLayout", "RedEmission", "DefaultEmission", "MoonParticleEffects",
]

VOICE_IDS = ["None", "female1_voice", "kobold_voice", "cat_voice"]
EMOTION_TYPES = ["Laughter", "Anger", "Quiet", "Surprise", "Curious"]
EVENT_NAMES = [
    "OnDrawn", "OnPlayFromHand", "OnAttacked", "OnBecomeSelectablePositive",
    "OnBecomeSelectableNegative", "OnSacrificed", "OnSelectedForDeckTrial",
    "OnSelectedForCardMerge", "OnSelectedForCardRemove", "OnDiscoveredInExploration",
    "ProspectorBoss", "AnglerBoss", "TrapperTraderBoss", "LeshyBoss",
    "RoyalBoss", "DefaultOpponent",
]

SIGIL_BEHAVIOR_TEMPLATE = [
    {
        "trigger": {
            "triggerType": "OnResolveOnBoard",
            "activatesForCardsWithCondition": "",
        }
    }
]

