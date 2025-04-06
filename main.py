from products import Product, NonStockedProduct, LimitedProduct
from store import Store

def start(store):
    """
    Starts the user interface for interacting with the store.
    """
    while True:
        print("\n   Store Menu")
        print("   ----------")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")
        choice = input("Please choose a number: ").strip()

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
            print("\nAvailable Products:")
            index = 1
            for product in products:
                print(f"{index}. {product.name} (Quantity: {product.get_quantity()})")
                index += 1

            shopping_list = []
            print("When you want to finish order, enter empty text")
            while True:
                selection = input("Which product # do you want? ").strip()
                if selection == "":
                    break
                if not selection.isdigit():
                    print("Invalid input. Please enter a number.")
                    continue

                selection = int(selection)
                if selection < 1 or selection > len(products):
                    print("Invalid product number. Try again.")
                    continue

                product = products[selection - 1]
                quantity = input(f"What amount do you want? ").strip()

                if not quantity.isdigit() or int(quantity) <= 0:
                    print("Please enter a valid quantity.")
                    continue

                quantity = int(quantity)
                if quantity > product.get_quantity():
                    print(f"Sorry, you cannot order more than {product.get_quantity()} units.")
                    continue
                print("Product added to list!\n")
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
