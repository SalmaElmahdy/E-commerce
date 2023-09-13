import pytest

from store.models import Variation

def test_product_str(product):
    assert product.__str__() == 'shirt'
    
def test_product_variation(variation):
    assert variation.product is not None
    assert variation.variation_category in [choice[0] for choice in Variation.variation_category_choice]
    assert isinstance(variation.__str__(), str)
    assert variation.is_active is True