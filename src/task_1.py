class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = float(price)
        self.quantity = int(quantity)

    def __repr__(self):
        return f"Product(name={self.name!r}, price={self.price}, qty={self.quantity})"


class Category:
    # Атрибуты класса
    category_count: int = 0
    product_count: int = 0
    total_categories: int = 0
    total_products: int = 0

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.products = list(products)

        # Обновляем общие счётчики
        Category.total_categories += 1
        Category.total_products += len(self.products)

        Category.category_count += 1
        Category.product_count += len(self.products)

    def __repr__(self):
        return f"Category(name={self.name!r}, products={len(self.products)})"

    def add_product(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавлять только объекты Product")
        self.products.append(product)
        Category.total_products += 1
        Category.product_count += 1
