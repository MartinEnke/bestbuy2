from products import Product, NonStockedProduct, LimitedProduct
from store import Store

def start(store):
    """
    Starts the user interface for interacting with the store.
    """
    while True:
        print("\nWelcome to the Store!")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            # List all products
            products = store.get_all_products()
            if not products:
                print("No active products available.")
            else:
                for product in products:
                    print(product.show())

        elif choice == "2":
            # Show total quantity in store
            total_quantity = store.get_total_quantity()
            print(f"Total quantity in store: {total_quantity}")

        elif choice == "3":
            # Make an order
            products = store.get_all_products()
            shopping_list = []
            print("Enter the product and quantity you'd like to order:")
            while True:
                product_name = input("Enter product name (or 'done' to finish): ").strip()
                if product_name.lower() == "done":
                    break
                quantity = input(f"Enter quantity for {product_name}: ").strip()
                if not quantity.isdigit() or int(quantity) <= 0:
                    print("Please enter a valid quantity.")
                    continue

                product = next((p for p in products if p.name.lower() == product_name.lower()), None)
                if not product:
                    print("Product not found. Try again.")
                else:
                    quantity = int(quantity)
                    if isinstance(product, LimitedProduct) and quantity > product.max_order_quantity:
                        print(f"Sorry, you can only order up to {product.max_order_quantity} of {product.name}.")
                        continue
                    elif quantity > product.get_quantity():
                        print(f"Sorry, you cannot order more than {product.get_quantity()} of {product.name}.")
                        continue
                    shopping_list.append((product, quantity))

            if shopping_list:
                total_price = store.order(shopping_list)
                print(f"Total order cost: {total_price} dollars.")
            else:
                print("No products were selected.")

        elif choice == "4":
            # Quit the program
            print("Thank you for visiting the store!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


def main():
    # Setup initial stock of inventory
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Microsoft Windows License", price=150),
        LimitedProduct("Shipping Fee", price=10, quantity=100, max_order_quantity=1)
    ]
    best_buy = Store(product_list)

    # Start the user interface
    start(best_buy)


if __name__ == "__main__":
    main()
