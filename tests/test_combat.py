from polycalculator import unit
from polycalculator.combat import (
    CombatResult,
    DamageResult,
    StatusEffectResult,
    apply_tentacle_damage,
    calculate_damage,
    calculate_status_effects,
    single_combat,
)
from polycalculator.status_effect import StatusEffect


class TestCalculateDamage:
    def test_wa_wa(self):
        result = calculate_damage(unit.Warrior(), unit.Warrior())
        expected_result = DamageResult(50, 50)
        assert expected_result.to_attacker == result.to_attacker
        assert expected_result.to_defender == result.to_defender

    def test_je_je(self):
        result = calculate_damage(unit.Jelly(), unit.Jelly())
        expected_result = DamageResult(50, 50)
        assert expected_result.to_attacker == result.to_attacker
        assert expected_result.to_defender == result.to_defender

    def test_injured_wa_injured_wa_d(self):
        wa1 = unit.Warrior(50)
        wa2 = unit.Warrior(50)
        wa2.add_status_effect(unit.StatusEffect.FORTIFIED)
        result = calculate_damage(wa1, wa2)
        expected_result = DamageResult(50, 40)
        assert expected_result.to_attacker == result.to_attacker
        assert expected_result.to_defender == result.to_defender

    def test_wa_injured_wa(self):
        wa1 = unit.Warrior()
        wa2 = unit.Warrior(50)
        result = calculate_damage(wa1, wa2)
        expected_result = DamageResult(30, 60)
        assert expected_result.to_attacker == result.to_attacker
        assert expected_result.to_defender == result.to_defender

    def test_je_injured_wa(self):
        je = unit.Jelly()
        wa = unit.Warrior(50)
        result = calculate_damage(je, wa)
        expected_result = DamageResult(30, 60)
        assert expected_result.to_attacker == result.to_attacker
        assert expected_result.to_defender == result.to_defender

    def test_sh_wa(self):
        result = calculate_damage(unit.Shaman(), unit.Warrior())
        expected_result = DamageResult(60, 20)
        assert expected_result.to_attacker == result.to_attacker
        assert expected_result.to_defender == result.to_defender


class TestCalculateStatusEffects:
    def test_wa_wa(self):
        result = calculate_status_effects(unit.Warrior(), unit.Warrior(), True)
        expected_result = StatusEffectResult(set(), set())
        assert expected_result.to_attacker == result.to_attacker
        assert expected_result.to_defender == result.to_defender

    def test_ph_wa(self):
        result = calculate_status_effects(unit.Phychi(), unit.Warrior(), False)
        expected_result = StatusEffectResult(set(), {StatusEffect.POISONED})
        assert expected_result.to_attacker == result.to_attacker
        assert expected_result.to_defender == result.to_defender

    def test_ia_wa(self):
        result = calculate_status_effects(unit.IceArcher(), unit.Warrior(), False)
        expected_result = StatusEffectResult(set(), {StatusEffect.FROZEN})
        assert expected_result.to_attacker == result.to_attacker
        assert expected_result.to_defender == result.to_defender

    def test_wa_ia(self):
        result = calculate_status_effects(unit.Warrior(), unit.IceArcher(), False)
        expected_result = StatusEffectResult(set(), set())
        assert expected_result.to_attacker == result.to_attacker
        assert expected_result.to_defender == result.to_defender


class TestApplyTentacleDamage:
    def test_wa_je(self):
        result = apply_tentacle_damage(unit.Warrior(), unit.Jelly())
        expected_result = (unit.Warrior(50), 50)

        assert expected_result[0] == result[0]
        assert expected_result[1] == result[1]

    def test_je_je(self):
        result = apply_tentacle_damage(unit.Jelly(), unit.Jelly())
        ex_je = unit.Jelly()
        ex_je.add_status_effect(StatusEffect.TAKES_RETALIATION)
        expected_result = (ex_je, 0)

        assert expected_result[0] == result[0]
        assert expected_result[1] == result[1]

    def test_ar_je(self):
        result = apply_tentacle_damage(unit.Archer(), unit.Jelly())
        expected_result = (
            unit.Archer(),
            0,
        )

        assert expected_result[0] == result[0]
        assert expected_result[1] == result[1]


class TestSingleCombat:
    def test_wa_wa(self):
        result = single_combat(unit.Warrior(), unit.Warrior())
        expected_result = CombatResult(
            DamageResult(50, 50),
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
        wa_d = unit.Warrior()
        wa_d.add_status_effect(StatusEffect.FORTIFIED)
        result = single_combat(unit.Warrior(), wa_d)
        expected_result = CombatResult(
            DamageResult(to_attacker=50, to_defender=40),
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
        wa_d1 = unit.Warrior()
        wa_d1.add_status_effect(StatusEffect.FORTIFIED)
        wa_d2 = unit.Warrior()
        wa_d2.add_status_effect(StatusEffect.FORTIFIED)
        result = single_combat(wa_d1, wa_d2)
        expected_result = CombatResult(
            DamageResult(to_attacker=50, to_defender=40),
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
        result = single_combat(unit.Warrior(), unit.Jelly())
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=50, to_defender=30),
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
        result = single_combat(unit.Jelly(), unit.Warrior(50))
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=0, to_defender=60),
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
        result = single_combat(unit.Jelly(), unit.Jelly())
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=50, to_defender=50),
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
        result = single_combat(unit.Jelly(150), unit.Jelly(190))
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=50, to_defender=40),
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
        result = single_combat(unit.Jelly(150), unit.Jelly(100))
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=40, to_defender=50),
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
        result = single_combat(unit.Jelly(110), unit.Jelly(70))
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=40, to_defender=60),
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
            unit.Jelly(70),
            unit.Jelly(30),
        )
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=30, to_defender=60),
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
        result = single_combat(unit.Phychi(), unit.Warrior())
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=0, to_defender=20),
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
        result = single_combat(unit.Warrior(), unit.Kiton())
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=80, to_defender=40),
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
        result = single_combat(unit.IceArcher(), unit.Warrior())
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=0, to_defender=0),
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
        result = single_combat(unit.MindBender(), unit.Warrior())
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=0, to_defender=0),
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
        result = single_combat(unit.Shaman(), unit.Warrior())
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=0, to_defender=20),
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
        result = single_combat(unit.Archer(), unit.Warrior())
        expected_result = CombatResult(
            damage=DamageResult(to_attacker=0, to_defender=50),
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
