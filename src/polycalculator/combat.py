from copy import deepcopy
from typing import NamedTuple

from polycalculator import unit
from polycalculator.status_effect import StatusEffect
from polycalculator.trait import Trait


def _round_away_from_zero(x: float) -> int:
    """
    Round a Fraction away from zero (positive numbers only).

    This is needed because Python's built-in round function rounds to the nearest
    even number when the number is exactly halfway between two integers.
    This function rounds away from zero.

    Parameters
    ----------
    x : float
        The number to round.

    Returns
    -------
    int
        The integer rounded away from zero.
    """
    return int(x + 0.5)


class DamageResult(NamedTuple):
    """
    The result of a damage calculation.

    Attributes
    ----------
    to_attacker : Fraction
        The amount of damage done to the attacker.
    to_defender : Fraction
        The amount of damage done to the defender.

    """

    to_attacker: int
    to_defender: int


class StatusEffectResult(NamedTuple):
    """
    The result of a status effect calculation.

    Attributes
    ----------
    to_attacker : set[StatusEffect]
        The status effects applied to the attacker.
    to_defender : set[StatusEffect]
        The status effects applied to the defender.

    """

    to_attacker: set[StatusEffect]
    to_defender: set[StatusEffect]


class CombatResult(NamedTuple):
    """
    The result of a combat between two units.

    Attributes
    ----------
    damage : DamageResult
        The result of the damage calculation.
    status_effects : StatusEffectResult
        The result of the status effect calculation.

    """

    damage: DamageResult
    status_effects: StatusEffectResult


def calculate_damage(attacker: unit.Unit, defender: unit.Unit) -> DamageResult:
    attack_force = attacker.attack * (attacker.current_hp / attacker.max_hp)
    defense_force = (
        defender.defense
        * (defender.current_hp / defender.max_hp)
        * defender.defense_bonus
    )
    total_damage = attack_force + defense_force
    attack_result = _round_away_from_zero(
        (attack_force / total_damage) * attacker.attack * 9
    )
    defense_result = _round_away_from_zero(
        (defense_force / total_damage) * defender.defense * 9
    )

    return DamageResult(defense_result, attack_result)


def calculate_status_effects(
    attacker: unit.Unit, defender: unit.Unit, takes_retaliation: bool
) -> StatusEffectResult:
    """
    Calculate the status effects applied to the attacker and defender.

    Parameters
    ----------
    attacker : Unit
        The attacking unit.
    defender : Unit
        The defending unit.
    damage_result : DamageResult
        The result of the damage calculation.

    Returns
    -------
    StatusEffectResult
        The status effects applied to the attacker and defender.
    """
    to_attacker: set[StatusEffect] = set()
    to_defender: set[StatusEffect] = set()

    if takes_retaliation:
        if Trait.POISON in defender.traits:
            to_attacker.add(StatusEffect.POISONED)

    if Trait.POISON in attacker.traits:
        to_defender.add(StatusEffect.POISONED)

    if Trait.FREEZE in attacker.traits:
        to_defender.add(StatusEffect.FROZEN)

    if Trait.CONVERT in attacker.traits:
        to_defender.add(StatusEffect.CONVERTED)

    return StatusEffectResult(to_attacker, to_defender)


def apply_tentacle_damage(
    attacker: unit.Unit, defender: unit.Unit
) -> tuple[unit.Unit, int]:
    """
    Handle cases where the defender has tentacles

    Parameters
    ----------
    attacker : Unit
        The attacking unit.
    defender : Unit
        The defending unit.

    Returns
    -------
    tuple[Unit, Fraction]
        The updated attacker and the tentacle damage dealt.
    """
    if Trait.TENTACLES not in defender.traits:
        return attacker, 0

    if Trait.TENTACLES in attacker.traits:
        # Special case: Jelly vs Jelly
        updated_attacker = deepcopy(attacker)
        updated_attacker.add_status_effect(StatusEffect.TAKES_RETALIATION)

        return updated_attacker, 0

    if attacker.range > defender.range:
        return attacker, 0

    # Tentacle strike happens before the attack, without retaliation.
    damage = calculate_damage(defender, attacker).to_attacker

    updated_attacker = deepcopy(attacker)
    updated_attacker.current_hp -= damage

    return updated_attacker, damage


def single_combat(attacker: unit.Unit, defender: unit.Unit) -> CombatResult:
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
    tentacle_damage = 0

    attacker, tentacle_damage = apply_tentacle_damage(attacker, defender)

    damage = calculate_damage(attacker, defender)

    takes_retaliation = StatusEffect.TAKES_RETALIATION in attacker.status_effects or (
        attacker.range <= defender.range
        and defender.current_hp - damage.to_defender > 0
        and Trait.STIFF not in defender.traits
        and Trait.SURPRISE not in attacker.traits
        and Trait.CONVERT not in attacker.traits
        and Trait.FREEZE not in attacker.traits
        and StatusEffect.FROZEN not in defender.status_effects
    )

    effects = calculate_status_effects(attacker, defender, takes_retaliation)

    damage_to_attacker = tentacle_damage + (
        damage.to_attacker if takes_retaliation else 0
    )

    return CombatResult(
        damage=DamageResult(damage_to_attacker, damage.to_defender),
        status_effects=effects,
    )
