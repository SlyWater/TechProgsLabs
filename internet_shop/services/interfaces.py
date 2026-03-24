from abc import ABC, abstractmethod
from typing import Optional
from internet_shop.models import Product
from uuid import UUID


class IProductService(ABC):

    @abstractmethod
    def add(self, product: Product) -> Product:
        """
        Добавляет новый продукт.
        Возвращает созданную сущность.
        Исключения обрабатываются в вызывающем коде.
        """
        pass

    @abstractmethod
    def remove(self, product_id: UUID) -> Product:
        """
        Удаляет продукт по ID.
        Возвращает удаленную сущность.
        Исключения обрабатываются в вызывающем коде.
        """
        pass

    @abstractmethod
    def edit(self, product: Product) -> Product:
        """
        Обновляет продукт.
        Возвращает измененную сущность.
        Исключения обрабатываются в вызывающем коде.
        """
        pass

    @abstractmethod
    def search(self, product_id: UUID) -> Optional[Product]:
        """
        Поиск продукта по параметрам.
        Возвращает найденную сущность или None.
        Исключения обрабатываются в вызывающем коде.
        """
        pass
