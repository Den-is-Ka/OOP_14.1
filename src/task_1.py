class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = float(price)
        self.quantity = int(quantity)

    def __repr__(self):
        return f"Product(name={self.name!r}, price={self.__price}, qty={self.quantity})"

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        # Разрешаем сложение только для одинаковых КЛАССОВ продуктов
        if not isinstance(other, Product):
            return NotImplemented
        if type(self) is not type(other):
            raise TypeError("Складывать можно только товары одного типа")
        return self.price * self.quantity + other.price * other.quantity

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


class Smartphone(Product):
    """Наследник Product с доп. полями:
    efficiency (float), model (str), memory (int), color (str).
    """
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = float(efficiency)
        self.model = model
        self.memory = int(memory)
        self.color = color


class LawnGrass(Product):
    """Наследник Product с доп. полями:
    country (str), germination_period (str), color (str).
    """
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    category_count: int = 0
    product_count: int = 0
    total_categories: int = 0
    total_products: int = 0

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        # Храним приватно
        self.__products = list(products)

        Category.total_categories += 1
        Category.total_products += len(self.__products)
        Category.category_count += 1
        Category.product_count += len(self.__products)

    def __repr__(self):
        return f"Category(name={self.name!r}, products={len(self.__products)})"

    def __str__(self):
        total_quantity = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product: Product):
        # Разрешаем добавлять только Product ИЛИ его наследников
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавлять только объекты Product или его наследников")
        self.__products.append(product)
        Category.total_products += 1
        Category.product_count += 1

    @property
    def products(self):
        # Возвращаем строку со всеми товарами
        return "".join(str(p) + "\n" for p in self.__products)
