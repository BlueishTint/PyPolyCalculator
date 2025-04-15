from collections.abc import Collection, Container
from typing import NamedTuple

from polycalculator.status_effect import StatusEffect
from polycalculator.trait import Trait
from polycalculator.unit import Unit


def _round_away_from_zero(x: float) -> int:
    return int((x + 5) / 10) * 10


class DamageResult(NamedTuple):
    """The damage the attacker and defender will take."""

    to_attacker: int
    """The damage the attacker will take."""
    to_defender: int
    """The damage the defender will take."""


class StatusEffectResult(NamedTuple):
    """The status effects the attacker and defender will receive."""

    to_attacker: set[StatusEffect]
    """The status effects the attacker will receive."""
    to_defender: set[StatusEffect]
    """The status effects the defender will receive."""


class CombatResult(NamedTuple):
    """The result of a combat between two units."""

    damage: DamageResult
    """The damage the attacker and defender will take."""
    status_effects: StatusEffectResult
    """The status effects the attacker and defender will receive."""


class UnitResult(NamedTuple):
    """The result of a combat for a single unit."""

    damage: int
    """The damage the unit will take."""
    status_effects: set[StatusEffect]
    """The status effects the unit will receive."""


class MultiCombatResult(NamedTuple):
    """The result of a battle involving more than two units."""

    attackers: list[UnitResult]
    """The results of the combat for the attacking units."""
    defenders: list[UnitResult]
    """The results of the combat for the defending units."""


def _calculate_attacker_damage(
    attack: int,
    attacker_health_ratio: float,
    defense: int,
    defender_health_ratio: float,
    defense_bonus: float,
) -> int:
    return _round_away_from_zero(
        4.5
        * attack
        * (effective_attack := attack * attacker_health_ratio)
        / (effective_attack + defense * defender_health_ratio * defense_bonus)
    )


def _calculate_damage(
    attack: int,
    attacker_health_ratio: float,
    defense: int,
    defender_health_ratio: float,
    defense_bonus: float,
    halved: bool = False,
) -> DamageResult:
    attack_force = attack * attacker_health_ratio
    defense_force = defense * defender_health_ratio * defense_bonus
    total_damage = attack_force + defense_force
    attack_result = _round_away_from_zero(attack_force / total_damage * attack * 4.5)
    defense_result = _round_away_from_zero(defense_force / total_damage * defense * 4.5)

    if halved:
        attack_result = attack_result // 2

    return DamageResult(defense_result, attack_result)


def _calculate_status_effects(
    attacker_traits: Container[Trait],
    defender_traits: Container[Trait],
    takes_retaliation: bool,
) -> StatusEffectResult:
    """
    Calculate the status effects applied to the attacker and defender.

    Parameters
    ----------
    attacker_traits : Container[Trait]
        The attacking unit's traits.
    defender_traits : Container[Trait]
        The defending unit's traits.
    takes_retaliation : bool
        Whether or not the attacker takes retaliation.

    Returns
    -------
    StatusEffectResult
        The status effects the attacker and defender will receive.
    """
    to_attacker: set[StatusEffect] = set()
    to_defender: set[StatusEffect] = set()

    if takes_retaliation and Trait.POISON in defender_traits:
        to_attacker.add(StatusEffect.POISONED)

    if Trait.POISON in attacker_traits:
        to_defender.add(StatusEffect.POISONED)

    if Trait.FREEZE in attacker_traits:
        to_defender.add(StatusEffect.FROZEN)

    if Trait.CONVERT in attacker_traits:
        to_defender.add(StatusEffect.CONVERTED)

    return StatusEffectResult(to_attacker, to_defender)


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

    if Trait.TENTACLES in defender.traits:
        if Trait.TENTACLES in attacker.traits:
            # Special case: Jelly vs Jelly
            attacker.add_status_effect(StatusEffect.TAKES_RETALIATION)
        elif attacker.range > defender.range:
            pass
        else:
            tentacle_damage = _calculate_attacker_damage(
                attacker.attack,
                attacker.health_ratio,
                defender.defense,
                defender.health_ratio,
                defender.defense_bonus,
            )

    damage = _calculate_damage(
        attacker.attack,
        attacker.health_ratio,
        defender.defense,
        defender.health_ratio,
        defender.defense_bonus,
        StatusEffect.SPLASHING in attacker.status_effects
        or StatusEffect.EXPLODING in attacker.status_effects,
    )

    takes_retaliation = StatusEffect.TAKES_RETALIATION in attacker.status_effects or (
        attacker.range <= defender.range
        and (defender.current_hp - damage.to_defender) > 0
        and Trait.STIFF not in defender.traits
        and Trait.SURPRISE not in attacker.traits
        and Trait.CONVERT not in attacker.traits
        and Trait.FREEZE not in attacker.traits
        and StatusEffect.FROZEN not in defender.status_effects
    )

    effects = _calculate_status_effects(
        attacker.traits, defender.traits, takes_retaliation
    )

    damage_to_attacker = (
        tentacle_damage + (damage.to_attacker if takes_retaliation else 0)
        if StatusEffect.EXPLODING not in attacker.status_effects
        else attacker.current_hp
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
