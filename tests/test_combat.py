from pathlib import Path
from typing import TypedDict

import pytest
import yaml

from polycalculator import combat, unit
from polycalculator.status_effect import StatusEffect

# region: Setup


class DamageResult(TypedDict):
    to_attacker: int
    to_defender: int


class StatusEffectResult(TypedDict):
    to_attacker: list[str]
    to_defender: list[str]


class SingleCombatData(TypedDict):
    attacker: str
    defender: str
    damage: DamageResult
    effects: StatusEffectResult


def parse_single(
    data: SingleCombatData,
) -> tuple[unit.Unit, unit.Unit, combat.CombatResult]:
    attacker = unit.parse_unit(data["attacker"])
    if attacker is None:
        raise ValueError(f"Invalid attacker: {data['attacker']}")
    defender = unit.parse_unit(data["defender"])
    if defender is None:
        raise ValueError(f"Invalid defender: {data['defender']}")
    result = combat.CombatResult(
        combat.DamageResult(
            data["damage"]["to_attacker"], data["damage"]["to_defender"]
        ),
        combat.StatusEffectResult(
            set(StatusEffect(e) for e in data["effects"]["to_attacker"]),
            set(StatusEffect(e) for e in data["effects"]["to_defender"]),
        ),
    )
    return attacker, defender, result


single_combat_data_path = (
    Path(__file__).parent / "resources" / "single_combat_data.yaml"
)

single_combat_data: list[tuple[unit.Unit, unit.Unit, combat.CombatResult]] = [
    parse_single(tup) for tup in yaml.safe_load(open(single_combat_data_path, "r"))
]


class CombatResult(TypedDict):
    damage: int
    effects: list[str]


class MultiCombatData(TypedDict):
    attackers: list[str]
    defenders: list[str]
    attacker_results: list[CombatResult]
    defender_results: list[CombatResult]


def parse_multi(
    data: MultiCombatData,
) -> tuple[list[unit.Unit], list[unit.Unit], combat.MultiCombatResult]:
    attackers = [unit.parse_unit(a) for a in data["attackers"]]
    if None in attackers:
        raise ValueError(f"Invalid attackers: {data['attackers']}")
    defenders = [unit.parse_unit(d) for d in data["defenders"]]
    if None in defenders:
        raise ValueError(f"Invalid defenders: {data['defenders']}")

    attacker_results = [
        combat.UnitResult(d["damage"], set(StatusEffect(e) for e in d["effects"]))
        for d in data["attacker_results"]
    ]
    defender_results = [
        combat.UnitResult(d["damage"], set(StatusEffect(e) for e in d["effects"]))
        for d in data["defender_results"]
    ]
    return (
        attackers,
        defenders,
        combat.MultiCombatResult(attacker_results, defender_results),
    )  # type: ignore


multi_combat_data_path = Path(__file__).parent / "resources" / "multi_combat_data.yaml"

multi_combat_data: list[
    tuple[list[unit.Unit], list[unit.Unit], combat.MultiCombatResult]
] = [parse_multi(tup) for tup in yaml.safe_load(open(multi_combat_data_path, "r"))]

# endregion: Setup


@pytest.mark.parametrize(("attacker", "defender", "expected"), single_combat_data)
def test_single_combat(
    attacker: unit.Unit, defender: unit.Unit, expected: combat.CombatResult
):
    result = combat.single_combat(attacker, defender)
    assert result.damage.to_attacker == expected.damage.to_attacker
    assert result.damage.to_defender == expected.damage.to_defender
    assert result.status_effects.to_attacker == expected.status_effects.to_attacker
    assert result.status_effects.to_defender == expected.status_effects.to_defender


@pytest.mark.parametrize(("attackers", "defenders", "expected"), multi_combat_data)
def test_multi_combat(
    attackers: list[unit.Unit],
    defenders: list[unit.Unit],
    expected: combat.MultiCombatResult,
):
    result = combat.multi_combat(attackers, defenders)
    assert len(result.attackers) == len(expected.attackers)
    assert len(result.defenders) == len(expected.defenders)
    for attacker_result, expected_result in zip(result.attackers, expected.attackers):
        assert attacker_result.damage == expected_result.damage
        assert attacker_result.status_effects == expected_result.status_effects
    for defender_result, expected_result in zip(result.defenders, expected.defenders):
        assert defender_result.damage == expected_result.damage
        assert defender_result.status_effects == expected_result.status_effects
