from abc import ABC, abstractmethod


class Promotion(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity: int) -> float:
        pass


class PercentageDiscountPromotion(Promotion):
    def __init__(self, name: str, discount_percentage: float):
        super().__init__(name)
        self.discount_percentage = discount_percentage

    def apply_promotion(self, product, quantity: int) -> float:
        total_price = product.price * quantity
        discount = total_price * (self.discount_percentage / 100)
        return total_price - discount


class SecondItemHalfPricePromotion(Promotion):
    def __init__(self, name: str):
        super().__init__(name)

    def apply_promotion(self, product, quantity: int) -> float:
        full_price_items = quantity // 2
        half_price_items = quantity - full_price_items
        total_price = (full_price_items * product.price) + (half_price_items * product.price / 2)
        return total_price


class Buy2Get1FreePromotion(Promotion):
    def __init__(self, name: str):
        super().__init__(name)

    def apply_promotion(self, product, quantity: int) -> float:
        chargeable_quantity = quantity - (quantity // 3)  # Every 3rd item is free
        total_price = chargeable_quantity * product.price
        return total_price