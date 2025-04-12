from enum import StrEnum, auto


class Trait(StrEnum):
    """A unit trait."""

    # Normal
    CARRY = auto()
    """
    Allows a unit to carry another unit inside.
    A unit with the carry skill can move to a land tile adjacent to water.
    Doing so releases the unit it was carrying and ends the unit's turn.
    """
    CONVERT = auto()
    """Allows a unit to convert an enemy unit into a friendly unit by attacking it."""
    DASH = auto()
    """Allows a unit to attack after moving in the same turn."""
    ESCAPE = auto()
    """Allows a unit to move after attacking in the same turn."""
    FORTIFY = auto()
    """Allows a unit to receive a defence bonus in a city."""
    HEAL = auto()
    """
    Gives a unit the Heal Others unit action, which
    heals all adjacent friendly units by up to 4 HP.
    """
    PERSIST = auto()
    """
    Allows a unit to attack again immediately after killing an enemy unit.
    There is no limit on the number of kills in a single turn.
    """
    SCOUT = auto()
    """Allows a unit to explore a 5x5 area instead of a 3x3 area."""
    SPLASH = auto()
    """Allows a unit to damage or poison enemy units adjacent to the targeted unit."""
    STATIC = auto()
    """Prevents a unit from becoming a veteran."""
    STIFF = auto()
    """Prevents a unit from retaliating when attacked by an enemy unit."""
    STOMP = auto()
    """Causes a unit to deal damage to all adjacent enemy units when it moves."""
    SURPRISE = auto()
    """
    Prevents a unit from triggering retaliation attacks when attacking an enemy unit.
    """
    # Cloak
    CREEP = auto()
    """Allows a unit to ignore movement barriers imposed by terrain."""
    HIDE = auto()
    """Allows a unit to hide itself and become invisible to enemies when it moves."""
    INFILTRATE = auto()
    """Allows a unit to incite a revolt and spawn Daggers by entering an enemy city."""
    # Aquarion
    AUTOFLOOD = auto()
    """Allows a unit to automatically flood any tile it moves onto."""
    DRENCH = auto()
    """Allows a unit to flood any tile it attacks."""
    TENTACLES = auto()
    """
    Allows a unit to damage any enemy that moves next to it,
    as well as when it moves next to an enemy or when it is trained.
    """
    # Elyrion
    GROW = auto()
    """Allows a unit to grow into a different unit after a given number of turns."""
    INDEPENDENT = auto()
    """
    Units with this skill do not take up a population slot in or belong to any city.
    """
    # Polaris
    AUTO_FREEZE = auto()
    """
    Allows a unit to automatically freeze adjacent enemy units and water tiles
    (turning them into ice tiles) as it moves.
    """
    FREEZE = auto()
    """Allows a unit to freeze enemy units it attacks."""
    FREEZE_AREA = auto()
    """
    Gives a unit the Freeze Area unit action, which freezes adjacent enemy units,
    freezes adjacent water tiles into ice tiles, and converts adjacent land tiles to the
    style of the tribe the unit belongs to.
    """
    SKATE = auto()
    """
    Doubles movement on ice but limits movement to one and prohibits the use of the
    dash and escape skills on land.
    """
    # Cymanti
    BOOST = auto()
    """
    Gives a unit the Boost unit action, which boosts all adjacent friendly units by
    increasing their attack by 0.5 and movement by 1 until their next action
    (excluding moving).
    """
    EAT = auto()
    """Allows a unit to grow in length for every kill."""
    EXPLODE = auto()
    """
    Gives a unit the Explode unit action, which damages using the unit's attack value
    and poisons all adjacent enemy units, kills the unit itself, and leaves in its place
    spores (on land) or Algae (on water).
    """
    NAVIGATE = auto()
    """
    Allows a unit to move in ocean even if no prerequisite
    technology is researched but prevents the unit from moving
    onto land, except for capturing cities and villages.
    """
    POISON = auto()
    """Allows a unit to poison enemy units it attacks."""
    SNEAK = auto()
    """Allows a unit to ignore movement barriers imposed by enemy units."""
