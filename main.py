from products import Product, NonStockedProduct, LimitedProduct
from store import Store
import promotions

def start(store):
    """
    Starts the interactive CLI for the provided store.

    Prints a menu of actions:
      1. List all active products
      2. Show total quantity of products
      3. Make an order by selecting products and quantities
      4. Quit the application

    Prompts the user for input and performs the corresponding action until the user chooses to quit.
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
            # List all active products
            products = store.get_all_products()
            if not products:
                print("No active products available.")
            else:
                for product in products:
                    print(product.show())

        elif choice == "2":
            # Show total quantity of all products
            total_quantity = store.get_total_quantity()
            print(f"Total quantity in store: {total_quantity}")


        elif choice == "3":
            """
            Allows the user to create an order by selecting products by index
            and specifying quantities. Validates inputs and ensures stock
            limits are respected. Calculates and prints the total order cost.
            """
            products = store.get_all_products()
            print("\nAvailable Products:")
            index = 1
            for product in products:
                print(f"{index}. {product.name} "
                      f"(Quantity: {product.get_quantity()})")
                index += 1
            shopping_list = []
            print("When you want to finish order, enter empty text")

            while True:
                selection = input(
                    "Which product # do you want? "
                ).strip()
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
                # Loop until a valid quantity is entered
                while True:
                    quantity_str = input(
                        f"What amount do you want? "
                    ).strip()
                    if quantity_str == "":
                        break

                    if not quantity_str.isdigit() or int(quantity_str) <= 0:
                        print("Please enter a valid quantity.")
                        continue
                    quantity = int(quantity_str)

                    current_total = sum(q for p, q in shopping_list if p is product)
                    if isinstance(product, LimitedProduct) and current_total + quantity > product.maximum:
                        print(f"Sorry, you can only purchase up to {product.maximum} of '{product.name}' per order.")
                        continue

                    try:
                        if quantity > product.get_quantity():
                            raise ValueError(
                                f"Sorry, you cannot order more than "
                                f"{product.get_quantity()} units."
                            )
                        shopping_list.append((product, quantity))
                        print("Product added to list!\n")
                        break
                    except ValueError as ve:
                        print(ve)

            if shopping_list:
                try:
                    total_price = store.order(shopping_list)
                    print(f"Total order cost: {total_price} dollars.")
                except ValueError as ve:
                    print(f"Order error: {ve}")
            else:
                print("No products were selected.")


        elif choice == "4":
            # Quit the program
            print("Thank you for visiting the store!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


def main():
    """
    Initializes the store with a set of products and launches the CLI.
    """
    # Setup initial stock of inventory
    # setup initial stock of inventory
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    ]
    best_buy = Store(product_list)

    # Create promotion catalog
    second_half_price = promotions.SecondHalfPrice("Second Half price!")
    third_one_free = promotions.ThirdOneFree("Third One Free!")
    thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

    # Add promotions to products
    product_list[0].set_promotion(second_half_price)  # MacBook
    product_list[1].set_promotion(third_one_free)  # Earbuds
    product_list[3].set_promotion(thirty_percent)  # Windows License

    start(best_buy)


if __name__ == "__main__":
    main()