from src.task_1 import Category, Product


def test_product_init():
    p = Product("Milk", "1L milk", 1.49, 3)
    assert p.name == "Milk"
    assert p.description == "1L milk"
    assert isinstance(p.price, float)
    assert p.price == 1.49
    assert isinstance(p.quantity, int)
    assert p.quantity == 3


def test_category_init(sample_products):
    p1, p2, _ = sample_products
    cat = Category("Fruits", "Fresh fruits", [p1, p2])

    assert cat.name == "Fruits"
    assert cat.description == "Fresh fruits"
    assert isinstance(cat.products, list)
    assert len(cat.products) == 2
    assert all(isinstance(x, Product) for x in cat.products)


def test_total_counts_after_init(sample_categories):
    assert Category.total_categories == 2
    assert Category.total_products == 3


def test_add_product_updates_totals(sample_categories):
    cat1, _ = sample_categories
    before = Category.total_products

    new_p = Product("Pear", "Green pear", 0.9, 4)
    cat1.add_product(new_p)

    assert len(cat1.products) == 3
    assert Category.total_products == before + 1
