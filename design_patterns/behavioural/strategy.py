# Strategy Pattern
#
# Defines a family of algorithms, encapsulates each one, and makes them
# interchangeable. The context delegates the algorithm to a strategy object
# instead of implementing it directly — behaviour can be swapped at runtime.
#
# Use Case                  Why Strategy
# Sorting                   Bubble, Merge, Quick — swap without changing caller
# Discount pricing          Percentage, Flat, No discount — rules change often
# Navigation                Fastest, Shortest, Avoid tolls
# Authentication            Password, OAuth, OTP
# Compression               ZIP, GZIP, BZIP2
from abc import ABC
from abc import abstractmethod


# ── Example 1 : Discount Pricing ──────────────────────────────────────────────


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, price: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, price: float) -> float:
        return price


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: float):
        self._percent = percent

    def apply(self, price: float) -> float:
        return price * (1 - self._percent / 100)


class FlatDiscount(DiscountStrategy):
    def __init__(self, flat: float):
        self._flat = flat

    def apply(self, price: float) -> float:
        return max(0.0, price - self._flat)


# Context — holds a strategy, delegates pricing to it
class ShoppingCart:
    def __init__(self, strategy: DiscountStrategy = NoDiscount()):
        self._strategy = strategy

    def set_strategy(self, strategy: DiscountStrategy) -> None:
        """Swap discount strategy at runtime."""
        self._strategy = strategy

    def checkout(self, price: float) -> None:
        final = self._strategy.apply(price)
        print(f"Original: ${price:.2f}  →  Final: ${final:.2f}")


# ── Example 2 : Sorting ───────────────────────────────────────────────────────


class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list[int]) -> list[int]:
        pass


class BubbleSort(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        arr = data[:]
        n = len(arr)
        for i in range(n):
            for j in range(n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr


class MergeSort(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        if len(data) <= 1:
            return data[:]
        mid = len(data) // 2
        left = self.sort(data[:mid])
        right = self.sort(data[mid:])
        return self._merge(left, right)

    def _merge(self, left: list[int], right: list[int]) -> list[int]:
        result, i, j = [], 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        return result + left[i:] + right[j:]


class PythonBuiltinSort(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        return sorted(data)


# Context
class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy) -> None:
        self._strategy = strategy

    def sort(self, data: list[int]) -> list[int]:
        return self._strategy.sort(data)


# ── Driver Code ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # --- Pricing ---
    cart = ShoppingCart()
    cart.checkout(200.00)  # no discount

    cart.set_strategy(PercentageDiscount(20))
    cart.checkout(200.00)  # 20% off

    cart.set_strategy(FlatDiscount(30))
    cart.checkout(200.00)  # $30 off

    print()

    # --- Sorting ---
    data = [5, 3, 8, 1, 9, 2]
    sorter = Sorter(BubbleSort())
    print(f"Bubble : {sorter.sort(data)}")

    sorter.set_strategy(MergeSort())
    print(f"Merge  : {sorter.sort(data)}")

    sorter.set_strategy(PythonBuiltinSort())
    print(f"Builtin: {sorter.sort(data)}")

# Output:
# Original: $200.00  →  Final: $200.00
# Original: $200.00  →  Final: $160.00
# Original: $200.00  →  Final: $170.00
#
# Bubble : [1, 2, 3, 5, 8, 9]
# Merge  : [1, 2, 3, 5, 8, 9]
# Builtin: [1, 2, 3, 5, 8, 9]
