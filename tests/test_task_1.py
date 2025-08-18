import pytest

from src.task_1 import Category, LawnGrass, Product, Smartphone


# ---------- Product: базовые проверки и price ----------
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
    assert p.price == pytest.approx(10.0)

    p.price = -5
    out2 = capsys.readouterr().out
    assert "Цена не должна быть нулевая или отрицательная" in out2
    assert p.price == pytest.approx(10.0)


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


# ---------- Category: счётчики и add_product ----------
def test_category_counters_after_init(sample_products):
    # до создания
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

    # __repr__
    assert "Category(name='Fruits'" in repr(cat1)
    assert "Category(name='Citrus'" in repr(cat2)


def test_add_product_updates_counters_and_getter_format(sample_products):
    p1, p2, p3 = sample_products
    cat = Category("Fruits", "Fresh fruits", [p1, p2])

    before_total = Category.total_products
    before_prod_count = Category.product_count

    new_p = Product("Pear", "Green pear", 0.9, 4)
    cat.add_product(new_p)

    assert Category.total_products == before_total + 1
    assert Category.product_count == before_prod_count + 1

    # Геттер products возвращает строку, основанную на __str__ продукта
    out = cat.products
    assert isinstance(out, str)
    assert f"{new_p.name}, {new_p.price} руб. Остаток: {new_p.quantity} шт.\n" in out


def test_products_is_private_list_but_accessible_via_mangling(sample_products):
    """Атрибут products — это геттер (строка), а реальный список скрыт в __products."""
    p1, p2, _ = sample_products
    cat = Category("Fruits", "Fresh fruits", [p1, p2])

    # публичный геттер возвращает строку
    assert isinstance(cat.products, str)
    # внутренний список по name-mangling
    internal_list = getattr(cat, "_Category__products")
    assert isinstance(internal_list, list)
    assert len(internal_list) == 2
    assert all(isinstance(x, Product) for x in internal_list)


# ---------- __str__ ----------
def test_product_str(sample_product_data):
    p = Product(**sample_product_data)
    expected = f"{p.name}, {p.price} руб. Остаток: {p.quantity} шт."
    assert str(p) == expected


def test_category_str(sample_products):
    p1, p2, p3 = sample_products
    cat = Category("Fruits", "Fresh fruits", [p1, p2])
    total_qty = p1.quantity + p2.quantity
    assert str(cat) == f"Fruits, количество продуктов: {total_qty} шт."

    cat.add_product(p3)
    total_qty_new = total_qty + p3.quantity
    assert str(cat) == f"Fruits, количество продуктов: {total_qty_new} шт."


# ---------- __add__ ограничения ----------
def test_add_same_class_products_ok():
    s1 = Smartphone("A", "d", 100.0, 2, 95.0, "M1", 128, "black")
    s2 = Smartphone("B", "d", 200.0, 1, 90.0, "M2", 256, "white")
    # 100*2 + 200*1 = 400
    assert s1 + s2 == 400.0

    g1 = LawnGrass("G1", "d", 10.0, 10, "RU", "7 дней", "зелёный")
    g2 = LawnGrass("G2", "d", 20.0, 3, "US", "5 дней", "тёмно-зелёный")
    # 10*10 + 20*3 = 160
    assert g1 + g2 == 160.0


def test_add_different_class_products_raises_typeerror():
    s = Smartphone("A", "d", 100.0, 2, 95.0, "M1", 128, "black")
    g = LawnGrass("G", "d", 10.0, 10, "RU", "7 дней", "зелёный")
    with pytest.raises(TypeError):
        _ = s + g


def test_add_with_non_product_returns_notimplemented():
    p = Product("X", "d", 10.0, 1)
    # прямой вызов __add__ возвращает NotImplemented
    assert p.__add__("not a product") is NotImplemented


# ---------- add_product ограничения ----------
def test_category_add_accepts_subclasses_and_rejects_others():
    s = Smartphone("A", "d", 100.0, 2, 95.0, "M1", 128, "black")
    g = LawnGrass("G", "d", 10.0, 10, "RU", "7 дней", "зелёный")
    cat = Category("Mixed", "desc", [])

    # Принимаем Product и наследников
    cat.add_product(s)
    cat.add_product(g)
    cat.add_product(Product("P", "d", 1.0, 1))

    # Но отвергаем произвольные объекты
    with pytest.raises(TypeError):
        cat.add_product("not a product")
