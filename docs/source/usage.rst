Usage
=====

.. _installation:

Installation
------------

To use PolyCalculator, first install it using pip:

.. code-block:: console

   (.venv) $ pip install polycalculator

Creating units
----------------

To build a unit, you can use the `UnitBuilder` class.
This class allows you to create a unit with specific attributes
such as cost, max_hp, attack, defense, movement, range, and traits.

It also has helper methods to create specific types of units:

.. autofunction:: polycalculator.unit.UnitBuilder.warrior

For example:

>>> from polycalculator.unit import UnitBuilder
>>> UnitBuilder.warrior().build()
Unit(cost=2, max_hp=10, attack=Fraction(2, 1), defense=Fraction(2, 1), movement=1, range=1, traits=[<Trait.DASH: 3>, <Trait.FORTIFY: 5>], current_hp=Fraction(10, 1))
