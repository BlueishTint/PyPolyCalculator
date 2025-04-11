from collections.abc import Collection
from copy import deepcopy
from typing import NamedTuple

from polycalculator import unit
from polycalculator.status_effect import StatusEffect
from polycalculator.trait import Trait
from polycalculator.unit import Unit


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
    return int((x + 5) / 10) * 10


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


class UnitResult(NamedTuple):
    damage: int
    status_effects: set[StatusEffect]


class MultiCombatResult(NamedTuple):
    attackers: list[UnitResult]
    defenders: list[UnitResult]


def calculate_damage(attacker: Unit, defender: Unit) -> DamageResult:
    attack_force = attacker.attack * (attacker.current_hp / attacker.max_hp)
    defense_force = (
        defender.defense
        * (defender.current_hp / defender.max_hp)
        * defender.defense_bonus
    )
    total_damage = attack_force + defense_force
    attack_result = _round_away_from_zero(
        (attack_force / total_damage) * attacker.attack * 4.5
    )
    defense_result = _round_away_from_zero(
        (defense_force / total_damage) * defender.defense * 4.5
    )

    return DamageResult(defense_result, attack_result)


def calculate_status_effects(
    attacker: Unit, defender: Unit, takes_retaliation: bool
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


def apply_tentacle_damage(attacker: Unit, defender: Unit) -> tuple[Unit, int]:
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
    tuple[Unit, int]
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


def multi_combat(
    attackers: Collection[Unit], defenders: Collection[Unit]
) -> MultiCombatResult:
    """
    Simulate a multi-combat between two units.

    Parameters
    ----------
    attackers : Collection[Unit]
        The attacking units.
    defenders : Collection[Unit]
        The defending units.

    Returns
    -------
    MultiCombatResult
        The damage done and status effects applied to the attackers and defenders.
    """
    attacker_results: list[UnitResult] = []
    defender_results: list[UnitResult] = []
    defenders_i = iter(enumerate(defenders))

    defender_e = next(defenders_i, None)
    if defender_e is None:
        for attacker in attackers:
            attacker_results.append(UnitResult(0, set()))
        return MultiCombatResult(attackers=attacker_results, defenders=defender_results)

    defender_results.append(UnitResult(0, set()))
    i_d, defender = defender_e

    for i_a, attacker in enumerate(attackers):
        if defender.current_hp <= 0:
            defender_e = next(defenders_i, None)
            if defender_e is None:
                for _ in range(i_a, len(attackers)):
                    attacker_results.append(UnitResult(0, set()))
                break
            defender_results.append(UnitResult(0, set()))
            i_d, defender = defender_e

        result = single_combat(attacker, defender)
        attacker_results.append(
            UnitResult(result.damage.to_attacker, result.status_effects.to_attacker)
        )

        defender_results[i_d] = UnitResult(
            defender_results[i_d].damage + result.damage.to_defender,
            defender_results[i_d].status_effects.union(
                result.status_effects.to_defender
            ),
        )

        defender.current_hp -= result.damage.to_defender
        defender.add_status_effects(result.status_effects.to_defender)

    return MultiCombatResult(attackers=attacker_results, defenders=defender_results)


if __name__ == "__main__":
    attackers = [unit.Warrior(), unit.Warrior()]
    defenders = [unit.Warrior()]
    result = multi_combat(attackers, defenders)
    print(result)
    print("#######################################")
    attackers = [unit.Warrior(), unit.Warrior()]
    wa_d = unit.Warrior()
    wa_d.add_status_effect(StatusEffect.FORTIFIED)
    defenders = [wa_d]
    result = multi_combat(attackers, defenders)
    print(result)
