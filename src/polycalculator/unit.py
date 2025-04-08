"""Contains all code to define Units and ways to create them."""

from collections.abc import Iterable
from copy import deepcopy
from enum import Enum
from fractions import Fraction as F

from attrs import define, field

from polycalculator.status_effect import StatusEffect
from polycalculator.trait import Trait as T


@define(slots=True, kw_only=True)
class Unit:
    """
    A Polytopia unit.

    When initializing a `Unit`,
    `current_hp` is automatically set to `max_hp` unless otherwise specified.

    Attributes
    ----------
    cost : int
        The cost of the unit in stars.
    max_hp : int
        The maximum hit points of the unit.
    attack : Fraction
        The attack stat of the unit.
    defense : Fraction
        The defense stat of the unit.
    movement : int, default 1
        The movement stat of the unit.
    range : int, default 1
        The range stat of the unit.
    traits : list[Trait], optional
        A list of traits the unit has.
    current_hp : Fraction, default `max_hp`
        The current hit points of the unit.
    status_effects : set[StatusEffect], default `set()`

    Examples
    --------
    >>> unit = Unit(cost=2, max_hp=10, attack=F(2), defense=F(2))
    >>> unit.current_hp
    10
    >>> unit.movement
    1
    >>> unit.range
    1
    >>> unit.traits
    []
    >>> unit.status_effects
    set()

    """

    cost: int
    max_hp: int
    attack: F
    defense: F
    movement: int = 1
    range: int = 1
    traits: list[T] = field(factory=list)
    status_effects: set[StatusEffect] = field(factory=set)
    current_hp: F = field()

    @current_hp.default  # type: ignore[attr-defined]
    def _default_current_hp(self):
        return F(self.max_hp)

    @property
    def defense_bonus(self) -> F:
        """
        Calculate the defense bonus based on the unit's status effects.

        Returns
        -------
        Fraction
            The defense bonus as a fraction.
        """
        if StatusEffect.POISONED in self.status_effects:
            return F(7, 10)
        if StatusEffect.FORTIFIED in self.status_effects:
            return F(3, 2)
        if StatusEffect.WALLED in self.status_effects:
            return F(4, 1)
        return F(1, 1)


class UnitTemplate(Enum):
    """All the default Polytopia units."""

    DEFAULT_WARRIOR = Unit(
        cost=2,
        max_hp=10,
        attack=F(2),
        defense=F(2),
        traits=[T.DASH, T.FORTIFY],
    )  # type: ignore

    # Normal
    WARRIOR = Unit(
        cost=2,
        max_hp=10,
        attack=F(2),
        defense=F(2),
        traits=[T.DASH, T.FORTIFY],
    )  # type: ignore
    ARCHER = Unit(
        cost=3,
        max_hp=10,
        attack=F(2),
        defense=F(1),
        range=2,
        traits=[T.DASH, T.FORTIFY],
    )  # type: ignore
    RIDER = Unit(
        cost=3,
        max_hp=10,
        attack=F(2),
        defense=F(1),
        movement=2,
        traits=[T.DASH, T.ESCAPE, T.FORTIFY],
    )  # type: ignore
    CATAPULT = Unit(
        cost=8,
        max_hp=10,
        attack=F(4),
        defense=F(0),
        range=3,
        traits=[T.STIFF],
    )  # type: ignore
    KNIGHT = Unit(
        cost=8,
        max_hp=10,
        attack=F(7, 2),
        defense=F(1),
        movement=3,
        traits=[T.DASH, T.PERSIST, T.FORTIFY],
    )  # type: ignore
    SWORDSMAN = Unit(
        cost=5,
        max_hp=15,
        attack=F(3),
        defense=F(3),
        traits=[T.DASH],
    )  # type: ignore
    DEFENDER = Unit(
        cost=3,
        max_hp=15,
        attack=F(1),
        defense=F(3),
        traits=[T.FORTIFY],
    )  # type: ignore
    CLOAK = Unit(
        cost=8,
        max_hp=5,
        attack=F(2),
        defense=F(1, 2),
        movement=2,
        traits=[T.HIDE, T.INFILTRATE, T.DASH, T.SCOUT, T.CREEP, T.STATIC, T.STIFF],  # type: ignore
    )
    DAGGER = Unit(
        cost=2,
        max_hp=10,
        attack=F(2),
        defense=F(1),
        traits=[T.SURPRISE, T.DASH, T.INDEPENDENT, T.STATIC],  # type: ignore
    )
    MIND_BENDER = Unit(
        cost=5,
        max_hp=10,
        attack=F(0),
        defense=F(1),
        traits=[T.HEAL, T.CONVERT, T.STIFF],
    )  # type: ignore
    GIANT = Unit(
        cost=10,
        max_hp=40,
        attack=F(5),
        defense=F(4),
        traits=[T.STATIC],
    )  # type: ignore
    # Naval
    DEFAULT_RAFT = Unit(
        cost=2,
        max_hp=10,
        attack=F(0),
        defense=F(2),
        movement=2,
        range=0,
        traits=[T.CARRY, T.STATIC, T.STIFF],
    )  # type: ignore
    DEFAULT_SCOUT = Unit(
        cost=7,
        max_hp=10,
        attack=F(2),
        defense=F(1),
        movement=3,
        range=2,
        traits=[T.DASH, T.CARRY, T.SCOUT, T.STATIC],
    )  # type: ignore
    DEFAULT_RAMMER = Unit(
        cost=7,
        max_hp=10,
        attack=F(3),
        defense=F(3),
        movement=3,
        traits=[T.DASH, T.CARRY, T.STATIC],
    )  # type: ignore
    DEFAULT_BOMBER = Unit(
        cost=17,
        max_hp=10,
        attack=F(3),
        defense=F(2),
        movement=2,
        range=3,
        traits=[T.CARRY, T.SPLASH, T.STATIC, T.STIFF],  # type: ignore
    )
    JUGGERNAUT = Unit(
        cost=10,
        max_hp=40,
        attack=F(4),
        defense=F(4),
        movement=2,
        traits=[T.CARRY, T.STATIC, T.STIFF, T.STOMP],
    )  # type: ignore
    PIRATE = Unit(
        cost=2,
        max_hp=10,
        attack=F(2),
        defense=F(1),
        movement=2,
        traits=[T.SURPRISE, T.DASH, T.INDEPENDENT, T.STATIC],  # type: ignore
    )
    # Aquarion
    TRIDENTION = Unit(
        cost=8,
        max_hp=10,
        attack=F(5, 2),
        defense=F(1),
        movement=2,
        range=2,
        traits=[T.DASH, T.PERSIST],
    )  # type: ignore
    SHARK = Unit(
        cost=8,
        max_hp=10,
        attack=F(7, 2),
        defense=F(2),
        movement=3,
        traits=[T.DASH, T.SURPRISE],
    )  # type: ignore
    JELLY = Unit(
        cost=8,
        max_hp=20,
        attack=F(2),
        defense=F(2),
        movement=2,
        traits=[T.TENTACLES, T.STIFF, T.STATIC],
    )  # type: ignore
    PUFFER = Unit(
        cost=8,
        max_hp=10,
        attack=F(4),
        defense=F(0),
        movement=2,
        range=3,
        traits=[T.DRENCH],
    )  # type: ignore
    CRAB = Unit(
        cost=10,
        max_hp=40,
        attack=F(4),
        defense=F(4),
        movement=2,
        traits=[T.ESCAPE, T.AUTOFLOOD, T.STATIC],
    )  # type: ignore
    # Elyrion
    POLYTAUR = Unit(
        cost=3,
        max_hp=15,
        attack=F(3),
        defense=F(1),
        traits=[T.DASH, T.INDEPENDENT, T.FORTIFY, T.STATIC],  # type: ignore
    )
    EGG = Unit(
        cost=10,
        max_hp=10,
        attack=F(0),
        defense=F(2),
        traits=[T.GROW, T.FORTIFY, T.STIFF, T.STATIC],
    )  # type: ignore
    BABY_DRAGON = Unit(
        cost=10,
        max_hp=15,
        attack=F(3),
        defense=F(3),
        movement=2,
        traits=[T.GROW, T.DASH, T.ESCAPE, T.SCOUT, T.STATIC],  # type: ignore
    )
    FIRE_DRAGON = Unit(
        cost=10,
        max_hp=20,
        attack=F(4),
        defense=F(3),
        movement=3,
        range=2,
        traits=[T.DASH, T.SPLASH, T.SCOUT, T.STATIC],  # type: ignore
    )
    # Polaris
    MOONI = Unit(
        cost=5,
        max_hp=10,
        attack=F(0),
        defense=F(1),
        traits=[T.AUTO_FREEZE, T.SKATE, T.STIFF, T.STATIC],
    )  # type: ignore
    ICE_ARCHER = Unit(
        cost=3,
        max_hp=10,
        attack=F(0),
        defense=F(1),
        range=2,
        traits=[T.DASH, T.FREEZE, T.FORTIFY, T.STIFF],
    )  # type: ignore
    BATTLE_SLED = Unit(
        cost=5,
        max_hp=15,
        attack=F(3),
        defense=F(2),
        movement=2,
        traits=[T.DASH, T.ESCAPE, T.SKATE],
    )  # type: ignore
    ICE_FORTRESS = Unit(
        cost=15,
        max_hp=20,
        attack=F(4),
        defense=F(3),
        range=2,
        traits=[T.SKATE, T.SCOUT],
    )  # type: ignore
    GAAMI = Unit(
        cost=10,
        max_hp=30,
        attack=F(4),
        defense=F(3),
        traits=[T.AUTO_FREEZE, T.FREEZE_AREA, T.STATIC],
    )  # type: ignore
    # Cymanti
    HEXAPOD = Unit(
        cost=3,
        max_hp=5,
        attack=F(3),
        defense=F(1),
        movement=2,
        traits=[T.DASH, T.ESCAPE, T.SNEAK, T.CREEP],
    )  # type: ignore
    DOOMUX = Unit(
        cost=10,
        max_hp=20,
        attack=F(4),
        defense=F(2),
        movement=3,
        traits=[T.DASH, T.CREEP, T.EXPLODE],
    )  # type: ignore
    KITON = Unit(
        cost=3,
        max_hp=15,
        attack=F(1),
        defense=F(3),
        traits=[T.POISON],
    )  # type: ignore
    PHYCHI = Unit(
        cost=3,
        max_hp=15,
        attack=F(1),
        defense=F(1),
        movement=2,
        range=2,
        traits=[T.DASH, T.POISON, T.SURPRISE],
    )  # type: ignore
    SHAMAN = Unit(
        cost=5,
        max_hp=10,
        attack=F(1),
        defense=F(1),
        traits=[T.CONVERT, T.BOOST, T.STATIC],
    )  # type: ignore
    EXIDA = Unit(
        cost=8,
        max_hp=10,
        attack=F(3),
        defense=F(1),
        range=3,
        traits=[T.POISON, T.SPLASH],
    )  # type: ignore
    CENTIPEDE = Unit(
        cost=10,
        max_hp=20,
        attack=F(4),
        defense=F(3),
        movement=2,
        traits=[T.DASH, T.EAT, T.CREEP, T.STATIC],
    )  # type: ignore
    SEGMENT = Unit(
        cost=1,
        max_hp=10,
        attack=F(4),
        defense=F(3),
        movement=2,
        traits=[T.DASH, T.EAT, T.CREEP, T.STATIC],
    )  # type: ignore


class UnitBuilder:
    """
    A builder class for creating and customizing `Unit` objects.

    This class provides a fluent interface to configure various attributes
    and traits of a `Unit` before instantiation.

    Attributes
    ----------
    _unit : Unit
        A deep copy of the base unit to be customized.
    _current_hp_set : bool
        Flag indicating if the current HP has been explicitly set.

    Examples
    --------
    >>> unit = UnitBuilder.warrior().with_max_hp(15).with_attack(3).build()
    >>> unit.status_effects
    {<StatusEffect.VETERAN: 5>}

    """

    def __init__(self, base: Unit):
        """
        Initialize the UnitBuilder with a base unit.

        Parameters
        ----------
        base : Unit
            The base unit to be used as a template for building.
        """
        self._unit = deepcopy(base)
        self._current_hp_set = False

    # region sugar
    @classmethod
    def from_template(cls, template: UnitTemplate) -> "UnitBuilder":
        """
        Create a UnitBuilder from a unit template.

        Parameters
        ----------
        template : UnitTemplate
            The template to create the unit from.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized with the template's unit.
        """
        return cls(template.value)

    @classmethod
    def warrior(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a warrior unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a warrior.
        """
        return cls.from_template(UnitTemplate.WARRIOR)

    @classmethod
    def rider(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a rider unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a rider.
        """
        return cls.from_template(UnitTemplate.RIDER)

    @classmethod
    def archer(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for an archer unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as an archer.
        """
        return cls.from_template(UnitTemplate.ARCHER)

    @classmethod
    def catapult(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a catapult unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a catapult.
        """
        return cls.from_template(UnitTemplate.CATAPULT)

    @classmethod
    def knight(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a knight unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a knight.
        """
        return cls.from_template(UnitTemplate.KNIGHT)

    @classmethod
    def swordsman(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a swordsman unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a swordsman.
        """
        return cls.from_template(UnitTemplate.SWORDSMAN)

    @classmethod
    def defender(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a defender unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a defender.
        """
        return cls.from_template(UnitTemplate.DEFENDER)

    @classmethod
    def cloak(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a cloak unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a cloak.
        """
        return cls.from_template(UnitTemplate.CLOAK)

    @classmethod
    def dagger(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a dagger unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a dagger.
        """
        return cls.from_template(UnitTemplate.DAGGER)

    @classmethod
    def mind_bender(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a mind bender unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a mind bender.
        """
        return cls.from_template(UnitTemplate.MIND_BENDER)

    @classmethod
    def giant(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a giant unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a giant.
        """
        return cls.from_template(UnitTemplate.GIANT)

    @classmethod
    def raft(cls, unit: UnitTemplate = UnitTemplate.DEFAULT_WARRIOR) -> "UnitBuilder":
        """
        Create a UnitBuilder for a raft unit.

        Parameters
        ----------
        unit : UnitTemplate, optional
            The unit template to derive the raft's max HP from,
            by default UnitTemplate.DEFAULT_WARRIOR.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a raft.
        """
        return cls.from_template(UnitTemplate.DEFAULT_RAFT).with_max_hp(
            unit.value.max_hp
        )

    @classmethod
    def scout(cls, unit: UnitTemplate = UnitTemplate.DEFAULT_WARRIOR) -> "UnitBuilder":
        """
        Create a UnitBuilder for a scout unit.

        Parameters
        ----------
        unit : UnitTemplate, optional
            The unit template to derive the scout's max HP from,
            by default UnitTemplate.DEFAULT_WARRIOR.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a scout.
        """
        return cls.from_template(UnitTemplate.DEFAULT_SCOUT).with_max_hp(
            unit.value.max_hp
        )

    @classmethod
    def rammer(cls, unit: UnitTemplate = UnitTemplate.DEFAULT_WARRIOR) -> "UnitBuilder":
        """
        Create a UnitBuilder for a rammer unit.

        Parameters
        ----------
        unit : UnitTemplate, optional
            The unit template to derive the rammer's max HP from,
            by default UnitTemplate.DEFAULT_WARRIOR.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a rammer.
        """
        return cls.from_template(UnitTemplate.DEFAULT_RAMMER).with_max_hp(
            unit.value.max_hp
        )

    @classmethod
    def bomber(cls, unit: UnitTemplate = UnitTemplate.DEFAULT_WARRIOR) -> "UnitBuilder":
        """
        Create a UnitBuilder for a bomber unit.

        Parameters
        ----------
        unit : UnitTemplate, optional
            The unit template to derive the bomber's max HP from,
            by default UnitTemplate.DEFAULT_WARRIOR.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a bomber.
        """
        return cls.from_template(UnitTemplate.DEFAULT_BOMBER).with_max_hp(
            unit.value.max_hp
        )

    @classmethod
    def juggernaut(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a juggernaut unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a juggernaut.
        """
        return cls.from_template(UnitTemplate.JUGGERNAUT)

    @classmethod
    def pirate(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a pirate unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a pirate.
        """
        return cls.from_template(UnitTemplate.PIRATE)

    @classmethod
    def tridention(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a tridention unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a tridention.
        """
        return cls.from_template(UnitTemplate.TRIDENTION)

    @classmethod
    def shark(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a shark unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a shark.
        """
        return cls.from_template(UnitTemplate.SHARK)

    @classmethod
    def jelly(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a jelly unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a jelly.
        """
        return cls.from_template(UnitTemplate.JELLY)

    @classmethod
    def puffer(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a puffer unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a puffer.
        """
        return cls.from_template(UnitTemplate.PUFFER)

    @classmethod
    def crab(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a crab unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a crab.
        """
        return cls.from_template(UnitTemplate.CRAB)

    @classmethod
    def polytaur(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a polytaur unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a polytaur.
        """
        return cls.from_template(UnitTemplate.POLYTAUR)

    @classmethod
    def egg(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for an egg unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as an egg.
        """
        return cls.from_template(UnitTemplate.EGG)

    @classmethod
    def baby_dragon(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a baby dragon unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a baby dragon.
        """
        return cls.from_template(UnitTemplate.BABY_DRAGON)

    @classmethod
    def fire_dragon(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a fire dragon unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a fire dragon.
        """
        return cls.from_template(UnitTemplate.FIRE_DRAGON)

    @classmethod
    def mooni(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a mooni unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a mooni.
        """
        return cls.from_template(UnitTemplate.MOONI)

    @classmethod
    def ice_archer(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for an ice archer unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as an ice archer.
        """
        return cls.from_template(UnitTemplate.ICE_ARCHER)

    @classmethod
    def battle_sled(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a battle sled unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a battle sled.
        """
        return cls.from_template(UnitTemplate.BATTLE_SLED)

    @classmethod
    def ice_fortress(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for an ice fortress unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as an ice fortress.
        """
        return cls.from_template(UnitTemplate.ICE_FORTRESS)

    @classmethod
    def gaami(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a gaami unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a gaami.
        """
        return cls.from_template(UnitTemplate.GAAMI)

    @classmethod
    def hexapod(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a hexapod unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a hexapod.
        """
        return cls.from_template(UnitTemplate.HEXAPOD)

    @classmethod
    def doomux(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a doomux unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a doomux.
        """
        return cls.from_template(UnitTemplate.DOOMUX)

    @classmethod
    def kiton(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a kiton unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a kiton.
        """
        return cls.from_template(UnitTemplate.KITON)

    @classmethod
    def phychi(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a phychi unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a phychi.
        """
        return cls.from_template(UnitTemplate.PHYCHI)

    @classmethod
    def shaman(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a shaman unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a shaman.
        """
        return cls.from_template(UnitTemplate.SHAMAN)

    @classmethod
    def exida(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for an exida unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as an exida.
        """
        return cls.from_template(UnitTemplate.EXIDA)

    @classmethod
    def centipede(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a centipede unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a centipede.
        """
        return cls.from_template(UnitTemplate.CENTIPEDE)

    @classmethod
    def segment(cls) -> "UnitBuilder":
        """
        Create a UnitBuilder for a segment unit.

        Returns
        -------
        UnitBuilder
            An instance of UnitBuilder initialized as a segment.
        """
        return cls.from_template(UnitTemplate.SEGMENT)

    # endregion sugar

    # Mutator methods
    def with_max_hp(self, hp: int) -> "UnitBuilder":
        """
        Set the maximum hit points for the unit.

        Parameters
        ----------
        hp : int
            The maximum hit points to set.

        Returns
        -------
        UnitBuilder
            The current instance of UnitBuilder.

        Notes
        -----
        This does not set the current HP. Use `with_current_hp` to set that separately.
        """
        self._unit.max_hp = hp
        return self

    def with_current_hp(self, hp: F) -> "UnitBuilder":
        """
        Set the current hit points for the unit.

        Parameters
        ----------
        hp : float
            The current hit points to set.

        Returns
        -------
        UnitBuilder
            The current instance of UnitBuilder.

        Notes
        -----
        If current_hp exceeds max_hp by more than 5, it will be capped at max_hp + 5.
        Then, if the unit is not already a veteran, it will be marked as such.
        """
        if (
            hp >= self._unit.max_hp + 5
            and StatusEffect.VETERAN not in self._unit.status_effects
        ):
            hp = F(self._unit.max_hp + 5)
            self._unit.status_effects.add(StatusEffect.VETERAN)
            return self.with_max_hp(int(hp))

        self._unit.current_hp = hp
        self._current_hp_set = True
        return self

    def with_attack(self, attack: float) -> "UnitBuilder":
        """
        Set the attack value for the unit.

        Parameters
        ----------
        attack : float
            The attack value to set.

        Returns
        -------
        UnitBuilder
            The current instance of UnitBuilder.
        """
        self._unit.attack = F(attack)
        return self

    def with_defense(self, defense: float) -> "UnitBuilder":
        """
        Set the defense value for the unit.

        Parameters
        ----------
        defense : float
            The defense value to set.

        Returns
        -------
        UnitBuilder
            The current instance of UnitBuilder.
        """
        self._unit.defense = F(defense)
        return self

    def add_trait(self, trait: T) -> "UnitBuilder":
        """
        Add a single trait to the unit.

        Parameters
        ----------
        trait : Trait
            The trait to add.

        Returns
        -------
        UnitBuilder
            The current instance of UnitBuilder.
        """
        if trait not in self._unit.traits:
            self._unit.traits.append(trait)
        return self

    def add_traits(self, traits: Iterable[T]) -> "UnitBuilder":
        """
        Add multiple traits to the unit.

        Parameters
        ----------
        traits : Iterable[Trait]
            An iterable of traits to add.

        Returns
        -------
        UnitBuilder
            The current instance of UnitBuilder.
        """
        for trait in traits:
            self.add_trait(trait)
        return self

    def veteran(self) -> "UnitBuilder":
        """
        Apply veteran status to the unit, increasing max HP by 5.

        Returns
        -------
        UnitBuilder
            The current instance of UnitBuilder.

        Notes
        -----
        If you haven't set the current HP, it will be set to the new max HP.
        If you have set the current HP, it will remain unchanged.
        """
        if StatusEffect.VETERAN in self._unit.status_effects:
            return self
        self._unit.status_effects.add(StatusEffect.VETERAN)
        self._unit.max_hp += 5
        if not self._current_hp_set:
            self._unit.current_hp = F(self._unit.max_hp)
        return self

    def boosted(self) -> "UnitBuilder":
        """
        Apply boosted status to the unit, increasing movement and attack.

        Returns
        -------
        UnitBuilder
            The current instance of UnitBuilder.
        """
        self._unit.status_effects.add(StatusEffect.BOOSTED)
        self._unit.movement += 1
        self._unit.attack += F(1, 2)
        return self

    def poisoned(self) -> "UnitBuilder":
        """
        Apply poisoned status to the unit, reducing defense.

        Returns
        -------
        UnitBuilder
            The current instance of UnitBuilder.

        Notes
        -----
        As in the game, this overrides any previous or subsequent defense bonuses.
        """
        self._unit.status_effects.add(StatusEffect.POISONED)
        self._unit.status_effects.discard(StatusEffect.FORTIFIED)
        self._unit.status_effects.discard(StatusEffect.WALLED)
        self._defense_bonus = F(7, 10)
        return self

    def defense_bonus(self) -> "UnitBuilder":
        """
        Apply a defense bonus to the unit if not poisoned.

        Returns
        -------
        UnitBuilder
            The current instance of UnitBuilder.
        """
        if StatusEffect.POISONED not in self._unit.status_effects:
            self._unit.status_effects.discard(StatusEffect.FORTIFIED)
        return self

    def wall_bonus(self) -> "UnitBuilder":
        """
        Apply a wall defense bonus to the unit if not poisoned.

        Returns
        -------
        UnitBuilder
            The current instance of UnitBuilder.
        """
        if StatusEffect.POISONED not in self._unit.status_effects:
            self._unit.status_effects.discard(StatusEffect.FORTIFIED)
            self._unit.status_effects.add(StatusEffect.WALLED)
        return self

    def takes_retaliation(self) -> "UnitBuilder":
        """
        Force unit to take retaliation.

        Returns
        -------
        UnitBuilder
            The current instance of UnitBuilder.
        """
        self._unit.status_effects.add(StatusEffect.TAKES_RETALIATION)
        return self

    def build(self) -> Unit:
        """
        Finalize the unit configuration and return the built unit.

        Returns
        -------
        Unit
            The fully constructed unit with the specified attributes and traits.
        """
        return self._unit
