from products import Product
from store import Store

def main():
    # Create product instances
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    # Buying products
    print(bose.buy(50))  # Will return the total price for 50 Bose earbuds
    print(mac.buy(100))  # Will return the total price for 100 MacBook Air M2
    print(mac.is_active())  # Check if the product is active

    # Showing product details
    print(bose.show())  # Will show details of the Bose earbuds
    print(mac.show())  # Will show details of the MacBook Air

    # Changing the quantity of the Bose product
    bose.set_quantity(1000)
    print(bose.show())  # Updated quantity and details of Bose earbuds

    # List of products to add to the store
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
    ]

    # Create store instance with products
    best_buy = Store(product_list)

    # Get all active products
    products = best_buy.get_all_products()

    # Print total quantity of all products in store
    print("Total quantity in store:", best_buy.get_total_quantity())

    # Place an order and calculate total price
    order_price = best_buy.order([(products[0], 1), (products[1], 2)])  # Order 1 MacBook Air and 2 Bose earbuds
    print(f"Total order cost: {order_price} dollars.")  # Display total price of the order

if __name__ == "__main__":
    main()