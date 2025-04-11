import pytest

from polycalculator.status_effect import StatusEffect
from polycalculator.trait import Trait
from polycalculator.unit import DefaultWarrior, Defender, Giant, Raft, Warrior


class TestUnit:
    def test_wa(self):
        wa = Warrior()
        assert wa.cost == 2
        assert wa.max_hp == 100
        assert wa.current_hp == 100
        assert wa.attack == 20
        assert wa.defense == 20
        assert wa.range == 1
        assert wa.traits == frozenset((Trait.DASH, Trait.FORTIFY))
        assert wa.status_effects == set()
        assert wa.defense_bonus == 1
        assert (
            repr(wa)
            == "Warrior(cost=2, current_hp=100, max_hp=100, attack=20, defense=20, range=1, traits=frozenset({<Trait.DASH: 'dash'>, <Trait.FORTIFY: 'fortify'>}), status_effects=set())"
            or repr(wa)
            == "Warrior(cost=2, current_hp=100, max_hp=100, attack=20, defense=20, range=1, traits=frozenset({<Trait.FORTIFY: 'fortify'>, <Trait.DASH: 'dash'>}), status_effects=set())"
        )

    def test_wa_80(self):
        wa = Warrior(80)
        assert wa.max_hp == 100
        assert wa.current_hp == 80

    def test_wa_0(self):
        with pytest.raises(
            ValueError, match="Current HP must be initialized as greater than 0"
        ):
            Warrior(0)

    def test_wa_neg_10(self):
        wa = Warrior()
        wa.current_hp = -10
        assert wa.max_hp == 100
        assert wa.current_hp == 0

    def test_wa_v_180(self):
        wa = Warrior()
        wa.add_status_effect(StatusEffect.VETERAN)
        wa.current_hp = 180
        assert wa.max_hp == 150
        assert wa.current_hp == 150
        assert wa.traits == frozenset((Trait.DASH, Trait.FORTIFY))
        assert wa.status_effects == {StatusEffect.VETERAN}

    def test_gi_430(self):
        with pytest.raises(
            ValueError,
            match="Cannot add the veteran status effect to a unit with the static trait",
        ):
            Giant(430)

    def test_wa_150(self):
        wa = Warrior(150)
        assert wa.max_hp == 150
        assert wa.current_hp == 150
        assert wa.status_effects == {StatusEffect.VETERAN}

    def test_wa_v(self):
        wa = Warrior()
        wa.add_status_effect(StatusEffect.VETERAN)
        assert wa.max_hp == 150
        assert wa.current_hp == 150
        assert wa.traits == frozenset((Trait.DASH, Trait.FORTIFY))
        assert wa.status_effects == {StatusEffect.VETERAN}

    def test_wa_80_v(self):
        wa = Warrior(80)
        wa.add_status_effect(StatusEffect.VETERAN)
        assert wa.max_hp == 150
        assert wa.current_hp == 80
        assert wa.status_effects == {StatusEffect.VETERAN}

    def test_wa_d(self):
        wa = Warrior()
        wa.add_status_effect(StatusEffect.FORTIFIED)
        assert wa.status_effects == {StatusEffect.FORTIFIED}
        assert wa.defense_bonus == 1.5

    def test_wa_w(self):
        wa = Warrior()
        wa.add_status_effect(StatusEffect.WALLED)
        assert wa.status_effects == {StatusEffect.WALLED}
        assert wa.defense_bonus == 4.0

    def test_wa_p(self):
        wa = Warrior()
        wa.add_status_effect(StatusEffect.POISONED)
        assert wa.status_effects == {StatusEffect.POISONED}
        assert wa.defense_bonus == 0.7

    def test_wa_w_p(self):
        wa = Warrior()
        wa.add_status_effects((StatusEffect.WALLED, StatusEffect.POISONED))
        assert wa.status_effects == {
            StatusEffect.POISONED,
        }
        assert wa.defense_bonus == 0.7

    def test_wa_p_w(self):
        wa = Warrior()
        wa.add_status_effects((StatusEffect.POISONED, StatusEffect.WALLED))
        assert wa.status_effects == {
            StatusEffect.POISONED,
        }
        assert wa.defense_bonus == 0.7

    def test_equality(self):
        wa1 = Warrior()
        wa2 = Warrior()
        dwa = DefaultWarrior()
        assert wa1 == wa2
        assert not wa1 == dwa


class TestNavalUnit:
    def test_rf(self):
        rf = Raft()
        assert rf.cost == 2
        assert rf.max_hp == 100
        assert rf.current_hp == 100
        assert rf.attack == 0
        assert rf.defense == 20
        assert rf.range == 0
        assert rf.traits == frozenset((Trait.CARRY, Trait.STATIC, Trait.STIFF))
        assert rf.status_effects == set()
        assert rf.defense_bonus == 1

    def test_rf_80(self):
        rf = Raft()
        rf.current_hp = 80
        assert rf.max_hp == 100
        assert rf.current_hp == 80

    def test_rf_de(self):
        de = Defender()
        rf = Raft(de)
        assert rf.cost == 3
        assert rf.max_hp == 150
        assert rf.current_hp == 150

    def test_rf_wa_90(self):
        wa = Warrior(90)
        rf = Raft(wa)
        assert rf.current_hp == 90

    def test_rf_wa_p(self):
        wa = Warrior()
        wa.add_status_effect(StatusEffect.POISONED)
        rf = Raft(wa)
        assert rf.status_effects == {StatusEffect.POISONED}
        assert rf.defense_bonus == 0.7

    def test_rf_wa_v(self):
        wa = Warrior()
        wa.add_status_effect(StatusEffect.VETERAN)
        rf = Raft(wa)
        assert rf.max_hp == 150
        assert rf.current_hp == 150
        assert rf.status_effects == set()
