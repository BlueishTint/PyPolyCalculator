import pytest

from polycalculator.status_effect import StatusEffect
from polycalculator.trait import Trait
from polycalculator.unit import Defender, Giant, Raft, Warrior


class TestUnit:
    def test_wa(self):
        wa = Warrior()
        assert wa.cost == 2
        assert wa.max_hp == 20
        assert wa.current_hp == 20
        assert wa.attack == 4
        assert wa.defense == 4
        assert wa.range == 1
        assert wa.traits == frozenset((Trait.DASH, Trait.FORTIFY))
        assert wa.status_effects == set()
        assert wa.defense_bonus == 1
        assert (
            repr(wa)
            == "Warrior(cost=2, hp=20, attack=4, defense=4, range=1, traits=frozenset({<Trait.DASH: 'dash'>, <Trait.FORTIFY: 'fortify'>}), status_effects=set())"
            or repr(wa)
            == "Warrior(cost=2, hp=20, attack=4, defense=4, range=1, traits=frozenset({<Trait.FORTIFY: 'fortify'>, <Trait.DASH: 'dash'>}), status_effects=set())"
        )

    def test_wa_16(self):
        wa = Warrior()
        wa.current_hp = 16
        assert wa.cost == 2
        assert wa.max_hp == 20
        assert wa.current_hp == 16
        assert wa.attack == 4
        assert wa.defense == 4
        assert wa.range == 1
        assert wa.traits == frozenset((Trait.DASH, Trait.FORTIFY))
        assert wa.status_effects == set()
        assert wa.defense_bonus == 1

    def test_wa_neg_1(self):
        wa = Warrior()
        with pytest.raises(ValueError, match="Current HP cannot be negative"):
            wa.current_hp = -1

    def test_wa_v_36(self):
        wa = Warrior()
        wa.add_status_effect(StatusEffect.VETERAN)
        wa.current_hp = 36
        assert wa.cost == 2
        assert wa.max_hp == 30
        assert wa.current_hp == 30
        assert wa.attack == 4
        assert wa.defense == 4
        assert wa.range == 1
        assert wa.traits == frozenset((Trait.DASH, Trait.FORTIFY))
        assert wa.status_effects == {StatusEffect.VETERAN}
        assert wa.defense_bonus == 1

    def test_gi_86(self):
        gi = Giant()
        with pytest.raises(
            ValueError,
            match="Cannot add the veteran status effect to a unit with the static trait",
        ):
            gi.current_hp = 86

    def test_wa_30(self):
        wa = Warrior()
        wa.current_hp = 30
        assert wa.max_hp == 30
        assert wa.current_hp == 30
        assert wa.attack == 4
        assert wa.defense == 4
        assert wa.range == 1
        assert wa.traits == frozenset((Trait.DASH, Trait.FORTIFY))
        assert wa.status_effects == {StatusEffect.VETERAN}
        assert wa.defense_bonus == 1

    def test_wa_v(self):
        wa = Warrior()
        wa.add_status_effect(StatusEffect.VETERAN)
        assert wa.max_hp == 30
        assert wa.current_hp == 30
        assert wa.attack == 4
        assert wa.defense == 4
        assert wa.range == 1
        assert wa.traits == frozenset((Trait.DASH, Trait.FORTIFY))
        assert wa.status_effects == {StatusEffect.VETERAN}
        assert wa.defense_bonus == 1

    def test_wa_8_v(self):
        wa = Warrior()
        wa.current_hp = 8
        wa.add_status_effect(StatusEffect.VETERAN)
        assert wa.max_hp == 30
        assert wa.current_hp == 8
        assert wa.attack == 4
        assert wa.defense == 4
        assert wa.range == 1
        assert wa.traits == frozenset((Trait.DASH, Trait.FORTIFY))
        assert wa.status_effects == {StatusEffect.VETERAN}
        assert wa.defense_bonus == 1

    def test_wa_f(self):
        wa = Warrior()
        wa.add_status_effect(StatusEffect.FORTIFIED)
        assert wa.max_hp == 20
        assert wa.current_hp == 20
        assert wa.attack == 4
        assert wa.defense == 4
        assert wa.range == 1
        assert wa.traits == frozenset((Trait.DASH, Trait.FORTIFY))
        assert wa.status_effects == {StatusEffect.FORTIFIED}
        assert wa.defense_bonus == 1.5

    def test_wa_w(self):
        wa = Warrior()
        wa.add_status_effect(StatusEffect.WALLED)
        assert wa.max_hp == 20
        assert wa.current_hp == 20
        assert wa.attack == 4
        assert wa.defense == 4
        assert wa.range == 1
        assert wa.traits == frozenset((Trait.DASH, Trait.FORTIFY))
        assert wa.status_effects == {StatusEffect.WALLED}
        assert wa.defense_bonus == 4.0

    def test_wa_p(self):
        wa = Warrior()
        wa.add_status_effect(StatusEffect.POISONED)
        assert wa.max_hp == 20
        assert wa.current_hp == 20
        assert wa.attack == 4
        assert wa.defense == 4
        assert wa.range == 1
        assert wa.traits == frozenset((Trait.DASH, Trait.FORTIFY))
        assert wa.status_effects == {StatusEffect.POISONED}
        assert wa.defense_bonus == 0.7

    def test_wa_w_p(self):
        wa = Warrior()
        wa.add_status_effect(StatusEffect.WALLED)
        wa.add_status_effect(StatusEffect.POISONED)
        assert wa.status_effects == {
            StatusEffect.POISONED,
        }
        assert wa.defense_bonus == 0.7

    def test_wa_p_w(self):
        wa = Warrior()
        wa.add_status_effect(StatusEffect.POISONED)
        wa.add_status_effect(StatusEffect.WALLED)
        assert wa.status_effects == {
            StatusEffect.POISONED,
        }
        assert wa.defense_bonus == 0.7


class TestNavalUnit:
    def test_rf(self):
        rf = Raft()
        assert rf.cost == 2
        assert rf.max_hp == 20
        assert rf.current_hp == 20
        assert rf.attack == 0
        assert rf.defense == 4
        assert rf.range == 0
        assert rf.traits == frozenset((Trait.CARRY, Trait.STATIC, Trait.STIFF))
        assert rf.status_effects == set()
        assert rf.defense_bonus == 1

    def test_rf_16(self):
        rf = Raft()
        rf.current_hp = 16
        assert rf.max_hp == 20
        assert rf.current_hp == 16

    def test_rf_de(self):
        de = Defender()
        rf = Raft(de)
        assert rf.cost == 3
        assert rf.max_hp == 30
        assert rf.current_hp == 30

    def test_rf_wa_18(self):
        wa = Warrior()
        wa.current_hp = 18
        rf = Raft(wa)
        assert rf.current_hp == 18

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
        assert rf.max_hp == 30
        assert rf.current_hp == 30
        assert rf.status_effects == {StatusEffect.VETERAN}
