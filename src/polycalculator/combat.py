from fractions import Fraction
from polycalculator.status_effect import StatusEffect
from polycalculator.trait import Trait
from polycalculator.unit import Unit, UnitBuilder

from typing import NamedTuple


class CombatResult(NamedTuple):
    """
    The result of a combat between two units.

    Attributes
    ----------
        damage_to_attacker : Fraction
            The amount of damage done to the attacker.
        damage_to_defender : Fraction
            The amount of damage done to the defender.
        attacker_status_effects : set[StatusEffect]
            The status effects applied to the attacker.
        defender_status_effects : set[StatusEffect]
            The status effects applied to the defender.

    """

    damage_to_attacker: Fraction
    damage_to_defender: Fraction
    attacker_status_effects: set[StatusEffect]
    defender_status_effects: set[StatusEffect]


def _round_away_from_zero(x: Fraction) -> Fraction:
    """
    Round a Fraction away from zero.

    This is needed because Python's built-in round function rounds to the nearest even number
    when the number is exactly halfway between two integers. This function rounds away from zero.

    Parameters
    ----------
        x : Fraction
            The number to round.

    Returns
    -------
        Fraction
            The fraction rounded away from zero.
    """
    if x >= 0:
        return Fraction(int(x + Fraction(1, 2)), 1)
    else:
        return Fraction(int(x - Fraction(1, 2)), 1)


def single_combat(attacker: Unit, defender: Unit) -> CombatResult:
    """
    Simulate a single combat between two units.

    Parameters
    ----------
        attacker : Unit
            The attacking unit.
        defender : Unit
            The defending unit.

    Returns
    -------
        CombatResult
            The damage done and status effects applied to the attacker and defender.
    """
    tentacle_damage = Fraction(0)
    # FUTURE: If another tentacles unit is added, this probably isn't going to work.
    if Trait.TENTACLES in defender.traits and Trait.TENTACLES not in attacker.traits:
        _, tentacle_damage, _, _ = single_combat(
            UnitBuilder(defender).with_attack(2).build(), attacker
        )
        attacker = (
            UnitBuilder(attacker)
            .with_current_hp(attacker.current_hp - tentacle_damage)
            .build()
        )

    attack_force = attacker.attack * (attacker.current_hp / attacker.max_hp)
    defense_force = (
        defender.defense
        * (defender.current_hp / defender.max_hp)
        * defender.defense_bonus
    )
    total_damage = attack_force + defense_force
    attack_result = _round_away_from_zero(
        (attack_force / total_damage) * attacker.attack * Fraction(4.5)
    )
    defense_result = _round_away_from_zero(
        (defense_force / total_damage) * defender.defense * Fraction(4.5)
    )

    attacker_status_effects: set[StatusEffect] = set()
    defender_status_effects: set[StatusEffect] = set()

    takes_retaliation = StatusEffect.TAKES_RETALIATION in attacker.status_effects or (
        attacker.range <= defender.range
        and Trait.STIFF not in defender.traits
        and Trait.SURPRISE not in attacker.traits
        and Trait.CONVERT not in attacker.traits
        and StatusEffect.FROZEN not in defender.status_effects
    )

    if takes_retaliation:
        if Trait.POISON in defender.traits:
            attacker_status_effects.add(StatusEffect.POISONED)

        # NOTE: The CONVERT and FREEZE traits do not activate on retaliation.

    if Trait.POISON in attacker.traits:
        defender_status_effects.add(StatusEffect.POISONED)
    if Trait.FREEZE in attacker.traits:
        defender_status_effects.add(StatusEffect.FROZEN)
    if Trait.CONVERT in attacker.traits:
        defender_status_effects.add(StatusEffect.CONVERTED)

    return CombatResult(
        damage_to_attacker=tentacle_damage
        + (Fraction(attack_result) if takes_retaliation else Fraction(0)),
        damage_to_defender=Fraction(defense_result),
        attacker_status_effects=attacker_status_effects,
        defender_status_effects=defender_status_effects,
    )
