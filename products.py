from promotions import Promotion


class Product:
    def __init__(self, name: str, price: float, quantity: int):
        if not name or price < 0 or quantity < 0:
            raise ValueError("Invalid product details: name cannot be empty, price and quantity must be non-negative.")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = quantity > 0
        self.promotion = None  # Promotion instance (if any)

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

    # Promotion-related methods
    def get_promotion(self):
        return self.promotion

    def set_promotion(self, promotion: Promotion):
        self.promotion = promotion

    def show(self) -> str:
        promotion_info = f"Promotion: {self.promotion.name}" if self.promotion else "No promotion"
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, {promotion_info}"

    def buy(self, quantity: int) -> float:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if quantity > self.quantity:
            raise ValueError("Not enough stock available.")

        total_price = (
            self.promotion.apply_promotion(self, quantity)
            if self.promotion else quantity * self.price
        )

        self.set_quantity(self.quantity - quantity)
        return total_price


class NonStockedProduct(Product):
    def __init__(self, name: str, price: float):
        # Non-stocked products always have quantity 0
        super().__init__(name, price, quantity=0)

    def show(self) -> str:
        return f"{self.name}, Price: {self.price}, Non-stocked (Quantity: {self.quantity})"


class LimitedProduct(Product):
    def __init__(self, name: str, price: float, quantity: int, max_order_quantity: int):
        super().__init__(name, price, quantity)
        self.max_order_quantity = max_order_quantity

    def buy(self, quantity: int) -> float:
        if quantity > self.max_order_quantity:
            raise ValueError(f"You can only purchase up to {self.max_order_quantity} of this item.")
        return super().buy(quantity)

    def show(self) -> str:
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, Max order quantity: {self.max_order_quantity}"
