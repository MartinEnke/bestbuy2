from abc import ABC, abstractmethod


class Promotion(ABC):
    """
    Abstracts base class for all promotions.
    """

    def __init__(self, name: str):
        """
        Initializes a Promotion.
        """
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity: int) -> float:
        """
        Calculates the total price after applying this promotion.
        """
        pass

    def apply(self, shopping_list, full_price: float) -> float:
        """
        Applies this promotion across the full shopping_list.

        Default implementation:
          - For each (product, qty) in shopping_list, call apply_promotion.
          - Sum those line totals and return.

        Promotions that need to look at the entire basket (e.g. bundle deals)
        can override this method.
        """
        discounted_total = 0.0
        for product, qty in shopping_list:
            discounted_total += self.apply_promotion(product, qty)
        return discounted_total


class PercentDiscount(Promotion):
    """
    Applies a percentage-based discount on the total price.
    """

    def __init__(self, name: str, percent: float):
        """
        Initializes a percentage discount promotion.
        """
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity: int) -> float:
        """
        Computes discounted total: total = price*qty - (percent% of price*qty).
        """
        total = product.price * quantity
        discount = total * (self.percent / 100)
        return total - discount


class SecondHalfPrice(Promotion):
    """
    “Second half price” promotion: first item full price, subsequent items at half price.
    """

    def __init__(self, name: str):
        """
        Initialize a second-half-price promotion.
        """
        super().__init__(name)

    def apply_promotion(self, product, quantity: int) -> float:
        """
        Calculates total cost where the first unit is full price,
        and each additional unit is half price.
        """
        if quantity <= 0:
            return 0.0
        full_price = product.price
        half_count = quantity - 1
        return full_price + half_count * (product.price / 2)


class ThirdOneFree(Promotion):
    """
    “Buy 2 get 1 free” promotion: every third item is free.
    """

    def __init__(self, name: str):
        """
        Initializes a buy‑2‑get‑1‑free promotion.
        """
        super().__init__(name)

    def apply_promotion(self, product, quantity: int) -> float:
        """
        Calculates total cost where each third unit is free.
        """
        free_count = quantity // 3
        chargeable = quantity - free_count
        return chargeable * product.price


# Legacy class names for existing tests/setup

class PercentageDiscountPromotion(PercentDiscount):
    """
    Legacy alias for PercentDiscount to support older test names.
    Inherits apply_promotion behavior exactly.
    """

    def __init__(self, name: str, discount_percentage: float):
        super().__init__(name, discount_percentage)


class SecondItemHalfPricePromotion(SecondHalfPrice):
    """
    Legacy alias for SecondHalfPrice to support older test names.
    Inherits the same full‑plus‑half pricing logic.
    """

    def __init__(self, name: str):
        super().__init__(name)


class Buy2Get1FreePromotion(ThirdOneFree):
    """
    Legacy alias for ThirdOneFree to support older test names.
    Inherits the same buy‑2‑get‑1‑free logic.
    """

    def __init__(self, name: str):
        super().__init__(name)
