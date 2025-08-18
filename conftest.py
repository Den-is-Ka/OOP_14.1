import pytest
from src.task_1 import Category, Product


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Сбрасываем счётчики класса Category перед каждым тестом."""
    Category.total_categories = 0
    Category.total_products = 0
    Category.category_count = 0
    Category.product_count = 0
    yield
    Category.total_categories = 0
    Category.total_products = 0
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def sample_product_data():
    return {
        "name": "Apple",
        "description": "Red apple",
        "price": 0.5,
        "quantity": 10,
    }


@pytest.fixture
def sample_products():
    p1 = Product("Apple", "Red apple", 0.5, 10)
    p2 = Product("Banana", "Yellow banana", 0.8, 5)
    p3 = Product("Orange", "Citrus", 1.2, 7)
    return p1, p2, p3
