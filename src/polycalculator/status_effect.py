from enum import StrEnum, auto


class StatusEffect(StrEnum):
    """A unit status effect."""

    BOOSTED = auto()
    """The unit's movement is increased by 1 and attack is increased by 0.5."""
    CONVERTED = auto()
    """The unit is converted to the enemy's side."""
    FORTIFIED = auto()
    """The unit's defense is increased by 50%."""
    FROZEN = auto()
    """The unit cannot use any actions."""
    POISONED = auto()
    """Reduces a unit's defense by 30% and removes all defense bonuses."""
    SPLASHING = auto()
    """The unit deals splash damage to adjacent enemies."""
    TAKES_RETALIATION = auto()
    """The unit takes retaliation even if it has more range or the SURPRISE trait."""
    VETERAN = auto()
    """The unit's max hp is increased by 1."""
    WALLED = auto()
    """The unit's defense is increased by 300%."""
