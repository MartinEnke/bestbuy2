import pytest
from promotions import (
    PercentageDiscountPromotion,
    SecondItemHalfPricePromotion,
    Buy2Get1FreePromotion
)
from products import Product


@pytest.fixture
def product():
    return Product("Test Product", price=100, quantity=100)


def test_percentage_discount_promotion(product):
    promo = PercentageDiscountPromotion("10% Off", 10)
    discounted_price = promo.apply_promotion(product, 2)
    assert discounted_price == 180.0  # 200 - 10% = 180


def test_second_item_half_price_promotion(product):
    promo = SecondItemHalfPricePromotion("2nd Half Price")
    total = promo.apply_promotion(product, 3)
    # 1 full + 2 half = 1*100 + 2*50 = 200
    assert total == 200.0


def test_buy2_get1_free_promotion(product):
    promo = Buy2Get1FreePromotion("Buy 2 Get 1")
    total = promo.apply_promotion(product, 3)
    # Only 2 paid, 1 free: 2 * 100 = 200
    assert total == 200.0

    total = promo.apply_promotion(product, 6)
    # 4 paid, 2 free
    assert total == 400.0
