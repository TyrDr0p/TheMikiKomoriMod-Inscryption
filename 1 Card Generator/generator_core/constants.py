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

ABILITY_OPTIONS = [
    "ActivatedDealDamage", "ActivatedDrawSkeleton", "ActivatedEnergyToBones",
    "ActivatedHeal", "ActivatedRandomPowerBone", "ActivatedRandomPowerEnergy",
    "ActivatedSacrificeDrawCards", "ActivatedStatsUp", "ActivatedStatsUpEnergy",
    "AllStrike", "Apparition", "BeesOnHit", "BombSpawner", "BoneDigger",
    "Brittle", "BuffEnemy", "BuffGems", "BuffNeighbours", "CellBuffSelf",
    "CellDrawRandomCardOnDeath", "CellTriStrike", "ConduitBuffAttack",
    "ConduitEnergy", "ConduitFactory", "ConduitHeal", "ConduitNull",
    "ConduitSpawnGems", "CorpseEater", "CreateBells", "CreateDams",
    "CreateEgg", "DeathShield", "Deathtouch", "DebuffEnemy", "DeleteFile",
    "DoubleDeath", "DoubleStrike", "DrawAnt", "DrawCopy", "DrawCopyOnDeath",
    "DrawNewHand", "DrawRabbits", "DrawRandomCardOnDeath", "DrawVesselOnHit",
    "DropRubyOnDeath", "EdaxioArms", "EdaxioHead", "EdaxioLegs", "EdaxioTorso",
    "Evolve", "ExplodeGems", "ExplodeOnDeath", "ExplodingCorpse",
    "FileSizeDamage", "Flying", "GainAttackOnKill", "GainBattery",
    "GainGemBlue", "GainGemGreen", "GainGemOrange", "GainGemTriple",
    "GemDependant", "GemsDraw", "GuardDog", "Haunter", "HydraEgg", "IceCube",
    "LatchBrittle", "LatchDeathShield", "LatchExplodeOnDeath", "Loot",
    "MadeOfStone", "Morsel", "MoveBeside", "OpponentBones", "PermaDeath",
    "PreventAttack", "QuadrupleBones", "RandomAbility", "RandomConsumable",
    "Reach", "Sacrificial", "Sentry", "Sharp", "ShieldGems", "Sinkhole",
    "SkeletonStrafe", "Sniper", "SplitStrike", "SquirrelOrbit",
    "SquirrelStrafe", "SteelTrap", "Strafe", "StrafePush", "StrafeSwap",
    "Submerge", "SubmergeSquid", "SwapStats", "TailOnHit", "Transformer",
    "TripleBlood", "TriStrike", "Tutor", "VirtualReality", "WhackAMole",
]

ABILITIES = [{"display": value, "internal": value, "desc": value} for value in ABILITY_OPTIONS]

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
