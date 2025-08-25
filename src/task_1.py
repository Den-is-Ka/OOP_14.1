from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Iterable, List


class BaseProduct(ABC):

    @abstractmethod
    def total_cost(self) -> float:
        raise NotImplementedError


class InitPrintMixin:

    def _print_on_init(self) -> None:
        cls = self.__class__.__name__
        name = getattr(self, "name", None)
        description = getattr(self, "description", None)
        price = getattr(self, "price", None)
        quantity = getattr(self, "quantity", None)
        print(f"{cls}({name!r}, {description!r}, {price!r}, {quantity!r})")


class Product(BaseProduct, InitPrintMixin):

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        # 🔹 условие по ТЗ
        if int(quantity) == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

        self.name = name
        self.description = description
        self._price = float(price)
        self.quantity = int(quantity)

        self._print_on_init()

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price is None or float(new_price) <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        self._price = float(new_price)

    @classmethod
    def new_product(cls, data: dict[str, Any]) -> Product:
        return cls(
            name=str(data["name"]),
            description=str(data["description"]),
            price=float(data["price"]),
            quantity=int(data["quantity"]),
        )

    def total_cost(self) -> float:
        return self.price * self.quantity

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: Any) -> Any:
        if not isinstance(other, Product):
            return NotImplemented
        if self.__class__ is not other.__class__:
            raise TypeError("Нельзя складывать товары разных типов")
        return self.total_cost() + other.total_cost()


class Smartphone(Product):
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
    ) -> None:
        self.efficiency = float(efficiency)
        self.model = str(model)
        self.memory = int(memory)
        self.color = str(color)
        super().__init__(name, description, price, quantity)


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        self.country = str(country)
        self.germination_period = str(germination_period)
        self.color = str(color)
        super().__init__(name, description, price, quantity)


class Category:
    total_categories: int = 0
    total_products: int = 0

    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: Iterable[Product]) -> None:
        self.name = name
        self.description = description
        self.__products: List[Product] = []
        for p in products:
            self._add_product_internal(p)

        Category.total_categories += 1
        Category.category_count = Category.total_categories

    def _add_product_internal(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только Product и наследников")
        self.__products.append(product)
        Category.total_products += 1
        Category.product_count = Category.total_products

    def add_product(self, product: Any) -> None:
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только Product и наследников")
        self._add_product_internal(product)

    @property
    def products(self) -> str:
        return "".join(
            f"{p.name}, {p.price} руб. Остаток: {p.quantity} шт.\n" for p in self.__products
        )

    def __str__(self) -> str:
        total_qty = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов: {total_qty} шт."

    def __repr__(self) -> str:
        return f"Category(name={self.name!r}, description={self.description!r}, products={len(self.__products)!r})"

    def middle_price(self) -> float:
        try:
            count = len(self.__products)
            prices_sum = sum(p.price for p in self.__products)
            return round(prices_sum / count, 2)
        except ZeroDivisionError:
            return 0.0
