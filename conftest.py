import pytest
from pytest_factoryboy import register
from tests.factories import CategoryFactory, ProductFactory, VariationFactory

register(CategoryFactory) # connect to that by category_factory
register(ProductFactory)  # connect to that by product_factory
register(VariationFactory)


@pytest.fixture
def category(db, category_factory):
    category = category_factory.create()
    return category

@pytest.fixture
def product(db, product_factory):
    product = product_factory.create()
    return product

@pytest.fixture
def variation(db, variation_factory):
    product = variation_factory.create()
    return product