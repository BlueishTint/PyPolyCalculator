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

To represent units, PolyCalculator gives them each a class.
These classes allow you to create units with specific attributes
such as cost, max_hp, attack, defense, range, traits, and status_effects.

For example:

>>> from polycalculator.unit import Warrior
>>> Warrior()
Warrior(cost=2, current_hp=100, max_hp=100, attack=20, defense=20, range=1, traits=frozenset({<Trait.DASH: 'dash'>, <Trait.FORTIFY: 'fortify'>}), status_effects=set())
