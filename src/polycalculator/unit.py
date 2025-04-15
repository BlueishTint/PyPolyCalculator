from abc import ABC, abstractmethod
from collections.abc import Iterable
from importlib import resources
import re
from typing import TypedDict

import yaml

import polycalculator
from polycalculator.status_effect import StatusEffect
from polycalculator.trait import Trait


class _UnitParams(TypedDict):
    cost: int
    hp: int
    attack: int
    defense: int
    range: int
    traits: list[str]


class _NavalUnitParams(TypedDict):
    attack: int
    cost: int
    defense: int
    range: int
    traits: list[str]


UNIT_DATA: dict[str, _UnitParams] = yaml.safe_load(
    resources.open_text(polycalculator, "resources/units.yaml")
)
NAVAL_UNIT_DATA: dict[str, _NavalUnitParams] = yaml.safe_load(
    resources.open_text(polycalculator, "resources/naval_units.yaml")
)


class Unit(ABC):
    """Base class for all units."""

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
            self._current_hp = None
            return

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
            return

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

        if effect == StatusEffect.SPLASHING and Trait.SPLASH not in self.traits:
            return

        if effect == StatusEffect.EXPLODING and Trait.EXPLODE not in self.traits:
            return

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


def _change_name(name: str) -> str:
    """Change a string from CamelCase to normal case."""
    return " ".join(re.findall("[A-Z][^A-Z]*", name)).lower()


def _create_unit_class(
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
    _Unit.__doc__ = f"Represents a {_change_name(name)} unit."
    _Unit.__module__ = Unit.__module__
    _Unit.__qualname__ = Unit.__qualname__.replace("Unit", name)
    _Unit.__annotations__ = Unit.__annotations__.copy()
    return _Unit


_UnitRegistry = {
    name: _create_unit_class(name, **params) for name, params in UNIT_DATA.items()
}

DefaultWarrior = _UnitRegistry["DefaultWarrior"]
Warrior = _UnitRegistry["Warrior"]
Archer = _UnitRegistry["Archer"]
Rider = _UnitRegistry["Rider"]
Catapult = _UnitRegistry["Catapult"]
Knight = _UnitRegistry["Knight"]
Swordsman = _UnitRegistry["Swordsman"]
Defender = _UnitRegistry["Defender"]
Cloak = _UnitRegistry["Cloak"]
Dagger = _UnitRegistry["Dagger"]
MindBender = _UnitRegistry["MindBender"]
Giant = _UnitRegistry["Giant"]
Juggernaut = _UnitRegistry["Juggernaut"]
Pirate = _UnitRegistry["Pirate"]
Tridention = _UnitRegistry["Tridention"]
Shark = _UnitRegistry["Shark"]
Jelly = _UnitRegistry["Jelly"]
Puffer = _UnitRegistry["Puffer"]
Crab = _UnitRegistry["Crab"]
Polytaur = _UnitRegistry["Polytaur"]
Egg = _UnitRegistry["Egg"]
BabyDragon = _UnitRegistry["BabyDragon"]
FireDragon = _UnitRegistry["FireDragon"]
Mooni = _UnitRegistry["Mooni"]
IceArcher = _UnitRegistry["IceArcher"]
BattleSled = _UnitRegistry["BattleSled"]
IceFortress = _UnitRegistry["IceFortress"]
Gaami = _UnitRegistry["Gaami"]
Hexapod = _UnitRegistry["Hexapod"]
Doomux = _UnitRegistry["Doomux"]
Kiton = _UnitRegistry["Kiton"]
Phychi = _UnitRegistry["Phychi"]
Shaman = _UnitRegistry["Shaman"]
Exida = _UnitRegistry["Exida"]
Centipede = _UnitRegistry["Centipede"]
Segment = _UnitRegistry["Segment"]


class NavalUnit(Unit):
    """Base class for all naval units."""

    def __init__(self, unit: Unit | None = None):
        if unit is None:
            unit = DefaultWarrior()
        self._unit = unit

    @property
    def _base_max_hp(self) -> int:
        return self._unit._base_max_hp

    @property
    def max_hp(self) -> int:
        return self._unit.max_hp

    @property
    def current_hp(self) -> int:
        return self._unit.current_hp

    @current_hp.setter
    def current_hp(self, value: int) -> None:
        self._unit.current_hp = value

    @property
    def status_effects(self) -> set[StatusEffect]:
        return self._unit.status_effects

    def add_status_effect(self, effect: StatusEffect) -> None:
        self._unit.add_status_effect(effect)

    @property
    def defense_bonus(self) -> float:
        return self._unit.defense_bonus

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(cost={self.cost}, current_hp={self.current_hp}, max_hp={self.max_hp}, attack={self.attack}, defense={self.defense}, range={self.range}, traits={self.traits}, status_effects={self._unit.status_effects}, _unit={repr(self._unit)})"


def _create_naval_unit_class(
    name: str,
    *,
    cost: int,
    attack: int,
    defense: int,
    range: int,
    traits: list[str],
):
    _traits = frozenset(Trait(trait) for trait in traits)

    class _NavalUnit(NavalUnit):
        def __init__(self, unit: Unit | None = None):
            if unit is None:
                unit = DefaultWarrior()
            self._unit = unit

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
    _NavalUnit.__doc__ = f"Represents a {_change_name(name)} unit."
    _NavalUnit.__module__ = NavalUnit.__module__
    _NavalUnit.__qualname__ = NavalUnit.__qualname__.replace("NavalUnit", name)
    _NavalUnit.__annotations__ = NavalUnit.__annotations__.copy()
    return _NavalUnit


_NavalUnitRegistry = {
    name: _create_naval_unit_class(name, **params)
    for name, params in NAVAL_UNIT_DATA.items()
}

Raft = _NavalUnitRegistry["Raft"]
Scout = _NavalUnitRegistry["Scout"]
Rammer = _NavalUnitRegistry["Rammer"]
Bomber = _NavalUnitRegistry["Bomber"]


# region Build maps
_ABBR_OVERRIDES: dict[str, str] = yaml.safe_load(
    resources.open_text(polycalculator, "resources/abbr_overrides.yaml")
)

_NAVAL_ABBR_OVERRIDES: dict[str, str] = yaml.safe_load(
    resources.open_text(polycalculator, "resources/naval_abbr_overrides.yaml")
)
_abbr_map: dict[str, type[Unit]] = {}

for _name, _cls in set(_UnitRegistry.items()).difference(
    (("DefaultWarrior", DefaultWarrior),)
):
    _name = _name.lower()

    # Add custom abbreviations first so they take priority
    for abbr, target_name in _ABBR_OVERRIDES.items():
        if target_name == _name:
            _abbr_map[abbr] = _cls

    # Add all valid prefixes if not already overridden
    for i in range(2, len(_name) + 1):
        abbr = _name[:i]
        if abbr in _NAVAL_ABBR_OVERRIDES.keys():
            continue
        if abbr not in _abbr_map:
            _abbr_map[abbr] = _cls

_ABBR_MAP = _abbr_map
_naval_abbr_map: dict[str, type[NavalUnit]] = {}

for _name, _cls in _NavalUnitRegistry.items():
    _name = _name.lower()

    # Add custom abbreviations first so they take priority
    for abbr, target_name in _NAVAL_ABBR_OVERRIDES.items():
        if target_name == _name:
            _naval_abbr_map[abbr] = _cls

    # Add all valid prefixes if not already overridden
    for i in range(2, len(_name) + 1):
        abbr = _name[:i]
        if abbr in _ABBR_MAP.keys():
            continue
        if abbr not in _naval_abbr_map:
            _naval_abbr_map[abbr] = _cls

_NAVAL_ABBR_MAP = _naval_abbr_map
_EFFECT_ABBR_MAP = {
    abbr: StatusEffect(effect)
    for abbr, effect in yaml.safe_load(
        resources.open_text(polycalculator, "resources/effect_abbrs.yaml")
    ).items()
}
# endregion Build maps


def parse_unit(s: str) -> Unit | None:
    parts = s.lower().split()
    hp: float | None = None
    unit_cls: type[Unit] | None = None
    naval_cls: type[NavalUnit] | None = None
    status_effects: set[StatusEffect] = set()

    for part in parts:
        try:
            hp = float(part)
            continue
        except ValueError:
            pass

        if part in _ABBR_MAP:
            unit_cls = _ABBR_MAP[part]
        elif part in _NAVAL_ABBR_MAP:
            naval_cls = _NAVAL_ABBR_MAP[part]
        elif part in _EFFECT_ABBR_MAP:
            status_effects.add(_EFFECT_ABBR_MAP[part])
        else:
            print(f"Skipping unknown part {part}")

    if not unit_cls and not naval_cls:
        return None

    if unit_cls:
        unit = unit_cls(int(hp * 10) if hp is not None else None)
    else:
        unit = DefaultWarrior(int(hp * 10) if hp is not None else None)

    unit.add_status_effects(status_effects)

    if naval_cls:
        return naval_cls(unit)

    return unit
