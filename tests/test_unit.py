from fractions import Fraction

from polycalculator.status_effect import StatusEffect
from polycalculator.trait import Trait
from polycalculator.unit import Unit, UnitBuilder, UnitTemplate


def test_unit_creation():
    unit = Unit(cost=0, max_hp=0, attack=Fraction(0), defense=Fraction(0))  # type: ignore
    assert unit.cost == 0
    assert unit.max_hp == 0
    assert unit.attack == Fraction(0)
    assert unit.defense == Fraction(0)
    assert unit.current_hp == Fraction(0)
    assert unit.movement == 1
    assert unit.range == 1
    assert unit.status_effects == set()
    assert unit.traits == set()
    assert unit.defense_bonus == Fraction(1)


def test_unit_current_hp():
    unit = Unit(cost=0, max_hp=10, attack=Fraction(0), defense=Fraction(0))  # type: ignore
    assert unit.current_hp == Fraction(10)


def test_unit_builder_from_template():
    unit = UnitBuilder.from_template(UnitTemplate.WARRIOR).build()
    assert unit.attack == Fraction(2)


def test_unit_builder_sugar():
    unit = UnitBuilder.centipede().build()
    assert unit.attack == Fraction(4)


def test_unit_builder_init():
    unit = UnitBuilder(
        Unit(
            cost=0,
            max_hp=0,
            attack=Fraction(0),
            defense=Fraction(0),
        )  # type: ignore
    ).build()
    assert unit.cost == 0
    assert unit.max_hp == 0
    assert unit.attack == Fraction(0)
    assert unit.defense == Fraction(0)
    assert unit.current_hp == Fraction(0)
    assert unit.movement == 1
    assert unit.range == 1
    assert unit.status_effects == set()
    assert unit.traits == set()


def test_unit_builder_modifications():
    unit = (
        UnitBuilder.from_template(UnitTemplate.WARRIOR)
        .with_cost(0)
        .with_attack(Fraction(3))
        .with_defense(Fraction(1))
        .with_movement(2)
        .with_range(2)
        .add_status_effect(StatusEffect.POISONED)
        .add_status_effects({StatusEffect.FROZEN, StatusEffect.VETERAN})
        .add_trait(Trait.FREEZE)
        .add_traits({Trait.STIFF, Trait.DRENCH})
        .remove_trait(Trait.DASH)
        .build()
    )
    assert unit.cost == 0
    assert unit.attack == Fraction(3)
    assert unit.defense == Fraction(1)
    assert unit.movement == 2
    assert unit.range == 2
    assert unit.status_effects == {
        StatusEffect.POISONED,
        StatusEffect.FROZEN,
        StatusEffect.VETERAN,
    }
    assert unit.traits == {Trait.FREEZE, Trait.STIFF, Trait.DRENCH, Trait.FORTIFY}


def test_defense_bonus():
    unit = UnitBuilder.warrior().poisoned().build()
    assert unit.defense_bonus == Fraction(7, 10)
    unit = UnitBuilder.warrior().fortified().build()
    assert unit.defense_bonus == Fraction(3, 2)
    unit = UnitBuilder.warrior().walled().build()
    assert unit.defense_bonus == Fraction(4)


def test_unit_builder_max_hp():
    unit = UnitBuilder.warrior().with_max_hp(8).build()
    assert unit.max_hp == 8
    assert unit.current_hp == Fraction(8)


def test_unit_builder_current_hp():
    unit = UnitBuilder.warrior().with_current_hp(Fraction(8)).build()
    assert unit.max_hp == 10
    assert unit.current_hp == Fraction(8)


def test_unit_builder_current_hp_vet():
    unit = UnitBuilder.warrior().with_current_hp(Fraction(15)).build()
    assert unit.max_hp == 15
    assert StatusEffect.VETERAN in unit.status_effects
    assert unit.current_hp == Fraction(15)


def test_unit_builder_veteran():
    unit = UnitBuilder.warrior().veteran().build()
    assert unit.max_hp == 15
    assert StatusEffect.VETERAN in unit.status_effects
    assert unit.current_hp == Fraction(15)


def test_unit_builder_veteran_twice():
    unit = UnitBuilder.warrior().with_current_hp(Fraction(15)).veteran().build()
    assert unit.max_hp == 15
    assert StatusEffect.VETERAN in unit.status_effects
    assert unit.current_hp == Fraction(15)


def test_unit_builder_boosted():
    unit = UnitBuilder.warrior().boosted().build()
    assert unit.attack == Fraction(5, 2)
    assert unit.movement == 2
    assert StatusEffect.BOOSTED in unit.status_effects


def test_unit_builder_takes_retaliation():
    unit = UnitBuilder.warrior().takes_retaliation().build()
    assert StatusEffect.TAKES_RETALIATION in unit.status_effects


def test_unit_builder_raft():
    raft = UnitBuilder.raft().build()
    assert raft.attack == Fraction(0)
    assert raft.defense == Fraction(2)
    assert raft.movement == 2
    assert raft.range == 0
    assert raft.traits == {Trait.CARRY, Trait.STATIC, Trait.STIFF}


def test_unit_builder_scout():
    scout = UnitBuilder.scout().build()
    assert scout.attack == Fraction(2)
    assert scout.defense == Fraction(1)
    assert scout.movement == 3
    assert scout.range == 2
    assert scout.traits == {Trait.CARRY, Trait.STATIC, Trait.DASH, Trait.SCOUT}


def test_unit_builder_rammer():
    rammer = UnitBuilder.rammer().build()
    assert rammer.attack == Fraction(3)
    assert rammer.defense == Fraction(3)
    assert rammer.movement == 3
    assert rammer.range == 1
    assert rammer.traits == {Trait.CARRY, Trait.STATIC, Trait.DASH}


def test_unit_builder_bomber():
    bomber = UnitBuilder.bomber().build()
    assert bomber.attack == Fraction(3)
    assert bomber.defense == Fraction(2)
    assert bomber.movement == 2
    assert bomber.range == 3
    assert bomber.traits == {Trait.CARRY, Trait.STATIC, Trait.SPLASH, Trait.STIFF}


def test_unit_remove_status_effect():
    unit = (
        UnitBuilder.warrior()
        .veteran()
        .remove_status_effect(StatusEffect.VETERAN)
        .build()
    )

    assert unit.max_hp == 15
    assert unit.current_hp == Fraction(15)
    assert unit.status_effects == set()
    assert unit.traits == {Trait.FORTIFY, Trait.DASH}
