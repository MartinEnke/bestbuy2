from promotions import Promotion


class Product:
    """
    Represents a generic product in the store with stock management and optional promotion.
    """
    def __init__(self, name: str, price: float, quantity: int):
        """
        Initializes a new Product.
        """
        if not name or price < 0 or quantity < 0:
            raise ValueError(
                "Invalid product details: name cannot be empty, price and quantity must be non-negative."
            )

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = quantity > 0
        self.promotion = None  # Promotion instance (if any)

    def get_quantity(self) -> int:
        """Returns the current stock quantity."""
        return self.quantity

    def set_quantity(self, quantity: int):
        """
        Updates the stock quantity and deactivate if it reaches zero.
        """
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        """Returns True if the product is active (in stock)."""
        return self.active

    def activate(self):
        """Marks the product as active (in stock)."""
        self.active = True

    def deactivate(self):
        """Marks the product as inactive (out of stock)."""
        self.active = False

    # Promotion-related methods
    def get_promotion(self):
        """Returns the current promotion applied, or None if none."""
        return self.promotion

    def set_promotion(self, promotion: Promotion):
        """
        Attaches a Promotion to this product.
        """
        self.promotion = promotion

    def show(self) -> str:
        """
        Returns a string representation of the product, including promotion info.
        """
        promotion_info = (
            f"Promotion: {self.promotion.name}" if self.promotion else "No promotion"
        )
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, {promotion_info}"

    def buy(self, quantity: int) -> float:
        """
        Purchases a specified quantity of the product, applying promotion if available.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if quantity > self.quantity:
            raise ValueError("Not enough stock available.")

        # Calculate price using promotion if available, otherwise standard price * qty
        if self.promotion is not None:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = self.price * quantity


            # Deduct stock
        self.set_quantity(self.quantity - quantity)
        return total_price


class NonStockedProduct(Product):
    """
    Represents a product without inventory tracking (infinite availability).
    """
    def __init__(self, name: str, price: float):
        super().__init__(name, price, quantity=0)

    def get_quantity(self) -> int:
        """
        Overrides stock check—always “infinite” (we’ll treat as 0 but never out-of-stock).
        """
        return float('inf')

    def is_active(self) -> bool:
        return True

    def show(self) -> str:
        return f"{self.name}, Price: {self.price}, Non-stocked"

    def buy(self, quantity: int) -> float:
        """
        Always available—just calculate price (with promotion if any) without changing stock.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        return self.price * quantity


class LimitedProduct(Product):
    """
    Represents a product with a maximum allowable purchase limit per order.
    """
    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        """
        Initializes a limited product with a purchase cap.
        """
        super().__init__(name, price, quantity)
        if maximum <= 0:
            raise ValueError("Maximum must be greater than zero.")
        self.maximum = maximum

    def buy(self, quantity: int) -> float:
        """
        Purchases a specified quantity, enforcing the purchase cap.
        """
        if quantity > self.maximum:
            raise ValueError(
                f"You can only purchase up to {self.maximum} of this item."
            )
        return super().buy(quantity)

    def show(self) -> str:
        """
        Returns a string representation including the maximum purchase limit.
        """
        return (
            f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, "
            f"Max order quantity: {self.maximum}"
        )