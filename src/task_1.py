class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = float(price)
        self.quantity = int(quantity)

    def __repr__(self):
        return f"Product(name={self.name!r}, price={self.__price}, qty={self.quantity})"

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if new_price > 0:
            self.__price = new_price
        else:
            print("Цена не должна быть нулевая или отрицательная")

    @classmethod
    def new_product(cls, data: dict):
        return cls(
            name=data["name"],
            description=data["description"],
            price=data["price"],
            quantity=data["quantity"]
        )


class Category:
    category_count: int = 0
    product_count: int = 0
    total_categories: int = 0
    total_products: int = 0

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.__products = list(products)

        Category.total_categories += 1
        Category.total_products += len(self.__products)
        Category.category_count += 1
        Category.product_count += len(self.__products)

    def __repr__(self):
        return f"Category(name={self.name!r}, products={len(self.__products)})"

    def add_product(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавлять только объекты Product")
        self.__products.append(product)
        Category.total_products += 1
        Category.product_count += 1

    @property
    def products(self):
        return "".join(
            f"{p.name}, {p.price} руб. Остаток: {p.quantity} шт.\n"
            for p in self.__products
        )
