from abc import ABC, abstractmethod
from collections.abc import Iterable
from importlib import resources
from typing import TypedDict

import yaml

import polycalculator
from polycalculator.status_effect import StatusEffect
from polycalculator.trait import Trait


class UnitParams(TypedDict):
    cost: int
    hp: int
    attack: int
    defense: int
    range: int
    traits: list[str]


class NavalUnitParams(TypedDict):
    attack: int
    cost: int
    defense: int
    range: int
    traits: list[str]


UNIT_DATA: dict[str, UnitParams] = yaml.safe_load(
    resources.open_text(polycalculator, "resources/units.yaml")
)
NAVAL_UNIT_DATA: dict[str, NavalUnitParams] = yaml.safe_load(
    resources.open_text(polycalculator, "resources/naval_units.yaml")
)


class Unit(ABC):
    def __init__(self, current_hp: int | None = None):
        self._status_effects: set[StatusEffect] = set()
        if current_hp is None:
            self._current_hp = None
        elif current_hp <= 0:
            raise ValueError("Current HP must be initialized as greater than 0")
        else:
            self.current_hp = current_hp

    @property
    @abstractmethod
    def cost(self) -> int: ...

    @property
    @abstractmethod
    def _base_max_hp(self) -> int: ...

    @property
    def max_hp(self) -> int:
        if (
            StatusEffect.VETERAN in self._status_effects
            and Trait.STATIC not in self.traits
        ):
            return self._base_max_hp + 50
        return self._base_max_hp

    @property
    def current_hp(self) -> int:
        return self._current_hp if self._current_hp is not None else self.max_hp

    @current_hp.setter
    def current_hp(self, value: int) -> None:
        if value < 0:
            value = 0
        elif value > self.max_hp:
            if StatusEffect.VETERAN in self._status_effects:
                return

            self.add_status_effect(StatusEffect.VETERAN)

        self._current_hp = value

    @property
    def health_ratio(self) -> float:
        return self.current_hp / self.max_hp

    @property
    @abstractmethod
    def attack(self) -> int: ...

    @property
    @abstractmethod
    def defense(self) -> int: ...

    @property
    @abstractmethod
    def range(self) -> int: ...

    @property
    @abstractmethod
    def traits(self) -> frozenset[Trait]: ...

    @property
    def status_effects(self) -> set[StatusEffect]:
        return self._status_effects

    def add_status_effect(self, effect: StatusEffect) -> None:
        if effect == StatusEffect.VETERAN and Trait.STATIC in self.traits:
            raise ValueError(
                "Cannot add the veteran status effect to a unit with the static trait"
            )

        if effect == StatusEffect.POISONED:
            self._status_effects.discard(StatusEffect.FORTIFIED)
            self._status_effects.discard(StatusEffect.WALLED)

        if (
            effect in (StatusEffect.WALLED, StatusEffect.FORTIFIED)
            and StatusEffect.POISONED in self._status_effects
        ):
            return

        if effect == StatusEffect.WALLED:
            self._status_effects.discard(StatusEffect.FORTIFIED)

        self._status_effects.add(effect)

    def add_status_effects(self, effects: Iterable[StatusEffect]) -> None:
        for effect in effects:
            self.add_status_effect(effect)

    @property
    def defense_bonus(self) -> float:
        if StatusEffect.POISONED in self._status_effects:
            return 0.7
        if StatusEffect.WALLED in self._status_effects:
            return 4.0
        if StatusEffect.FORTIFIED in self._status_effects:
            return 1.5
        return 1.0

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(cost={self.cost}, current_hp={self.current_hp}, max_hp={self.max_hp}, attack={self.attack}, defense={self.defense}, range={self.range}, traits={self.traits}, status_effects={self._status_effects})"

    def __eq__(self, value: object) -> bool:
        return isinstance(value, self.__class__) and self.__dict__ == value.__dict__


def create_unit_class(
    name: str,
    *,
    cost: int,
    hp: int,
    attack: int,
    defense: int,
    range: int,
    traits: list[str],
):
    _traits = frozenset(Trait(trait) for trait in traits)

    class _Unit(Unit):
        @property
        def cost(self) -> int:
            return cost

        @property
        def _base_max_hp(self) -> int:
            return hp

        @property
        def attack(self) -> int:
            return attack

        @property
        def defense(self) -> int:
            return defense

        @property
        def range(self) -> int:
            return range

        @property
        def traits(self) -> frozenset[Trait]:
            return _traits

    _Unit.__name__ = name
    return _Unit


UnitRegistry = {
    name: create_unit_class(name, **params) for name, params in UNIT_DATA.items()
}

DefaultWarrior = UnitRegistry["DefaultWarrior"]
Warrior = UnitRegistry["Warrior"]
Archer = UnitRegistry["Archer"]
Rider = UnitRegistry["Rider"]
Catapult = UnitRegistry["Catapult"]
Knight = UnitRegistry["Knight"]
Swordsman = UnitRegistry["Swordsman"]
Defender = UnitRegistry["Defender"]
Cloak = UnitRegistry["Cloak"]
Dagger = UnitRegistry["Dagger"]
MindBender = UnitRegistry["MindBender"]
Giant = UnitRegistry["Giant"]
Juggernaut = UnitRegistry["Juggernaut"]
Pirate = UnitRegistry["Pirate"]
Tridention = UnitRegistry["Tridention"]
Shark = UnitRegistry["Shark"]
Jelly = UnitRegistry["Jelly"]
Puffer = UnitRegistry["Puffer"]
Crab = UnitRegistry["Crab"]
Polytaur = UnitRegistry["Polytaur"]
Egg = UnitRegistry["Egg"]
BabyDragon = UnitRegistry["BabyDragon"]
FireDragon = UnitRegistry["FireDragon"]
Mooni = UnitRegistry["Mooni"]
IceArcher = UnitRegistry["IceArcher"]
BattleSled = UnitRegistry["BattleSled"]
IceFortress = UnitRegistry["IceFortress"]
Gaami = UnitRegistry["Gaami"]
Hexapod = UnitRegistry["Hexapod"]
Doomux = UnitRegistry["Doomux"]
Kiton = UnitRegistry["Kiton"]
Phychi = UnitRegistry["Phychi"]
Shaman = UnitRegistry["Shaman"]
Exida = UnitRegistry["Exida"]
Centipede = UnitRegistry["Centipede"]
Segment = UnitRegistry["Segment"]


def create_naval_unit_class(
    name: str,
    *,
    cost: int,
    attack: int,
    defense: int,
    range: int,
    traits: list[str],
):
    _traits = frozenset(Trait(trait) for trait in traits)

    class _NavalUnit(Unit):
        def __init__(self, unit: Unit | None = None):
            if unit is None:
                unit = DefaultWarrior()
            self._unit = unit
            self._current_hp = unit.current_hp
            self._status_effects = unit.status_effects.difference(
                {StatusEffect.VETERAN}
            )

        @property
        def cost(self) -> int:
            return cost + self._unit.cost

        @property
        def _base_max_hp(self) -> int:
            return self._unit.max_hp

        @property
        def attack(self) -> int:
            return attack

        @property
        def defense(self) -> int:
            return defense

        @property
        def range(self) -> int:
            return range

        @property
        def traits(self) -> frozenset[Trait]:
            return _traits

    _NavalUnit.__name__ = name
    return _NavalUnit


NavalUnitRegistry = {
    name: create_naval_unit_class(name, **params)
    for name, params in NAVAL_UNIT_DATA.items()
}

Raft = NavalUnitRegistry["Raft"]
Scout = NavalUnitRegistry["Scout"]
Rammer = NavalUnitRegistry["Rammer"]
Bomber = NavalUnitRegistry["Bomber"]
