from collections.abc import Iterable
from copy import deepcopy
from enum import Enum
from fractions import Fraction as F
from polycalculator.trait import Trait as T
from attrs import define, field


@define(slots=True)
class Unit:
    cost: int
    max_hp: int
    attack: F
    defense: F
    movement: int
    range: int
    traits: list[T]
    current_hp: F = field()

    @current_hp.default  # type: ignore[attr-defined]
    def _default_current_hp(self):
        return F(self.max_hp)


class UnitTemplate(Enum):
    """All the default Polytopia units. For easy copying."""

    DEFAULT_WARRIOR = Unit(2, 10, F(2), F(2), 1, 1, [T.DASH, T.FORTIFY])  # type: ignore

    # Normal
    WARRIOR = Unit(2, 10, F(2), F(2), 1, 1, [T.DASH, T.FORTIFY])  # type: ignore
    ARCHER = Unit(3, 10, F(2), F(1), 1, 2, [T.DASH, T.FORTIFY])  # type: ignore
    RIDER = Unit(3, 10, F(2), F(1), 2, 1, [T.DASH, T.ESCAPE, T.FORTIFY])  # type: ignore
    CATAPULT = Unit(8, 10, F(4), F(0), 1, 3, [T.STIFF])  # type: ignore
    KNIGHT = Unit(8, 10, F(7, 2), F(1), 3, 1, [T.DASH, T.PERSIST, T.FORTIFY])  # type: ignore
    SWORDSMAN = Unit(5, 15, F(3), F(3), 1, 1, [T.DASH])  # type: ignore
    DEFENDER = Unit(3, 15, F(1), F(3), 1, 1, [T.FORTIFY])  # type: ignore
    CLOAK = Unit(
        8,
        5,
        F(2),
        F(1, 2),
        2,
        1,
        [T.HIDE, T.INFILTRATE, T.DASH, T.SCOUT, T.CREEP, T.STATIC, T.STIFF],  # type: ignore
    )
    DAGGER = Unit(
        2,
        10,
        F(2),
        F(1),
        1,
        1,
        [T.SURPRISE, T.DASH, T.INDEPENDENT, T.STATIC],  # type: ignore
    )
    MIND_BENDER = Unit(5, 10, F(0), F(1), 1, 1, [T.HEAL, T.CONVERT, T.STIFF])  # type: ignore
    GIANT = Unit(10, 40, F(5), F(4), 1, 1, [T.STATIC])  # type: ignore
    # Naval
    DEFAULT_RAFT = Unit(2, 10, F(0), F(2), 2, 0, [T.CARRY, T.STATIC, T.STIFF])  # type: ignore
    DEFAULT_SCOUT = Unit(7, 10, F(2), F(1), 3, 2, [T.DASH, T.CARRY, T.SCOUT, T.STATIC])  # type: ignore
    DEFAULT_RAMMER = Unit(7, 10, F(3), F(3), 3, 1, [T.DASH, T.CARRY, T.STATIC])  # type: ignore
    DEFAULT_BOMBER = Unit(
        17,
        10,
        F(3),
        F(2),
        2,
        3,
        [T.CARRY, T.SPLASH, T.STATIC, T.STIFF],  # type: ignore
    )
    JUGGERNAUT = Unit(10, 40, F(4), F(4), 2, 1, [T.CARRY, T.STATIC, T.STIFF, T.STOMP])  # type: ignore
    PIRATE = Unit(
        2,
        10,
        F(2),
        F(1),
        2,
        1,
        [T.SURPRISE, T.DASH, T.INDEPENDENT, T.STATIC],  # type: ignore
    )
    # Aquarion
    TRIDENTION = Unit(8, 10, F(5, 2), F(1), 2, 2, [T.DASH, T.PERSIST])  # type: ignore
    SHARK = Unit(8, 10, F(7, 2), F(2), 3, 1, [T.DASH, T.SURPRISE])  # type: ignore
    JELLY = Unit(8, 20, F(2), F(2), 2, 1, [T.TENTACLES, T.STIFF, T.STATIC])  # type: ignore
    PUFFER = Unit(8, 10, F(4), F(0), 2, 3, [T.DRENCH])  # type: ignore
    CRAB = Unit(10, 40, F(4), F(4), 2, 1, [T.ESCAPE, T.AUTOFLOOD, T.STATIC])  # type: ignore
    # Elyrion
    POLYTAUR = Unit(
        3,
        15,
        F(3),
        F(1),
        1,
        1,
        [T.DASH, T.INDEPENDENT, T.FORTIFY, T.STATIC],  # type: ignore
    )
    EGG = Unit(10, 10, F(0), F(2), 1, 1, [T.GROW, T.FORTIFY, T.STIFF, T.STATIC])  # type: ignore
    BABY_DRAGON = Unit(
        10,
        15,
        F(3),
        F(3),
        2,
        1,
        [T.GROW, T.DASH, T.ESCAPE, T.SCOUT, T.STATIC],  # type: ignore
    )
    FIRE_DRAGON = Unit(10, 20, F(4), F(3), 3, 2, [T.DASH, T.SPLASH, T.SCOUT, T.STATIC])  # type: ignore
    # Polaris
    MOONI = Unit(5, 10, F(0), F(1), 1, 1, [T.AUTO_FREEZE, T.SKATE, T.STIFF, T.STATIC])  # type: ignore
    ICE_ARCHER = Unit(3, 10, F(0), F(1), 1, 2, [T.DASH, T.FREEZE, T.FORTIFY, T.STIFF])  # type: ignore
    BATTLE_SLED = Unit(5, 15, F(3), F(2), 2, 1, [T.DASH, T.ESCAPE, T.SKATE])  # type: ignore
    ICE_FORTRESS = Unit(15, 20, F(4), F(3), 1, 2, [T.SKATE, T.SCOUT])  # type: ignore
    GAAMI = Unit(10, 30, F(4), F(3), 1, 1, [T.AUTO_FREEZE, T.FREEZE_AREA, T.STATIC])  # type: ignore
    # Cymanti
    HEXAPOD = Unit(3, 5, F(3), F(1), 2, 1, [T.DASH, T.ESCAPE, T.SNEAK, T.CREEP])  # type: ignore
    DOOMUX = Unit(10, 20, F(4), F(2), 3, 1, [T.DASH, T.CREEP, T.EXPLODE])  # type: ignore
    KITON = Unit(3, 15, F(1), F(3), 1, 1, [T.POISON])  # type: ignore
    PHYCHI = Unit(3, 15, F(1), F(1), 2, 2, [T.DASH, T.POISON, T.SURPRISE])  # type: ignore
    SHAMAN = Unit(5, 10, F(1), F(1), 1, 1, [T.CONVERT, T.BOOST, T.STATIC])  # type: ignore
    EXIDA = Unit(8, 10, F(3), F(1), 1, 3, [T.POISON, T.SPLASH])  # type: ignore
    CENTIPEDE = Unit(10, 20, F(4), F(3), 2, 1, [T.DASH, T.EAT, T.CREEP, T.STATIC])  # type: ignore
    SEGMENT = Unit(1, 10, F(4), F(3), 2, 1, [T.DASH, T.EAT, T.CREEP, T.STATIC])  # type: ignore


class UnitBuilder:
    def __init__(self, base: Unit):
        self._unit = deepcopy(base)
        self._current_hp_set = False
        self._defense_bonus = F(1)
        self._poisoned = False

    # region sugar
    @classmethod
    def from_template(cls, template: UnitTemplate) -> "UnitBuilder":
        return cls(template.value)

    @classmethod
    def warrior(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.WARRIOR)

    @classmethod
    def rider(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.RIDER)

    @classmethod
    def archer(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.ARCHER)

    @classmethod
    def catapult(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.CATAPULT)

    @classmethod
    def knight(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.KNIGHT)

    @classmethod
    def swordsman(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.SWORDSMAN)

    @classmethod
    def defender(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.DEFENDER)

    @classmethod
    def cloak(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.CLOAK)

    @classmethod
    def dagger(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.DAGGER)

    @classmethod
    def mind_bender(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.MIND_BENDER)

    @classmethod
    def giant(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.GIANT)

    @classmethod
    def raft(cls, unit: UnitTemplate = UnitTemplate.DEFAULT_WARRIOR) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.DEFAULT_RAFT).with_max_hp(
            unit.value.max_hp
        )

    @classmethod
    def scout(cls, unit: UnitTemplate = UnitTemplate.DEFAULT_WARRIOR) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.DEFAULT_RAFT).with_max_hp(
            unit.value.max_hp
        )

    @classmethod
    def rammer(cls, unit: UnitTemplate = UnitTemplate.DEFAULT_WARRIOR) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.DEFAULT_RAFT).with_max_hp(
            unit.value.max_hp
        )

    @classmethod
    def bomber(cls, unit: UnitTemplate = UnitTemplate.DEFAULT_WARRIOR) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.DEFAULT_RAFT).with_max_hp(
            unit.value.max_hp
        )

    @classmethod
    def juggernaut(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.JUGGERNAUT)

    @classmethod
    def pirate(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.PIRATE)

    @classmethod
    def tridention(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.TRIDENTION)

    @classmethod
    def shark(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.SHARK)

    @classmethod
    def jelly(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.JELLY)

    @classmethod
    def puffer(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.PUFFER)

    @classmethod
    def crab(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.CRAB)

    @classmethod
    def polytar(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.POLYTAUR)

    @classmethod
    def egg(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.EGG)

    @classmethod
    def baby_dragon(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.BABY_DRAGON)

    @classmethod
    def fire_dragon(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.FIRE_DRAGON)

    @classmethod
    def mooni(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.MOONI)

    @classmethod
    def ice_archer(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.ICE_ARCHER)

    @classmethod
    def battle_sled(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.BATTLE_SLED)

    @classmethod
    def ice_fortress(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.ICE_FORTRESS)

    @classmethod
    def gaami(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.GAAMI)

    @classmethod
    def hexapod(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.HEXAPOD)

    @classmethod
    def doomux(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.DOOMUX)

    @classmethod
    def kiton(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.KITON)

    @classmethod
    def phychi(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.PHYCHI)

    @classmethod
    def shaman(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.SHAMAN)

    @classmethod
    def exida(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.EXIDA)

    @classmethod
    def centipede(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.CENTIPEDE)

    @classmethod
    def segment(cls) -> "UnitBuilder":
        return cls.from_template(UnitTemplate.SEGMENT)

    # endregion sugar

    # Mutator methods
    def with_max_hp(self, hp: int) -> "UnitBuilder":
        self._unit.max_hp = hp
        return self

    def with_current_hp(self, hp: F) -> "UnitBuilder":
        self._unit.current_hp = hp
        self._hp_set = True
        return self

    def with_attack(self, attack: F) -> "UnitBuilder":
        self._unit.attack = attack
        return self

    def with_defense(self, defense: F) -> "UnitBuilder":
        self._unit.defense = defense
        return self

    def add_trait(self, trait: T) -> "UnitBuilder":
        if trait not in self._unit.traits:
            self._unit.traits.append(trait)
        return self

    def add_traits(self, traits: Iterable[T]) -> "UnitBuilder":
        for trait in traits:
            self.add_trait(trait)
        return self

    def veteran(self) -> "UnitBuilder":
        self._unit.max_hp += 5
        if not self._hp_set:
            self._unit.current_hp = F(self._unit.max_hp)
        return self

    def boosted(self) -> "UnitBuilder":
        self._unit.movement += 1
        self._unit.attack += F(1, 2)
        return self

    def poisoned(self) -> "UnitBuilder":
        self._defense_bonus = F(4, 5)
        self._poisoned = True
        return self

    def defense_bonus(self) -> "UnitBuilder":
        if not self._poisoned:
            self._defense_bonus = F(3, 2)
        return self

    def wall_bonus(self) -> "UnitBuilder":
        if not self._poisoned:
            self._defense_bonus = F(4)
        return self

    def build(self) -> Unit:
        self._unit.defense *= self._defense_bonus
        return self._unit
