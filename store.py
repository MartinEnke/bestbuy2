from products import LimitedProduct


class Store:
    """A class representing a store that manages multiple products."""

    def __init__(self, products=None):
        """
        Initializes the store with a list of products.
        If no list is provided, an empty list is used instead.
        """
        if products is None:
            self.products = []
            self.promotion = None
        else:
            self.products = products

    def set_promotion(self, promotion):
        """
        Attaches a promotion strategy to the store.
        The promotion must implement an `apply(order_list, full_price)` method.
        """
        self.promotion = promotion

    def add_product(self, product):
        """
        Adds a new product to the store.
        """
        self.products.append(product)

    def remove_product(self, product):
        """
        Removes a product from the store if it exists.
        """
        if product in self.products:
            self.products.remove(product)

    def get_total_quantity(self):
        """
        Returns the total quantity of all products in the store.
        """
        total_quantity = 0
        for product in self.products:
            total_quantity += product.get_quantity()
        return total_quantity

    def get_all_products(self):
        """
        Returns a list of all active products in the store.
        """
        active_products = []
        for product in self.products:
            if product.is_active():
                active_products.append(product)
        return active_products

    def order(self, shopping_list):
        """
        Processes an order:
          - Enforces per‑product caps for LimitedProduct
          - Calls each product.buy(qty) exactly once
          - Totals up the prices
        """
        # 1) Build a map of total requested per product
        totals = {}
        for product, qty in shopping_list:
            totals.setdefault(product, 0)
            totals[product] += qty

        # 2) Enforce LimitedProduct maximums
        for product, total_qty in totals.items():
            if isinstance(product, LimitedProduct):
                if total_qty > product.maximum:
                    raise ValueError(
                        f"You requested {total_qty} of {product.name}, "
                        f"but the per-order maximum is {product.maximum}."
                    )

        # 3) Now actually buy once per line, summing price
        total_price = 0
        for product, qty in shopping_list:
            if product in self.products and product.is_active():
                total_price += product.buy(qty)

        return total_price
