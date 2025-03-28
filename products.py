
class Product:
    def __init__(self, name: str, price: float, quantity: int):
        """
        Initializes a new product with the specified name, price, and quantity.
        """
        if not name or price < 0 or quantity < 0:
            raise ValueError(
                "Invalid product details: name cannot be empty, price and quantity must be non-negative.")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True


    def get_quantity(self) -> int:
        """
        Returns the current quantity of the product in stock.
        """
        return self.quantity

    def set_quantity(self, quantity: int):
        """
        Sets the quantity of the product in stock and deactivates the product if the quantity reaches 0.
        """
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        """
        Checks whether the product is active.
        """
        return self.active

    def activate(self):
        """
        Activates the product, making it available for purchase.
        """
        self.active = True

    def deactivate(self):
        """
        Deactivates the product, making it unavailable for purchase.
        """
        self.active = False

    def show(self) -> str:
        """
        Returns a string representation of the product, including its name, price, and quantity.
        """
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def buy(self, quantity: int) -> float:
        """
        Processes the purchase of a specified quantity of the product and updates the stock.
        """
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
