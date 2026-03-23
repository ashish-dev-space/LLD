# Decorator Pattern
#
# Attaches additional responsibilities to an object dynamically.
# Provides a flexible alternative to subclassing for extending functionality.
#
# Key Idea:
#   Wrap an object inside another object (the decorator) that adds behaviour
#   before/after delegating to the wrapped object.  Because decorators share
#   the same interface as the object they wrap, they can be stacked infinitely.
#
# Use Case                          Why Decorator
# Coffee / pizza toppings            Each topping adds cost & description dynamically
# I/O streams (buffered, encrypted)  Layer behaviours on a base stream
# Logging / metrics / retry          Wrap a service call transparently
# UI components (scroll, border)     Add visual features without modifying the widget
#
# Structure:
#
#   Component  (ABC)            ← common interface
#       │
#       ├── ConcreteComponent   ← base object (e.g. plain coffee)
#       │
#       └── Decorator (ABC)     ← holds a reference to a Component
#               │
#               ├── ConcreteDecoratorA  (e.g. MilkDecorator)
#               └── ConcreteDecoratorB  (e.g. SugarDecorator)
#
# OCP (Open-Closed Principle):
#   New toppings can be added without modifying existing coffee or decorator classes.
from abc import ABC
from abc import abstractmethod


# ── Component Interface ───────────────────────────────────────────────────────


class Coffee(ABC):
    """Base interface — every coffee (plain or decorated) must expose these."""

    @abstractmethod
    def cost(self) -> float:
        pass

    @abstractmethod
    def description(self) -> str:
        pass


# ── Concrete Components (base coffees) ────────────────────────────────────────


class Espresso(Coffee):
    def cost(self) -> float:
        return 100.0

    def description(self) -> str:
        return "Espresso"


class HouseBlend(Coffee):
    def cost(self) -> float:
        return 80.0

    def description(self) -> str:
        return "House Blend"


# ── Base Decorator ────────────────────────────────────────────────────────────
# Implements Coffee and holds a reference to a Coffee.
# Subclasses override cost()/description() to add their own behaviour and
# delegate to the wrapped object via super().


class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee  # wrapped component

    def cost(self) -> float:
        return self._coffee.cost()

    def description(self) -> str:
        return self._coffee.description()


# ── Concrete Decorators (toppings) ────────────────────────────────────────────


class MilkDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 20.0

    def description(self) -> str:
        return self._coffee.description() + " + Milk"


class SugarDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 5.0

    def description(self) -> str:
        return self._coffee.description() + " + Sugar"


class WhipCreamDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 30.0

    def description(self) -> str:
        return self._coffee.description() + " + Whip Cream"


class CaramelDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 35.0

    def description(self) -> str:
        return self._coffee.description() + " + Caramel"


# ── Client code ───────────────────────────────────────────────────────────────
# The client works with Coffee — it never knows how many layers of decorators
# are wrapped around the base component.


def print_order(coffee: Coffee) -> None:
    print(f"  {coffee.description()}  →  ₹{coffee.cost():.2f}")


# ── Driver Code ───────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # 1. Plain espresso — no decorators
    order1 = Espresso()
    print("Order 1:")
    print_order(order1)

    # 2. House Blend + Milk + Sugar — two decorators stacked
    order2 = SugarDecorator(MilkDecorator(HouseBlend()))
    print("Order 2:")
    print_order(order2)

    # 3. Espresso + Milk + Whip Cream + Caramel — three decorators stacked
    order3 = CaramelDecorator(WhipCreamDecorator(MilkDecorator(Espresso())))
    print("Order 3:")
    print_order(order3)

    # 4. Double milk! Decorators can repeat — try that with subclassing
    order4 = MilkDecorator(MilkDecorator(HouseBlend()))
    print("Order 4:")
    print_order(order4)

# Output:
# Order 1:
#   Espresso  →  ₹100.00
# Order 2:
#   House Blend + Milk + Sugar  →  ₹105.00
# Order 3:
#   Espresso + Milk + Whip Cream + Caramel  →  ₹185.00
# Order 4:
#   House Blend + Milk + Milk  →  ₹120.00
