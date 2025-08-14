import pytest

from src.task_1 import Category, Product


def test_product_init_and_price_getter(sample_product_data):
    p = Product(**sample_product_data)
    assert p.name == sample_product_data["name"]
    assert p.description == sample_product_data["description"]
    assert p.price == pytest.approx(sample_product_data["price"])
    assert isinstance(p.quantity, int)
    assert p.quantity == sample_product_data["quantity"]


def test_price_setter_accepts_positive():
    p = Product("N", "D", 10.0, 1)
    p.price = 99.9
    assert p.price == pytest.approx(99.9)


def test_price_setter_rejects_non_positive(capsys):
    p = Product("N", "D", 10.0, 1)

    p.price = 0
    out1 = capsys.readouterr().out
    assert "Цена не должна быть нулевая или отрицательная" in out1
    assert p.price == pytest.approx(10.0)  # не изменилось

    p.price = -5
    out2 = capsys.readouterr().out
    assert "Цена не должна быть нулевая или отрицательная" in out2
    assert p.price == pytest.approx(10.0)  # всё ещё не изменилось


def test_new_product_classmethod_creates_instance():
    data = {
        "name": "Milk",
        "description": "1L milk",
        "price": 1.49,
        "quantity": 3,
    }
    p = Product.new_product(data)
    assert isinstance(p, Product)
    assert p.name == "Milk"
    assert p.description == "1L milk"
    assert p.price == pytest.approx(1.49)
    assert p.quantity == 3


def test_category_counters_after_init(sample_products):
    assert Category.total_categories == 0
    assert Category.total_products == 0
    assert Category.category_count == 0
    assert Category.product_count == 0

    p1, p2, p3 = sample_products
    cat1 = Category("Fruits", "Fresh fruits", [p1, p2])
    cat2 = Category("Citrus", "Citrus-only", [p3])

    assert Category.total_categories == 2
    assert Category.category_count == 2
    assert Category.total_products == 3
    assert Category.product_count == 3

    assert "Category(name='Fruits'" in repr(cat1)


def test_add_product_updates_counters_and_getter_format(sample_products):
    p1, p2, p3 = sample_products
    cat = Category("Fruits", "Fresh fruits", [p1, p2])

    before_total = Category.total_products
    before_prod_count = Category.product_count

    new_p = Product("Pear", "Green pear", 0.9, 4)
    cat.add_product(new_p)

    assert Category.total_products == before_total + 1
    assert Category.product_count == before_prod_count + 1

    out = cat.products
    assert isinstance(out, str)
    assert f"{new_p.name}, {new_p.price} руб. Остаток: {new_p.quantity} шт.\n" in out


def test_products_is_private_list_but_accessible_via_mangling(sample_products):
    """Проверяем, атрибут products — что это геттер,
    реальный список спрятан в __products.
    """
    p1, p2, _ = sample_products
    cat = Category("Fruits", "Fresh fruits", [p1, p2])

    assert isinstance(cat.products, str)
    internal_list = getattr(cat, "_Category__products")
    assert isinstance(internal_list, list)
    assert len(internal_list) == 2
    assert all(isinstance(x, Product) for x in internal_list)
