from fractions import Fraction

from polycalculator.combat import CombatResult, single_combat
from polycalculator.status_effect import StatusEffect
from polycalculator.unit import UnitBuilder


def test_wa_wa():
    result = single_combat(UnitBuilder.warrior().build(), UnitBuilder.warrior().build())
    expected_result = CombatResult(
        damage_to_attacker=Fraction(5),
        damage_to_defender=Fraction(5),
        attacker_status_effects=set(),
        defender_status_effects=set(),
    )
    assert result.damage_to_attacker == expected_result.damage_to_attacker
    assert result.damage_to_defender == expected_result.damage_to_defender
    assert result.attacker_status_effects == expected_result.attacker_status_effects
    assert result.defender_status_effects == expected_result.defender_status_effects


def test_wa_wa_d():
    result = single_combat(
        UnitBuilder.warrior().build(), UnitBuilder.warrior().fortified().build()
    )
    expected_result = CombatResult(
        damage_to_attacker=Fraction(5),
        damage_to_defender=Fraction(4),
        attacker_status_effects=set(),
        defender_status_effects=set(),
    )
    assert result.damage_to_attacker == expected_result.damage_to_attacker
    assert result.damage_to_defender == expected_result.damage_to_defender
    assert result.attacker_status_effects == expected_result.attacker_status_effects
    assert result.defender_status_effects == expected_result.defender_status_effects


def test_wa_d_wa_d():
    result = single_combat(
        UnitBuilder.warrior().fortified().build(),
        UnitBuilder.warrior().fortified().build(),
    )
    expected_result = CombatResult(
        damage_to_attacker=Fraction(5),
        damage_to_defender=Fraction(4),
        attacker_status_effects=set(),
        defender_status_effects=set(),
    )
    assert result.damage_to_attacker == expected_result.damage_to_attacker
    assert result.damage_to_defender == expected_result.damage_to_defender
    assert result.attacker_status_effects == expected_result.attacker_status_effects
    assert result.defender_status_effects == expected_result.defender_status_effects


def test_wa_je():
    result = single_combat(UnitBuilder.warrior().build(), UnitBuilder.jelly().build())
    expected_result = CombatResult(
        damage_to_attacker=Fraction(5),
        damage_to_defender=Fraction(3),
        attacker_status_effects=set(),
        defender_status_effects=set(),
    )
    assert result.damage_to_attacker == expected_result.damage_to_attacker
    assert result.damage_to_defender == expected_result.damage_to_defender
    assert result.attacker_status_effects == expected_result.attacker_status_effects
    assert result.defender_status_effects == expected_result.defender_status_effects


def test_je_wa():
    result = single_combat(
        UnitBuilder.jelly().build(),
        UnitBuilder.warrior().with_current_hp(Fraction(5)).build(),
    )
    expected_result = CombatResult(
        damage_to_attacker=Fraction(0),
        damage_to_defender=Fraction(6),
        attacker_status_effects=set(),
        defender_status_effects=set(),
    )
    assert result.damage_to_attacker == expected_result.damage_to_attacker
    assert result.damage_to_defender == expected_result.damage_to_defender
    assert result.attacker_status_effects == expected_result.attacker_status_effects
    assert result.defender_status_effects == expected_result.defender_status_effects


def test_je_je():
    result = single_combat(UnitBuilder.jelly().build(), UnitBuilder.jelly().build())
    expected_result = CombatResult(
        damage_to_attacker=Fraction(5),
        damage_to_defender=Fraction(5),
        attacker_status_effects=set(),
        defender_status_effects=set(),
    )
    assert result.damage_to_attacker == expected_result.damage_to_attacker
    assert result.damage_to_defender == expected_result.damage_to_defender
    assert result.attacker_status_effects == expected_result.attacker_status_effects
    assert result.defender_status_effects == expected_result.defender_status_effects


def test_damaged_je_damaged_je_one():
    result = single_combat(
        UnitBuilder.jelly().with_current_hp(Fraction(15)).build(),
        UnitBuilder.jelly().with_current_hp(Fraction(19)).build(),
    )
    expected_result = CombatResult(
        damage_to_attacker=Fraction(5),
        damage_to_defender=Fraction(4),
        attacker_status_effects=set(),
        defender_status_effects=set(),
    )
    assert result.damage_to_attacker == expected_result.damage_to_attacker
    assert result.damage_to_defender == expected_result.damage_to_defender
    assert result.attacker_status_effects == expected_result.attacker_status_effects
    assert result.defender_status_effects == expected_result.defender_status_effects


def test_damaged_je_damaged_je_two():
    result = single_combat(
        UnitBuilder.jelly().with_current_hp(Fraction(15)).build(),
        UnitBuilder.jelly().with_current_hp(Fraction(10)).build(),
    )
    expected_result = CombatResult(
        damage_to_attacker=Fraction(4),
        damage_to_defender=Fraction(5),
        attacker_status_effects=set(),
        defender_status_effects=set(),
    )
    assert result.damage_to_attacker == expected_result.damage_to_attacker
    assert result.damage_to_defender == expected_result.damage_to_defender
    assert result.attacker_status_effects == expected_result.attacker_status_effects
    assert result.defender_status_effects == expected_result.defender_status_effects


def test_damaged_je_damaged_je_three():
    result = single_combat(
        UnitBuilder.jelly().with_current_hp(Fraction(11)).build(),
        UnitBuilder.jelly().with_current_hp(Fraction(7)).build(),
    )
    expected_result = CombatResult(
        damage_to_attacker=Fraction(4),
        damage_to_defender=Fraction(6),
        attacker_status_effects=set(),
        defender_status_effects=set(),
    )
    assert result.damage_to_attacker == expected_result.damage_to_attacker
    assert result.damage_to_defender == expected_result.damage_to_defender
    assert result.attacker_status_effects == expected_result.attacker_status_effects
    assert result.defender_status_effects == expected_result.defender_status_effects


def test_damaged_je_damaged_je_four():
    result = single_combat(
        UnitBuilder.jelly().with_current_hp(Fraction(7)).build(),
        UnitBuilder.jelly().with_current_hp(Fraction(3)).build(),
    )
    expected_result = CombatResult(
        damage_to_attacker=Fraction(3),
        damage_to_defender=Fraction(6),
        attacker_status_effects=set(),
        defender_status_effects=set(),
    )
    assert result.damage_to_attacker == expected_result.damage_to_attacker
    assert result.damage_to_defender == expected_result.damage_to_defender
    assert result.attacker_status_effects == expected_result.attacker_status_effects
    assert result.defender_status_effects == expected_result.defender_status_effects


def test_ph_wa():
    result = single_combat(UnitBuilder.phychi().build(), UnitBuilder.warrior().build())
    expected_result = CombatResult(
        damage_to_attacker=Fraction(0),
        damage_to_defender=Fraction(2),
        attacker_status_effects=set(),
        defender_status_effects={StatusEffect.POISONED},
    )
    assert result.damage_to_attacker == expected_result.damage_to_attacker
    assert result.damage_to_defender == expected_result.damage_to_defender
    assert result.attacker_status_effects == expected_result.attacker_status_effects
    assert result.defender_status_effects == expected_result.defender_status_effects


def test_wa_ki():
    result = single_combat(UnitBuilder.warrior().build(), UnitBuilder.kiton().build())
    expected_result = CombatResult(
        damage_to_attacker=Fraction(8),
        damage_to_defender=Fraction(4),
        attacker_status_effects={StatusEffect.POISONED},
        defender_status_effects=set(),
    )
    assert result.damage_to_attacker == expected_result.damage_to_attacker
    assert result.damage_to_defender == expected_result.damage_to_defender
    assert result.attacker_status_effects == expected_result.attacker_status_effects
    assert result.defender_status_effects == expected_result.defender_status_effects


def test_ia_wa():
    result = single_combat(
        UnitBuilder.ice_archer().build(), UnitBuilder.warrior().build()
    )
    expected_result = CombatResult(
        damage_to_attacker=Fraction(0),
        damage_to_defender=Fraction(0),
        attacker_status_effects=set(),
        defender_status_effects={StatusEffect.FROZEN},
    )
    assert result.damage_to_attacker == expected_result.damage_to_attacker
    assert result.damage_to_defender == expected_result.damage_to_defender
    assert result.attacker_status_effects == expected_result.attacker_status_effects
    assert result.defender_status_effects == expected_result.defender_status_effects


def test_mb_wa():
    result = single_combat(
        UnitBuilder.mind_bender().build(), UnitBuilder.warrior().build()
    )
    expected_result = CombatResult(
        damage_to_attacker=Fraction(0),
        damage_to_defender=Fraction(0),
        attacker_status_effects=set(),
        defender_status_effects={StatusEffect.CONVERTED},
    )
    assert result.damage_to_attacker == expected_result.damage_to_attacker
    assert result.damage_to_defender == expected_result.damage_to_defender
    assert result.attacker_status_effects == expected_result.attacker_status_effects
    assert result.defender_status_effects == expected_result.defender_status_effects


def test_sh_wa():
    result = single_combat(UnitBuilder.shaman().build(), UnitBuilder.warrior().build())
    expected_result = CombatResult(
        damage_to_attacker=Fraction(0),
        damage_to_defender=Fraction(2),
        attacker_status_effects=set(),
        defender_status_effects={StatusEffect.CONVERTED},
    )
    assert result.damage_to_attacker == expected_result.damage_to_attacker
    assert result.damage_to_defender == expected_result.damage_to_defender
    assert result.attacker_status_effects == expected_result.attacker_status_effects
    assert result.defender_status_effects == expected_result.defender_status_effects
