from abc import ABC, abstractmethod


# Step 1: Create the abstract Promotion class
class Promotion(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity: int) -> float:
        pass


# Step 2: Create the specific promotion classes

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
        total_items = quantity + (quantity // 2)  # Buy 2, get 1 free
        total_price = total_items * product.price
        return total_price


# Step 3: Update the Product class

class Product:
    def __init__(self, name: str, price: float, quantity: int):
        if not name or price < 0 or quantity < 0:
            raise ValueError("Invalid product details: name cannot be empty, price and quantity must be non-negative.")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = quantity > 0
        self.promotion = None  # Add promotion instance variable

    def get_quantity(self) -> int:
        return self.quantity

    def set_quantity(self, quantity: int):
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        return self.active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    # Getter and setter for promotion
    def get_promotion(self):
        return self.promotion

    def set_promotion(self, promotion: Promotion):
        self.promotion = promotion

    def show(self) -> str:
        promotion_info = f"Promotion: {self.promotion.name}" if self.promotion else "No promotion"
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, {promotion_info}"

    def buy(self, quantity: int) -> float:
        if self.promotion:
            # Apply promotion if exists
            return self.promotion.apply_promotion(self, quantity)
        else:
            # No promotion, normal price
            if quantity <= 0:
                raise ValueError("Quantity must be greater than zero.")
            if quantity > self.quantity:
                raise ValueError("Not enough stock available.")
            total_price = quantity * self.price
            self.set_quantity(self.quantity - quantity)
            return total_price


class NonStockedProduct(Product):
    def __init__(self, name: str, price: float):
        # Non-stocked products always have quantity 0
        super().__init__(name, price, quantity=0)

    def show(self) -> str:
        """
        Override the show method to reflect that this product is non-stocked.
        """
        return f"{self.name}, Price: {self.price}, Non-stocked (Quantity: {self.quantity})"


class LimitedProduct(Product):
    def __init__(self, name: str, price: float, quantity: int, max_order_quantity: int):
        super().__init__(name, price, quantity)
        self.max_order_quantity = max_order_quantity

    def buy(self, quantity: int) -> float:
        """
        Override the buy method to limit the quantity that can be purchased.
        If quantity exceeds max_order_quantity, an exception will be raised.
        """
        if quantity > self.max_order_quantity:
            raise ValueError(f"You can only purchase up to {self.max_order_quantity} of this item.")
        return super().buy(quantity)

    def show(self) -> str:
        """
        Override the show method to indicate that this product has a purchase limit.
        """
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, Max order quantity: {self.max_order_quantity}"
