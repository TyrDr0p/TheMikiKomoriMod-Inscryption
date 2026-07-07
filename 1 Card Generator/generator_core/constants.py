META_CATEGORIES = [
    "ChoiceNode", "GBCPack", "GBCPlayable", "Part3Random", "Rare",
    "TraderOffer", "AscensionUnlock", "Part1Rulebook", "Part1Modular",
    "Part3Rulebook", "Part3Modular", "BountyHunter", "GrimoraRulebook",
    "MagnificusRulebook", "Part3BuildACard", "AscensionUnlocked",
]

META_CATEGORY_TOOLTIPS = {
    "ChoiceNode": "Defines the card to be a choice option.",
    "GBCPack": "Can be acquired by buying a card pack in act 2.",
    "GBCPlayable": "Can show up in the card catalogue in act 2.",
    "Part3Random": "Can show up as card from the Loot sigil.",
    "Rare": "Defines the card to be rare.",
    "TraderOffer": "Can show up at the trader in act 1.",
    "Part1Rulebook": "Adds the sigil to the act 1 rulebook.",
    "Part1Modular": "Allows the sigil to appear on totems, Wolf Pelt trades and Cave Trial rewards.",
    "Part3Rulebook": "Adds the sigil to the act 3 rulebook.",
    "Part3Modular": "Allows the sigil to appear in the Upgrade node in act 3.",
    "BountyHunter": "Allows the sigil to appear on act 3 Bounty Hunter cards.",
    "GrimoraRulebook": "Adds the sigil to the rulebook in Grimora's part of Finale.",
    "MagnificusRulebook": "Adds the sigil to the rulebook in Magnificus' part of Finale.",
    "Part3BuildACard": "Allows the sigil to be chosen in the Build-A-Bot node in act 3.",
}

TEMPLES = ["Nature", "Undead", "Tech", "Wizard"]
TRIBES = ["Bird", "Canine", "Hooved", "Insect", "Reptile", "Squirrel"]
GEM_TYPES = ["Blue", "Green", "Orange"]
CARD_COMPLEXITIES = ["Vanilla", "Simple", "Intermediate", "Advanced"]
SPECIAL_STAT_ICONS = ["Ants", "Bell", "Bones", "CardsInHand", "GreenGems", "Mirror", "SacrificesThisTurn"]

CARD_COMPLEXITY_TOOLTIPS = {
    "Vanilla": "Will always be a learned card.",
    "Simple": "Will always be an unlocked card.",
    "Intermediate": "Will only be unlocked after tutorial.",
    "Advanced": "Will only be unlocked after tutorial.",
}

TEMPLE_TOOLTIPS = {
    "Nature": "Will show up in act 1 and be in Beast card packs.",
    "Undead": "Will show up in Undead card packs.",
    "Tech": "Will show up in act 3 and Tech card packs.",
    "Wizard": "Will show up in Wizard card packs.",
}

SPECIAL_STAT_ICON_TOOLTIPS = {
    "Ants": "Displays the Ants icon for the card's attack.",
    "Bell": "Displays the Bell icon for the card's attack.",
    "Bones": "Displays the Lammergeier's Bone icon for the card's attack and health.",
    "CardsInHand": "Displays the Hand Counter icon for the card's attack.",
    "GreenGems": "Displays the Green Mox icon for the card's attack.",
    "Mirror": "Displays the Mirror icon for the card's attack.",
    "SacrificesThisTurn": "Displays the Dagger icon for the card's attack.",
}

TRAITS = [
    "Ant", "Bear", "Blind", "DeathcardCreationNonOption", "EatsWarrens",
    "FeedsStoat", "Fused", "Gem", "Giant", "Goat", "Juvenile",
    "KillsSurvivors", "Lice", "LikesHoney", "Pelt", "ProtectsCub",
    "SatisfiesRingTrial", "Structure", "Terrain", "Uncuttable", "Undead", "Wolf",
]

TRAIT_TOOLTIPS = {
    "Ant": "Will increase the attack of cards with the Ant special ability.",
    "DeathcardCreationNonOption": "Cannot be used during creation of the Deathcard.",
    "Fused": "Will render the card as a stitched card in act 2.",
    "Gem": "Will prevent cards with the Gem Dependant sigil from perishing and will explode if ExplodeGems is on the board.",
    "Giant": "Only used for moon.",
    "Goat": "Will grant you the Boon of the Bone Lord, if sacrificed on the Bone Lord's Altar.",
    "KillsSurvivors": "Kills Survivors if used on the campfire.",
    "Lice": "Acts like Pelt Lice.",
    "Pelt": "Cannot be sacrificed, can be traded for cards during the Trapper/Trader fight, and gives no Bone Lord reward.",
    "SatisfiesRingTrial": "Satisfies the ring trial before the moon fight.",
    "Terrain": "Cannot be sacrificed.",
    "Uncuttable": "Immune to scissors and hook items.",
}

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

ABILITY_TOOLTIPS = {
    "ActivatedDealDamage": "When activated for 1 energy, deals 1 damage to opposing card.",
    "ActivatedDrawSkeleton": "When activated for 1 bone, draws a skeleton.",
    "ActivatedEnergyToBones": "Converts energy to bones.",
    "ActivatedHeal": "When activated for 2 bones, heals to full.",
    "ActivatedRandomPowerEnergy": "When activated for 1 energy, gains a random attack boost between 1 and 6 inclusive.",
    "ActivatedSacrificeDrawCards": "When activated, draw 3 cards, then die.",
    "ActivatedStatsUp": "When activated for 2 bones, gain +1/+1.",
    "ActivatedStatsUpEnergy": "When activated for 3 energy, gains +1/+1.",
    "AllStrike": "If there are any opposing cards, it will attack all of them, otherwise it will attack directly.",
    "BeesOnHit": "When taking damage, will add a bee to your hand.",
    "BombSpawner": "Spawns bombs on every empty board slot.",
    "BoneDigger": "At end of turn, add 1 bone.",
    "Brittle": "After card attacks, it dies.",
    "BuffEnemy": "Increase opposing card's attack by 1.",
    "BuffGems": "Increases attack of all gems by 1.",
    "BuffNeighbours": "Increase attack of adjacent cards by 1.",
    "CellBuffSelf": "When within circuit, increase attack by 2.",
    "CellDrawRandomCardOnDeath": "When within circuit, will draw a random card on death.",
    "CellTriStrike": "When within circuit, gains trifurcated strike.",
    "ConduitBuffAttack": "When completing circuit, will increase attack of all cards in circuit by 1.",
    "ConduitEnergy": "When completing circuit, energy doesn't deplete.",
    "ConduitFactory": "When completing circuit, will spawn leepbots in all your available board slots at end of turn.",
    "ConduitHeal": "When completing circuit, will heal all cards in circuit at end of turn.",
    "ConduitNull": "Will complete a circuit.",
    "ConduitSpawnGems": "When completing circuit, will spawn random gems in all your available board slots at end of turn.",
    "CorpseEater": "When another card dies, this card will be played in its slot.",
    "CreateBells": "When played, will spawn bell cards in adjacent slots.",
    "CreateDams": "When played, will spawn dam cards in adjacent slots.",
    "CreateEgg": "When played, spawns a broken egg in the opposing slot, with a 10% chance to spawn a Raven Egg instead.",
    "DeathShield": "When this card would take damage for the first time, it does not.",
    "Deathtouch": "When card deals damage to a card, it dies.",
    "DebuffEnemy": "Decrease opposing card's attack by 1.",
    "DeleteFile": "Nothing unless in archivists boss battle.",
    "DoubleDeath": "When another card dies, it dies again.",
    "DoubleStrike": "Makes the card attack the slot across from it an additional time.",
    "DrawAnt": "When played, add an ant to your hand.",
    "DrawCopy": "When played, will add a copy to your hand.",
    "DrawCopyOnDeath": "When dies, will add a copy to your hand.",
    "DrawNewHand": "Discards your hand and draws 4 new cards.",
    "DrawRabbits": "When played, will add a rabbit to your hand.",
    "DrawRandomCardOnDeath": "Will draw a random card with the Par3Random meta category on death.",
    "DrawVesselOnHit": "When taking damage, will draw a card from side deck.",
    "DropRubyOnDeath": "When card dies, spawn a ruby mox in its place.",
    "Evolve": "After a number of turns based on evolveParams, will turn into a card based on evolveParams.",
    "ExplodeGems": "When a card with the Gem trait dies, will cause them to explode.",
    "ExplodeOnDeath": "When card dies, deals 10 damage to adjacent and opposing card.",
    "FileSizeDamage": "Nothing unless in archivist boss battle.",
    "Flying": "When attacking, will attack directly.",
    "GainAttackOnKill": "Gets +1/+0 for the rest of the battle whenever it kills a creature.",
    "GainBattery": "When played, increases energy and max energy by 1.",
    "GainGemBlue": "Counts as Blue gem cost.",
    "GainGemGreen": "Counts as Green gem cost.",
    "GainGemOrange": "Counts as Orange gem cost.",
    "GainGemTriple": "Counts as all 3 gems when in play.",
    "GemDependant": "When played, and at start of turn, will die if you control no gems.",
    "GuardDog": "When a card is played opposite an empty slot, will move there.",
    "HydraEgg": "Transforms into Hydra if the deck contains cards with 1-5 attack, 1-5 health, and each default tribe.",
    "IceCube": "When card dies, spawns card in slot based on IceCubeParams.",
    "LatchBrittle": "When card dies, you can choose another card to give Brittle.",
    "LatchDeathShield": "When card dies, you can choose another card to give DeathShield.",
    "LatchExplodeOnDeath": "When card dies, you can choose another card to give ExplodeOnDeath.",
    "Loot": "When dealing damage, will draw cards equal to amount.",
    "MadeOfStone": "Invulnerable to Stinky and Deathtouch.",
    "Morsel": "When sacrificed to summon another card, the card will add +1/+2 to the summoned card.",
    "MoveBeside": "Moves to closest space when a card is played.",
    "OpponentBones": "When any enemy card dies, gain 1 bone.",
    "PermaDeath": "When card dies, it is removed from the deck.",
    "PreventAttack": "Prevents opposing card from attacking it.",
    "QuadrupleBones": "When dies, gain 4 bones.",
    "RandomAbility": "When drawn, Sigil becomes a random sigil.",
    "RandomConsumable": "When played, will add a random consumable if you have less than 3.",
    "Reach": "Will block attacking flying card.",
    "Sacrificial": "Can be sacrificed an unlimited number of times.",
    "Sentry": "When a card enters the slot in front of this card, it is dealt 1 damage.",
    "Sharp": "When attacked, will deal 1 damage to attacker.",
    "ShieldGems": "When played, will give cards with the Gem trait DeathShield.",
    "SkeletonStrafe": "Strafe but spawns skeleton in previous slot.",
    "Sniper": "When attacking, you can choose the target slots.",
    "SplitStrike": "When attacking, will attack slots adjacent to opposing slot.",
    "SquirrelOrbit": "No effect on player cards.",
    "SquirrelStrafe": "Strafe but spawns squirrel in previous slot.",
    "SteelTrap": "When card dies, it kills the opposing card, and adds a pelt to your hand.",
    "Strafe": "At end of turn, card moves.",
    "StrafePush": "Strafe but will move other cards with it.",
    "StrafeSwap": "Strafe but will forcibly swap the adjacent card with its current position.",
    "Submerge": "After attacking, will submerge, meaning it can't be attacked.",
    "SubmergeSquid": "Waterborne but becomes random tentacle card on resurface.",
    "SwapStats": "When taking damage, will swap attack and health.",
    "TailOnHit": "When attacked, will move and spawn a card in previous slot based on tailParams, then loses this ability.",
    "Transformer": "Same as evolve with different sigil icon.",
    "TripleBlood": "Counts as 3 blood when sacrificed.",
    "TriStrike": "When attacking, will attack opposing slot, and slots adjacent to opposing slot.",
    "Tutor": "When played, you can choose a card in your deck to add to your hand.",
    "WhackAMole": "When an empty slot is attacked, will move to that slot.",
}

ABILITIES = [{"display": value, "internal": value, "desc": ABILITY_TOOLTIPS.get(value, "")} for value in ABILITY_OPTIONS]

SPECIAL_TRIGGERED_ABILITIES = [
    "Ant", "BellProximity", "BountyHunter", "BrokenCoinLeft", "BrokenCoinRight",
    "CagedWolf", "CardsInHand", "Cat", "Daus", "GiantCard", "GiantMoon",
    "GiantShip", "GreenMage", "JerseyDevil", "Lammergeier", "Mirror",
    "Ouroboros", "PackMule", "RandomCard", "SacrificesThisTurn",
    "ShapeShifter", "SpawnLice", "TalkingCardChooser", "TrapSpawner",
]

SPECIAL_ABILITY_TOOLTIPS = {
    "Ant": "Increases cards attack by 1 for each card with ant trait on the board.",
    "BellProximity": "Damage is equal to 4 - the distance from the bell; adjacent is distance 0.",
    "BountyHunter": "Functions like act 3 Bounty Hunters; only works for opponent.",
    "BrokenCoinLeft": "Functions like Broken Obol (Left).",
    "BrokenCoinRight": "Functions like Broken Obol (Right).",
    "CagedWolf": "Functions like the Caged Wolf card.",
    "CardsInHand": "Damage is equal to the number of cards in player's hand.",
    "Cat": "Functions like the Cat card.",
    "Daus": "Functions like Daus.",
    "GiantCard": "Assigns to all slots on the board; only works for opponent.",
    "GiantMoon": "Renders moon death animation.",
    "GiantShip": "Exclusive to the Limoncello.",
    "GreenMage": "Damage is equal to the number of Green Mox cards you control.",
    "JerseyDevil": "Functions like Child 13.",
    "Lammergeier": "Attack and Health equal the amount of Bones you have divided by 2.",
    "Mirror": "Damage equal to opposing creature.",
    "Ouroboros": "Increases ouroborosDeaths in the save file when it dies.",
    "PackMule": "Grants 4 random cards and a Squirrel when killed.",
    "RandomCard": "Transforms into a random card when drawn.",
    "SacrificesThisTurn": "Grants attack power based on how many sacrifices were made this turn.",
    "ShapeShifter": "Exclusive to Ijiraq.",
    "SpawnLice": "Exclusive to Pelt Lice.",
    "TalkingCardChooser": "Exclusive to talking cards.",
    "TrapSpawner": "Creates a Steel Trap in its place after it perishes.",
}

APPEARANCE_BEHAVIOURS = [
    "AddSnelkDecals", "AlternatingBloodDecal", "AnimatedPortrait",
    "DynamicPortrait", "FullCardPortrait", "GiantAnimatedPortrait",
    "GoldEmission", "HologramPortrait", "RareCardBackground",
    "RareCardColors", "SexyGoat", "StaticGlitch", "TerrainBackground",
    "TerrainLayout", "RedEmission", "DefaultEmission", "MoonParticleEffects",
]

APPEARANCE_BEHAVIOUR_TOOLTIPS = {
    "AddSnelkDecals": "Cycles through the base game's Long Elk decals.",
    "AlternatingBloodDecal": "Renders card with blood decals.",
    "AnimatedPortrait": "Used for animated portraits.",
    "DynamicPortrait": "Renders the card's animated portrait differently.",
    "FullCardPortrait": "Renders the card with no stats.",
    "GiantAnimatedPortrait": "Used for animated portraits on giant cards.",
    "GoldEmission": "Renders the card with gold layout.",
    "HologramPortrait": "Renders portrait as hologram.",
    "RareCardBackground": "Renders card with rare background.",
    "RareCardColors": "Renders card with inverted colours.",
    "SexyGoat": "Renders alternate texture if you have the goat's eyeball.",
    "StaticGlitch": "Renders the card with the static animation.",
    "TerrainBackground": "Renders the card with terrain border.",
    "TerrainLayout": "Renders card with terrain card layout.",
    "RedEmission": "Does the Ijiraq emission effect.",
    "DefaultEmission": "Emissions are on cards by default.",
    "MoonParticleEffects": "Renders the Moon Particle Effects.",
}

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

CONFIGIL_TRIGGER_TYPES = [
    "OnDie", "OnSacrifice", "OnResolveOnBoard", "OnLoad", "OnStruck",
    "OnKill", "OnAttack", "OnPlayerStartOfTurn", "OnPlayerEndOfTurn",
    "OnOpponentStartOfTurn", "OnOpponentEndOfTurn", "OnStartOfTurn",
    "OnEndOfTurn", "OnDamage", "OnDamageDirectly", "OnHealthLevel",
    "OnCombatStart", "OnEnemyCombatStart", "OnDetect", "OnAddedToHand",
    "OnActivate", "OnPreDeath", "OnPreKill", "OnMove", "Passive",
]

CONFIGIL_TRIGGER_TOOLTIPS = {
    "OnDie": "Activates when the card bearing the sigil perishes. Will not trigger when sacrificed.",
    "OnSacrifice": "Activates when the card bearing the sigil is sacrificed.",
    "OnResolveOnBoard": "Activates when the card bearing the sigil is played.",
    "OnLoad": "Activates when the sigil becomes active, for example from a transformed card.",
    "OnStruck": "Activates when the card bearing the sigil receives damage.",
    "OnKill": "Activates when the card bearing the sigil kills another card.",
    "OnAttack": "Activates when the card bearing the sigil performs an attack.",
    "OnPlayerStartOfTurn": "Activates before you draw a card at the start of your turn.",
    "OnPlayerEndOfTurn": "Activates after all your cards have attacked during combat.",
    "OnOpponentStartOfTurn": "Activates before your opponent's cards attack during combat.",
    "OnOpponentEndOfTurn": "Activates after all your opponent's cards have attacked during combat.",
    "OnStartOfTurn": "Activates on the owner's start-of-turn trigger.",
    "OnEndOfTurn": "Activates on the owner's end-of-turn trigger.",
    "OnDamage": "Activates when the card bearing the sigil damages another card.",
    "OnDamageDirectly": "Activates when the card bearing the sigil damages the opponent.",
    "OnHealthLevel": "Activates when the card bearing the sigil is reduced to a specified health value or lower.",
    "OnCombatStart": "Activates when combat starts after ringing the bell.",
    "OnEnemyCombatStart": "Activates when the enemy's turn to attack begins.",
    "OnDetect": "Activates when an enemy card moves into the opposing slot.",
    "OnAddedToHand": "Activates when the card bearing the sigil is created in the player's hand.",
    "OnActivate": "Defines the sigil as an activated one. Required for activationCost.",
    "OnPreDeath": "Activates right before the card bearing the sigil would perish.",
    "OnPreKill": "Activates right before the card bearing the sigil would kill another card.",
    "OnMove": "Activates when the card bearing the sigil moves to another slot.",
    "Passive": "Renders the sigil active every frame.",
}

CONFIGIL_ACTION_TYPES = [
    "placeCards", "buffCards", "transformCards", "damageSlots", "attackSlots",
    "extraAttacks", "gainCurrency", "dealScaleDamage", "drawCards",
    "chooseSlots", "moveCards", "showMessage",
]

CONFIGIL_ACTION_TOOLTIPS = {
    "placeCards": "Place cards directly on the board.",
    "buffCards": "Buff or debuff cards already on the board.",
    "transformCards": "Transform cards on the board into other cards.",
    "damageSlots": "Directly damage slots; empty slots deal damage to the opponent.",
    "attackSlots": "Make cards perform attacks against chosen slots.",
    "extraAttacks": "Make cards perform additional attacks during combat.",
    "gainCurrency": "Gain or lose resources such as bones, energy, or foils.",
    "dealScaleDamage": "Deal direct damage to the scales.",
    "drawCards": "Create cards directly in the owner's hand.",
    "chooseSlots": "Allow the owner to manually choose slots for the effect.",
    "moveCards": "Move cards around the board.",
    "showMessage": "Display dialogue on screen.",
}

CONFIGIL_ACTION_ORDER = [
    "chooseSlots", "showMessage", "gainCurrency", "dealScaleDamage",
    "drawCards", "placeCards", "transformCards", "changeAppearance",
    "buffCards", "moveCards", "damageSlots", "attackSlots",
]

CONFIGIL_FIELD_TOOLTIPS = {
    "condition": "Optional expression. The effect only runs when this evaluates to true.",
    "slot": "Slot index. Configils indexes slots from 0 on the far left to 3 on the far right. Expressions are allowed.",
    "targetCard": "Specific card to affect. Variables such as [BaseCard] can be used.",
    "card": "Internal card name to place, draw, or transform into.",
    "retainMods": "Whether the created/transformed card retains stat buffs and transferred sigils.",
    "replace": "Whether this effect can replace a card already in the target slot.",
    "stats": "Stats are written as ATK/HP. Negative values reduce stats.",
    "damage": "Amount of damage dealt by the effect. Expressions are allowed.",
    "currency": "Positive values add resources. Negative values remove resources.",
    "messageLength": "How many seconds the message should display. Default is 2.",
}

CONFIGIL_MESSAGE_EMOTIONS = ["Neutral", "Laughter", "Anger", "Quiet", "Surprise", "Curious"]
CONFIGIL_LETTER_ANIMATIONS = ["Jitter", "WavyJitter", "None"]
CONFIGIL_SPEAKERS = [
    "Single", "Leshy", "Stoat", "Stinkbug", "Wolf", "Mushroom", "P03",
    "Goo", "Trader", "P03Archivist", "P03Photographer", "P03Telegrapher",
    "P03Canvas", "P03Librarians", "P03BountyHunter", "Grimora",
    "Magnificus", "AnglerTalkingCard", "P03MycologistMain",
    "P03MycologistSide", "Bonelord", "PirateSkull",
]

CONFIGIL_STRAFE_DIRECTIONS = ["normal", "right", "left"]
