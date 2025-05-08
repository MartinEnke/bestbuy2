"""
Unit tests for the Promotion class in promotions.py.
"""

import pytest
from promotions import (
    PercentDiscount,
    SecondHalfPrice,
    ThirdOneFree,
    PercentageDiscountPromotion,
    SecondItemHalfPricePromotion,
    Buy2Get1FreePromotion
)
from products import Product


@pytest.fixture
def product():
    return Product("Test Product", price=100, quantity=100)


def test_percent_discount(product):
    promo = PercentDiscount("30% off", percent=30)
    # 100 * 3 = 300 minus 30% = 210
    assert promo.apply_promotion(product, 3) == 210.0


def test_second_half_price(product):
    promo = SecondHalfPrice("Second Half price")
    # 3 items: 1 full + 2 half = 1*100 + 2*50 = 200
    assert promo.apply_promotion(product, 3) == 200.0


def test_third_one_free(product):
    promo = ThirdOneFree("Third One Free")
    # 3 items: pay for 2, 1 free = 2*100 = 200
    assert promo.apply_promotion(product, 3) == 200.0
    # 6 items: pay for 4 = 400
    assert promo.apply_promotion(product, 6) == 400.0


# Tests for the aliased (legacy) names

def test_legacy_percent_discount(product):
    promo = PercentageDiscountPromotion("10% off legacy", discount_percentage=10)
    assert promo.apply_promotion(product, 2) == 180.0  # 200 − 10%


def test_legacy_second_item_half_price(product):
    promo = SecondItemHalfPricePromotion("2nd Half Price Legacy")
    assert promo.apply_promotion(product, 3) == 200.0


def test_legacy_buy2_get1_free(product):
    promo = Buy2Get1FreePromotion("Buy 2 Get 1 Legacy")
    assert promo.apply_promotion(product, 3) == 200.0
    assert promo.apply_promotion(product, 6) == 400.0
