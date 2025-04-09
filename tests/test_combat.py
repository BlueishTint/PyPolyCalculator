from fractions import Fraction

from polycalculator.combat import (
    CombatResult,
    apply_tentacle_damage,
    calculate_damage,
    calculate_status_effects,
    single_combat,
    DamageResult,
    StatusEffectResult,
)
from polycalculator.status_effect import StatusEffect
from polycalculator.unit import UnitBuilder


class TestCalculateDamage:
    def test_wa_wa(self):
        result = calculate_damage(
            UnitBuilder.warrior().build(), UnitBuilder.warrior().build()
        )
        expected_result = DamageResult(Fraction(5), Fraction(5))
        assert expected_result.to_attacker == result.to_attacker
        assert expected_result.to_defender == result.to_defender

    def test_je_je(self):
        result = calculate_damage(
            UnitBuilder.jelly().build(), UnitBuilder.jelly().build()
        )
        expected_result = DamageResult(Fraction(5), Fraction(5))
        assert expected_result.to_attacker == result.to_attacker
        assert expected_result.to_defender == result.to_defender

    def test_injured_wa_injured_wa_d(self):
        result = calculate_damage(
            UnitBuilder.warrior().with_current_hp(Fraction(5)).build(),
            UnitBuilder.warrior().with_current_hp(Fraction(5)).fortified().build(),
        )
        expected_result = DamageResult(Fraction(5), Fraction(4))
        assert expected_result.to_attacker == result.to_attacker
        assert expected_result.to_defender == result.to_defender


class TestCalculateStatusEffects:
    def test_wa_wa(self):
        result = calculate_status_effects(
            UnitBuilder.warrior().build(), UnitBuilder.warrior().build(), True
        )
        expected_result = StatusEffectResult(set(), set())
        assert expected_result.to_attacker == result.to_attacker
        assert expected_result.to_defender == result.to_defender

    def test_ph_wa(self):
        result = calculate_status_effects(
            UnitBuilder.phychi().build(), UnitBuilder.warrior().build(), False
        )
        expected_result = StatusEffectResult(set(), {StatusEffect.POISONED})
        assert expected_result.to_attacker == result.to_attacker
        assert expected_result.to_defender == result.to_defender

    def test_ia_wa(self):
        result = calculate_status_effects(
            UnitBuilder.ice_archer().build(), UnitBuilder.warrior().build(), False
        )
        expected_result = StatusEffectResult(set(), {StatusEffect.FROZEN})
        assert expected_result.to_attacker == result.to_attacker
        assert expected_result.to_defender == result.to_defender

    def test_wa_ia(self):
        result = calculate_status_effects(
            UnitBuilder.warrior().build(), UnitBuilder.ice_archer().build(), False
        )
        expected_result = StatusEffectResult(set(), set())
        assert expected_result.to_attacker == result.to_attacker
        assert expected_result.to_defender == result.to_defender


class TestApplyTentacleDamage:
    def test_wa_je(self):
        result = apply_tentacle_damage(
            UnitBuilder.warrior().build(), UnitBuilder.jelly().build()
        )
        expected_result = (
            UnitBuilder.warrior().with_current_hp(Fraction(5)).build(),
            5,
        )

        assert expected_result[0] == result[0]
        assert expected_result[1] == result[1]

    def test_je_je(self):
        result = apply_tentacle_damage(
            UnitBuilder.jelly().build(), UnitBuilder.jelly().build()
        )
        expected_result = (
            UnitBuilder.jelly()
            .add_status_effect(StatusEffect.TAKES_RETALIATION)
            .build(),
            0,
        )

        assert expected_result[0] == result[0]
        assert expected_result[1] == result[1]

    def test_ar_je(self):
        result = apply_tentacle_damage(
            UnitBuilder.archer().build(), UnitBuilder.jelly().build()
        )
        expected_result = (
            UnitBuilder.archer().with_current_hp(Fraction(10)).build(),
            0,
        )

        assert expected_result[0] == result[0]
        assert expected_result[1] == result[1]


class TestSingleCombat:
    def test_wa_wa(self):
        result = single_combat(
            UnitBuilder.warrior().build(), UnitBuilder.warrior().build()
        )
        expected_result = CombatResult(
            DamageResult(Fraction(5), Fraction(5)),
            StatusEffectResult(set(), set()),
        )
        assert result.damage.to_attacker == expected_result.damage.to_attacker
        assert result.damage.to_defender == expected_result.damage.to_defender
        assert (
            result.status_effects.to_attacker
            == expected_result.status_effects.to_attacker
        )
        assert (
            result.status_effects.to_defender
            == expected_result.status_effects.to_defender
        )

    def test_wa_wa_d(self):
        result = single_combat(
            UnitBuilder.warrior().build(), UnitBuilder.warrior().fortified().build()
        )
        expected_result = CombatResult(
            DamageResult(to_attacker=Fraction(5), to_defender=Fraction(4)),
            StatusEffectResult(to_attacker=set(), to_defender=set()),
        )
        assert result.damage.to_attacker == expected_result.damage.to_attacker
        assert result.damage.to_defender == expected_result.damage.to_defender
        assert (
            result.status_effects.to_attacker
            == expected_result.status_effects.to_attacker
        )
        assert (
            result.status_effects.to_defender
            == expected_result.status_effects.to_defender
        )

    def test_wa_d_wa_d(self):
        result = single_combat(
            UnitBuilder.warrior().fortified().build(),
            UnitBuilder.warrior().fortified().build(),
        )
        expected_result = CombatResult(
            DamageResult(to_attacker=Fraction(5), to_defender=Fraction(4)),
            StatusEffectResult(to_attacker=set(), to_defender=set()),
        )
        assert result.damage.to_attacker == expected_result.damage.to_attacker
        assert result.damage.to_defender == expected_result.damage.to_defender
        assert (
            result.status_effects.to_attacker
            == expected_result.status_effects.to_attacker
        )
        assert (
            result.status_effects.to_defender
            == expected_result.status_effects.to_defender
        )

    def test_wa_je(self):
        result = single_combat(
            UnitBuilder.warrior().build(), UnitBuilder.jelly().build()
        )
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=Fraction(5), to_defender=Fraction(3)),
            status_effects=StatusEffectResult(to_attacker=set(), to_defender=set()),
        )
        assert result.damage.to_attacker == expected_result.damage.to_attacker
        assert result.damage.to_defender == expected_result.damage.to_defender
        assert (
            result.status_effects.to_attacker
            == expected_result.status_effects.to_attacker
        )
        assert (
            result.status_effects.to_defender
            == expected_result.status_effects.to_defender
        )

    def test_je_wa(self):
        result = single_combat(
            UnitBuilder.jelly().build(),
            UnitBuilder.warrior().with_current_hp(Fraction(5)).build(),
        )
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=Fraction(0), to_defender=Fraction(6)),
            status_effects=StatusEffectResult(to_attacker=set(), to_defender=set()),
        )
        assert result.damage.to_defender == expected_result.damage.to_defender
        assert (
            result.status_effects.to_attacker
            == expected_result.status_effects.to_attacker
        )
        assert (
            result.status_effects.to_defender
            == expected_result.status_effects.to_defender
        )

    def test_je_je(self):
        result = single_combat(UnitBuilder.jelly().build(), UnitBuilder.jelly().build())
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=Fraction(5), to_defender=Fraction(5)),
            status_effects=StatusEffectResult(to_attacker=set(), to_defender=set()),
        )
        assert result.damage.to_attacker == expected_result.damage.to_attacker
        assert result.damage.to_defender == expected_result.damage.to_defender
        assert (
            result.status_effects.to_attacker
            == expected_result.status_effects.to_attacker
        )
        assert (
            result.status_effects.to_defender
            == expected_result.status_effects.to_defender
        )

    def test_damaged_je_damaged_je_one(self):
        result = single_combat(
            UnitBuilder.jelly().with_current_hp(Fraction(15)).build(),
            UnitBuilder.jelly().with_current_hp(Fraction(19)).build(),
        )
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=Fraction(5), to_defender=Fraction(4)),
            status_effects=StatusEffectResult(to_attacker=set(), to_defender=set()),
        )
        assert result.damage.to_attacker == expected_result.damage.to_attacker
        assert result.damage.to_defender == expected_result.damage.to_defender
        assert (
            result.status_effects.to_attacker
            == expected_result.status_effects.to_attacker
        )
        assert (
            result.status_effects.to_defender
            == expected_result.status_effects.to_defender
        )

    def test_damaged_je_damaged_je_two(self):
        result = single_combat(
            UnitBuilder.jelly().with_current_hp(Fraction(15)).build(),
            UnitBuilder.jelly().with_current_hp(Fraction(10)).build(),
        )
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=Fraction(4), to_defender=Fraction(5)),
            status_effects=StatusEffectResult(to_attacker=set(), to_defender=set()),
        )
        assert result.damage.to_attacker == expected_result.damage.to_attacker
        assert result.damage.to_defender == expected_result.damage.to_defender
        assert (
            result.status_effects.to_attacker
            == expected_result.status_effects.to_attacker
        )
        assert (
            result.status_effects.to_defender
            == expected_result.status_effects.to_defender
        )

    def test_damaged_je_damaged_je_three(self):
        result = single_combat(
            UnitBuilder.jelly().with_current_hp(Fraction(11)).build(),
            UnitBuilder.jelly().with_current_hp(Fraction(7)).build(),
        )
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=Fraction(4), to_defender=Fraction(6)),
            status_effects=StatusEffectResult(to_attacker=set(), to_defender=set()),
        )
        assert result.damage.to_attacker == expected_result.damage.to_attacker
        assert result.damage.to_defender == expected_result.damage.to_defender
        assert (
            result.status_effects.to_attacker
            == expected_result.status_effects.to_attacker
        )
        assert (
            result.status_effects.to_defender
            == expected_result.status_effects.to_defender
        )

    def test_damaged_je_damaged_je_four(self):
        result = single_combat(
            UnitBuilder.jelly().with_current_hp(Fraction(7)).build(),
            UnitBuilder.jelly().with_current_hp(Fraction(3)).build(),
        )
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=Fraction(3), to_defender=Fraction(6)),
            status_effects=StatusEffectResult(to_attacker=set(), to_defender=set()),
        )
        assert result.damage.to_attacker == expected_result.damage.to_attacker
        assert result.damage.to_defender == expected_result.damage.to_defender
        assert (
            result.status_effects.to_attacker
            == expected_result.status_effects.to_attacker
        )
        assert (
            result.status_effects.to_defender
            == expected_result.status_effects.to_defender
        )

    def test_ph_wa(self):
        result = single_combat(
            UnitBuilder.phychi().build(), UnitBuilder.warrior().build()
        )
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=Fraction(0), to_defender=Fraction(2)),
            status_effects=StatusEffectResult(
                to_attacker=set(), to_defender={StatusEffect.POISONED}
            ),
        )
        assert result.damage.to_attacker == expected_result.damage.to_attacker
        assert result.damage.to_defender == expected_result.damage.to_defender
        assert (
            result.status_effects.to_attacker
            == expected_result.status_effects.to_attacker
        )
        assert (
            result.status_effects.to_defender
            == expected_result.status_effects.to_defender
        )

    def test_wa_ki(self):
        result = single_combat(
            UnitBuilder.warrior().build(), UnitBuilder.kiton().build()
        )
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=Fraction(8), to_defender=Fraction(4)),
            status_effects=StatusEffectResult(
                to_attacker={StatusEffect.POISONED}, to_defender=set()
            ),
        )
        assert result.damage.to_attacker == expected_result.damage.to_attacker
        assert result.damage.to_defender == expected_result.damage.to_defender
        assert (
            result.status_effects.to_attacker
            == expected_result.status_effects.to_attacker
        )
        assert (
            result.status_effects.to_defender
            == expected_result.status_effects.to_defender
        )

    def test_ia_wa(self):
        result = single_combat(
            UnitBuilder.ice_archer().build(), UnitBuilder.warrior().build()
        )
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=Fraction(0), to_defender=Fraction(0)),
            status_effects=StatusEffectResult(
                to_attacker=set(), to_defender={StatusEffect.FROZEN}
            ),
        )
        assert result.damage.to_attacker == expected_result.damage.to_attacker
        assert result.damage.to_defender == expected_result.damage.to_defender
        assert (
            result.status_effects.to_attacker
            == expected_result.status_effects.to_attacker
        )
        assert (
            result.status_effects.to_defender
            == expected_result.status_effects.to_defender
        )

    def test_mb_wa(self):
        result = single_combat(
            UnitBuilder.mind_bender().build(), UnitBuilder.warrior().build()
        )
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=Fraction(0), to_defender=Fraction(0)),
            status_effects=StatusEffectResult(
                to_attacker=set(), to_defender={StatusEffect.CONVERTED}
            ),
        )
        assert result.damage.to_attacker == expected_result.damage.to_attacker
        assert result.damage.to_defender == expected_result.damage.to_defender
        assert (
            result.status_effects.to_attacker
            == expected_result.status_effects.to_attacker
        )
        assert (
            result.status_effects.to_defender
            == expected_result.status_effects.to_defender
        )

    def test_sh_wa(self):
        result = single_combat(
            UnitBuilder.shaman().build(), UnitBuilder.warrior().build()
        )
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=Fraction(0), to_defender=Fraction(2)),
            status_effects=StatusEffectResult(
                to_attacker=set(), to_defender={StatusEffect.CONVERTED}
            ),
        )
        assert result.damage.to_attacker == expected_result.damage.to_attacker
        assert result.damage.to_defender == expected_result.damage.to_defender
        assert (
            result.status_effects.to_attacker
            == expected_result.status_effects.to_attacker
        )
        assert (
            result.status_effects.to_defender
            == expected_result.status_effects.to_defender
        )

    def test_ar_wa(self):
        result = single_combat(
            UnitBuilder.archer().build(), UnitBuilder.warrior().build()
        )
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=Fraction(0), to_defender=Fraction(5)),
            status_effects=StatusEffectResult(to_attacker=set(), to_defender=set()),
        )
        assert result.damage.to_attacker == expected_result.damage.to_attacker
        assert result.damage.to_defender == expected_result.damage.to_defender
        assert (
            result.status_effects.to_attacker
            == expected_result.status_effects.to_attacker
        )
        assert (
            result.status_effects.to_defender
            == expected_result.status_effects.to_defender
        )
