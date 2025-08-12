class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = float(price)
        self.quantity = int(quantity)

    def __repr__(self):
        # чтобы print(category2.products) показывал что-то читаемое
        return f"Product(name={self.name!r}, price={self.price}, qty={self.quantity})"


class Category:
    # атрибуты класса (общие для всех объектов)
    category_count: int = 0
    product_count: int = 0  # считаем количество элементов в списках products

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.products = list(products)  # фиксируем состав на момент создания

        # автоматически обновляем общие счётчики
        Category.category_count += 1
        Category.product_count += len(self.products)

    def __repr__(self):
        return f"Category(name={self.name!r}, products={len(self.products)})"

    # на будущее: если будешь добавлять товары после создания — поддерживай счётчик
    def add_product(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавлять только объекты Product")
        self.products.append(product)
        Category.product_count += 1
