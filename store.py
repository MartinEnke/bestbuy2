from products import Product


class Store:
    """A class representing a store that manages multiple products."""

    def __init__(self, products=None):
        """
        Initializes the store with a list of products.
        If no list is provided, an empty list is used instead.
        """
        if products is None:
            self.products = []
        else:
            self.products = products

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
        Processes an order by buying specified quantities of products.
        """
        total_price = 0

        for item in shopping_list:
            product, quantity = item
            if product in self.products and product.is_active():
                total_price += product.buy(quantity)

        return total_price
