from abc import ABC, abstractmethod
from typing import TypedDict
from polycalculator.trait import Trait
from polycalculator.status_effect import StatusEffect


class UnitParams(TypedDict):
    cost: int
    hp: int
    attack: int
    defense: int
    range: int
    traits: frozenset[Trait]


class NavalUnitParams(TypedDict):
    cost: int
    attack: int
    defense: int
    range: int
    traits: frozenset[Trait]


UNIT_DATA: dict[str, UnitParams] = {
    "DefaultWarrior": {
        "cost": 2,
        "hp": 20,
        "attack": 4,
        "defense": 2,
        "range": 1,
        "traits": frozenset((Trait.DASH, Trait.FORTIFY)),
    },
    "Warrior": {
        "cost": 2,
        "hp": 20,
        "attack": 4,
        "defense": 2,
        "range": 1,
        "traits": frozenset((Trait.DASH, Trait.FORTIFY)),
    },
    "Archer": {
        "cost": 3,
        "hp": 20,
        "attack": 4,
        "defense": 2,
        "range": 2,
        "traits": frozenset((Trait.DASH, Trait.FORTIFY)),
    },
    "Rider": {
        "cost": 3,
        "hp": 20,
        "attack": 4,
        "defense": 2,
        "range": 1,
        "traits": frozenset((Trait.DASH, Trait.ESCAPE, Trait.FORTIFY)),
    },
    "Catapult": {
        "cost": 8,
        "hp": 20,
        "attack": 8,
        "defense": 0,
        "range": 3,
        "traits": frozenset((Trait.STIFF,)),
    },
    "Knight": {
        "cost": 8,
        "hp": 20,
        "attack": 7,
        "defense": 2,
        "range": 1,
        "traits": frozenset((Trait.DASH, Trait.PERSIST)),
    },
    "Swordsman": {
        "cost": 5,
        "hp": 30,
        "attack": 6,
        "defense": 6,
        "range": 1,
        "traits": frozenset((Trait.DASH,)),
    },
    "Defender": {
        "cost": 3,
        "hp": 30,
        "attack": 2,
        "defense": 6,
        "range": 1,
        "traits": frozenset((Trait.FORTIFY,)),
    },
    "Cloak": {
        "cost": 8,
        "hp": 10,
        "attack": 4,
        "defense": 1,
        "range": 1,
        "traits": frozenset(
            (
                Trait.HIDE,
                Trait.INFILTRATE,
                Trait.DASH,
                Trait.SCOUT,
                Trait.CREEP,
                Trait.STATIC,
                Trait.STIFF,
            )
        ),
    },
    "Dagger": {
        "cost": 2,
        "hp": 20,
        "attack": 4,
        "defense": 4,
        "range": 1,
        "traits": frozenset(
            (Trait.SURPRISE, Trait.DASH, Trait.INDEPENDENT, Trait.STATIC)
        ),
    },
    "MindBender": {
        "cost": 5,
        "hp": 20,
        "attack": 0,
        "defense": 2,
        "range": 1,
        "traits": frozenset((Trait.HEAL, Trait.CONVERT, Trait.STIFF)),
    },
    "Giant": {
        "cost": 10,
        "hp": 80,
        "attack": 10,
        "defense": 8,
        "range": 1,
        "traits": frozenset((Trait.STATIC,)),
    },
    "Juggernaut": {
        "cost": 10,
        "hp": 80,
        "attack": 9,
        "defense": 8,
        "range": 1,
        "traits": frozenset((Trait.CARRY, Trait.STATIC, Trait.STIFF, Trait.STOMP)),
    },
    "Pirate": {
        "cost": 2,
        "hp": 20,
        "attack": 4,
        "defense": 2,
        "range": 1,
        "traits": frozenset(
            (Trait.SURPRISE, Trait.DASH, Trait.INDEPENDENT, Trait.STATIC)
        ),
    },
    "Tridention": {
        "cost": 8,
        "hp": 20,
        "attack": 5,
        "defense": 2,
        "range": 2,
        "traits": frozenset((Trait.DASH, Trait.PERSIST)),
    },
    "Shark": {
        "cost": 8,
        "hp": 20,
        "attack": 7,
        "defense": 4,
        "range": 1,
        "traits": frozenset((Trait.DASH, Trait.SURPRISE)),
    },
    "Jelly": {
        "cost": 8,
        "hp": 40,
        "attack": 4,
        "defense": 4,
        "range": 1,
        "traits": frozenset((Trait.TENTACLES, Trait.STIFF, Trait.STATIC)),
    },
    "Puffer": {
        "cost": 8,
        "hp": 20,
        "attack": 8,
        "defense": 0,
        "range": 3,
        "traits": frozenset((Trait.DRENCH,)),
    },
    "Crab": {
        "cost": 10,
        "hp": 80,
        "attack": 8,
        "defense": 8,
        "range": 1,
        "traits": frozenset((Trait.STATIC, Trait.ESCAPE, Trait.AUTOFLOOD)),
    },
    "Polytaur": {
        "cost": 3,
        "hp": 30,
        "attack": 6,
        "defense": 2,
        "range": 1,
        "traits": frozenset(
            (Trait.DASH, Trait.INDEPENDENT, Trait.FORTIFY, Trait.STATIC)
        ),
    },
    "Egg": {
        "cost": 10,
        "hp": 20,
        "attack": 0,
        "defense": 4,
        "range": 1,
        "traits": frozenset((Trait.GROW, Trait.FORTIFY, Trait.STIFF, Trait.STATIC)),
    },
    "BabyDragon": {
        "cost": 10,
        "hp": 30,
        "attack": 6,
        "defense": 6,
        "range": 1,
        "traits": frozenset(
            (Trait.DASH, Trait.ESCAPE, Trait.STATIC, Trait.SCOUT, Trait.GROW)
        ),
    },
    "FireDragon": {
        "cost": 10,
        "hp": 40,
        "attack": 8,
        "defense": 6,
        "range": 2,
        "traits": frozenset((Trait.DASH, Trait.SPLASH, Trait.STATIC, Trait.SCOUT)),
    },
    "Mooni": {
        "cost": 5,
        "hp": 20,
        "attack": 0,
        "defense": 2,
        "range": 1,
        "traits": frozenset(
            (Trait.AUTO_FREEZE, Trait.STATIC, Trait.SKATE, Trait.STIFF)
        ),
    },
    "IceArcher": {
        "cost": 3,
        "hp": 20,
        "attack": 0,
        "defense": 2,
        "range": 2,
        "traits": frozenset((Trait.DASH, Trait.FREEZE, Trait.STIFF, Trait.FORTIFY)),
    },
    "BattleSled": {
        "cost": 5,
        "hp": 30,
        "attack": 6,
        "defense": 4,
        "range": 1,
        "traits": frozenset((Trait.DASH, Trait.ESCAPE, Trait.SKATE)),
    },
    "IceFortress": {
        "cost": 15,
        "hp": 40,
        "attack": 8,
        "defense": 6,
        "range": 2,
        "traits": frozenset((Trait.SKATE, Trait.SCOUT)),
    },
    "Gaami": {
        "cost": 10,
        "hp": 60,
        "attack": 8,
        "defense": 6,
        "range": 1,
        "traits": frozenset((Trait.AUTO_FREEZE, Trait.FREEZE_AREA, Trait.STATIC)),
    },
    "Hexapod": {
        "cost": 3,
        "hp": 10,
        "attack": 6,
        "defense": 2,
        "range": 1,
        "traits": frozenset((Trait.DASH, Trait.ESCAPE, Trait.SNEAK, Trait.CREEP)),
    },
    "Doomux": {
        "cost": 10,
        "hp": 40,
        "attack": 8,
        "defense": 4,
        "range": 1,
        "traits": frozenset((Trait.DASH, Trait.CREEP, Trait.EXPLODE)),
    },
    "Kiton": {
        "cost": 3,
        "hp": 30,
        "attack": 2,
        "defense": 6,
        "range": 1,
        "traits": frozenset((Trait.POISON,)),
    },
    "Phychi": {
        "cost": 3,
        "hp": 10,
        "attack": 2,
        "defense": 2,
        "range": 2,
        "traits": frozenset((Trait.DASH, Trait.POISON, Trait.SURPRISE)),
    },
    "Shaman": {
        "cost": 5,
        "hp": 20,
        "attack": 2,
        "defense": 2,
        "range": 1,
        "traits": frozenset((Trait.CONVERT, Trait.BOOST, Trait.STATIC)),
    },
    "Exida": {
        "cost": 8,
        "hp": 20,
        "attack": 6,
        "defense": 2,
        "range": 3,
        "traits": frozenset((Trait.POISON, Trait.SPLASH)),
    },
    "Centipede": {
        "cost": 10,
        "hp": 40,
        "attack": 8,
        "defense": 6,
        "range": 1,
        "traits": frozenset((Trait.DASH, Trait.EAT, Trait.CREEP, Trait.STATIC)),
    },
    "Segment": {
        "cost": 1,
        "hp": 10,
        "attack": 4,
        "defense": 3,
        "range": 1,
        "traits": frozenset((Trait.EXPLODE, Trait.STATIC, Trait.STIFF)),
    },
}

NAVAL_UNIT_DATA: dict[str, NavalUnitParams] = {
    "Raft": {
        "cost": 0,
        "attack": 0,
        "defense": 2,
        "range": 0,
        "traits": frozenset((Trait.CARRY, Trait.STATIC, Trait.STIFF)),
    },
    "Scout": {
        "cost": 5,
        "attack": 4,
        "defense": 2,
        "range": 2,
        "traits": frozenset((Trait.DASH, Trait.CARRY, Trait.SCOUT, Trait.STATIC)),
    },
    "Rammer": {
        "cost": 5,
        "attack": 6,
        "defense": 6,
        "range": 1,
        "traits": frozenset((Trait.DASH, Trait.CARRY, Trait.STATIC)),
    },
    "Bomber": {
        "cost": 15,
        "attack": 6,
        "defense": 4,
        "range": 3,
        "traits": frozenset((Trait.CARRY, Trait.SPLASH, Trait.STATIC, Trait.STIFF)),
    },
}


class Unit(ABC):
    def __init__(self, current_hp: int | None = None):
        self._current_hp = current_hp
        self._status_effects: set[StatusEffect] = set()

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
            return self._base_max_hp + 10
        return self._base_max_hp

    @property
    def current_hp(self) -> int:
        # returns self.max_hp if self._current_hp is None
        # else returns self._current_hp
        return self._current_hp or self.max_hp

    @current_hp.setter
    def current_hp(self, value: int) -> None:
        if value < 0:
            raise ValueError("Current HP cannot be negative")
        self._current_hp = min(value, self.max_hp)

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
            return

        if effect == StatusEffect.POISONED:
            self._status_effects.discard(StatusEffect.FORTIFIED)
            self._status_effects.discard(StatusEffect.WALLED)

        if effect == StatusEffect.WALLED:
            self._status_effects.discard(StatusEffect.FORTIFIED)

        self._status_effects.add(effect)

    @property
    def defense_bonus(self) -> float:
        if StatusEffect.POISONED in self._status_effects:
            return 0.7
        if StatusEffect.WALLED in self._status_effects:
            return 4.0
        if StatusEffect.FORTIFIED in self._status_effects:
            return 1.5
        return 1.0


def create_unit_class(
    name: str,
    *,
    cost: int,
    hp: int,
    attack: int,
    defense: int,
    range: int,
    traits: frozenset[Trait],
):
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
            return traits

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
    traits: frozenset[Trait],
):
    class _NavalUnit(Unit):
        def __init__(self, unit: Unit | None = None):
            if unit is None:
                unit = DefaultWarrior()
            self._unit = unit
            self._status_effects = unit.status_effects

            super().__init__(unit.current_hp)

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
            return traits

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
