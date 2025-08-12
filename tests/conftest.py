import pytest
from src.task_1 import Product, Category

@pytest.fixture(autouse=True)
def reset_category_counters():
    """
    Сбрасываем счётчики класса Category перед каждым тестом,
    чтобы тесты были независимыми.
    """
    Category.total_categories = 0
    Category.total_products = 0
    yield
    # (опционально) повторный сброс после теста
    Category.total_categories = 0
    Category.total_products = 0


@pytest.fixture
def sample_products():
    p1 = Product("Apple", "Red apple", 0.5, 10)
    p2 = Product("Banana", "Yellow banana", 0.8, 5)
    p3 = Product("Orange", "Citrus", 1.2, 7)
    return p1, p2, p3


@pytest.fixture
def sample_categories(sample_products):
    p1, p2, p3 = sample_products
    cat1 = Category("Fruits", "Fresh fruits", [p1, p2])
    cat2 = Category("Citrus", "Citrus-only", [p3])
    return cat1, cat2