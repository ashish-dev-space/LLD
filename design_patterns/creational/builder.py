# Builder Pattern
#
# Builds a complex object step by step. It separates the construction
# of a complex object from its representation, so that the same
# construction process can create different representations.
#
# Use Case                  Why Builder
# SQL Query builder         Chain clauses (SELECT, WHERE, ORDER BY) flexibly
# HTTP Request builder      Set headers, body, method independently
# Config / Report objects   Optional fields with sensible defaults
# ── Product ───────────────────────────────────────────────────────────────────


class Pizza:
    def __init__(self):
        self.size = None
        self.crust = None
        self.sauce = None
        self.toppings = []

    def __str__(self):
        toppings = ", ".join(self.toppings) if self.toppings else "none"
        return (
            f"Pizza(size={self.size}, crust={self.crust}, "
            f"sauce={self.sauce}, toppings=[{toppings}])"
        )


# ── Builder ───────────────────────────────────────────────────────────────────


class PizzaBuilder:
    def __init__(self):
        self._pizza = Pizza()

    def set_size(self, size: str) -> "PizzaBuilder":
        self._pizza.size = size
        return self

    def set_crust(self, crust: str) -> "PizzaBuilder":
        self._pizza.crust = crust
        return self

    def set_sauce(self, sauce: str) -> "PizzaBuilder":
        self._pizza.sauce = sauce
        return self

    def add_topping(self, topping: str) -> "PizzaBuilder":
        self._pizza.toppings.append(topping)
        return self

    def build(self) -> Pizza:
        return self._pizza


# ── Director (optional) ───────────────────────────────────────────────────────
# Encapsulates predefined construction recipes.


class PizzaDirector:
    def make_margherita(self) -> Pizza:
        return (
            PizzaBuilder()
            .set_size("medium")
            .set_crust("thin")
            .set_sauce("tomato")
            .add_topping("mozzarella")
            .add_topping("basil")
            .build()
        )

    def make_bbq_loaded(self) -> Pizza:
        return (
            PizzaBuilder()
            .set_size("large")
            .set_crust("thick")
            .set_sauce("bbq")
            .add_topping("chicken")
            .add_topping("onions")
            .add_topping("cheddar")
            .build()
        )


# ── Driver Code ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Using the Director for predefined recipes
    director = PizzaDirector()
    print(director.make_margherita())
    print(director.make_bbq_loaded())

    # Building a custom pizza directly (no Director needed)
    custom = (
        PizzaBuilder()
        .set_size("small")
        .set_crust("stuffed")
        .set_sauce("pesto")
        .add_topping("mushrooms")
        .build()
    )
    print(custom)

# Output:
# Pizza(size=medium, crust=thin, sauce=tomato, toppings=[mozzarella, basil])
# Pizza(size=large, crust=thick, sauce=bbq, toppings=[chicken, onions, cheddar])
# Pizza(size=small, crust=stuffed, sauce=pesto, toppings=[mushrooms])
