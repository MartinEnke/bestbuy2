"""
Unit tests for the Products class in products.py.
"""

import pytest
from products import Product


def test_create_product():
    """Test that a product can be created successfully."""
    product = Product("Laptop", 1000.0, 5)
    assert product.name == "Laptop"
    assert product.price == 1000.0
    assert product.quantity == 5
    assert product.is_active() is True


def test_create_invalid_product():
    """Test that creating a product with invalid details raises an error."""
    with pytest.raises(ValueError):
        Product("", 1000.0, 5)

    with pytest.raises(ValueError):
        Product("Laptop", -100.0, 5)

    with pytest.raises(ValueError):
        Product("Laptop", 1000.0, -5)


def test_set_quantity():
    """Test setting the quantity of a product and auto-deactivation."""
    product = Product("Phone", 800.0, 10)

    product.set_quantity(5)
    assert product.get_quantity() == 5

    product.set_quantity(0)
    assert product.get_quantity() == 0
    assert product.is_active() is False


def test_buy():
    """Test buying products with valid and invalid quantities."""
    product = Product("Tablet", 500.0, 10)

    assert product.buy(2) == 1000.0
    assert product.get_quantity() == 8

    with pytest.raises(ValueError):
        product.buy(0)

    with pytest.raises(ValueError):
        product.buy(20)


# Test 1: When a product reaches 0 quantity, it becomes inactive
def test_product_becomes_inactive_when_quantity_reaches_zero():
    # Create a product with initial quantity of 1
    product = Product("Test Product", price=100, quantity=1)

    # Buy the product with quantity 1
    product.buy(1)

    # Assert that the product's quantity is 0 and it is inactive
    assert product.get_quantity() == 0
    assert not product.is_active()  # Product should be inactive when quantity is 0


# Test 2: Product purchase modifies the quantity and returns the correct output
def test_product_purchase_modifies_quantity():
    # Create a product with an initial quantity of 10
    product = Product("Test Product", price=100, quantity=10)

    # Buy 3 units of the product
    total_price = product.buy(3)

    # Assert that the quantity is updated to 7 (10 - 3)
    assert product.get_quantity() == 7

    # Assert that the total price for the purchase is correct (3 * 100 = 300)
    assert total_price == 300


# Test 3: Buying a larger quantity than exists invokes an exception
def test_buying_more_than_available_raises_exception():
    # Create a product with an initial quantity of 5
    product = Product("Test Product", price=100, quantity=5)

    # Attempt to buy 6 units, which is more than the available quantity
    with pytest.raises(ValueError, match="Not enough stock available."):
        product.buy(6)

