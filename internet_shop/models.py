# •	Id – уникальный идентификатор (рассмотрите Guid)
# •	Definition – Текстовое описание товара
# •	Name – Название товара
# •	Price – стоимость товара
# •	Image – изображение товара

import uuid
from sqlalchemy import Column, String, Float
from internet_shop.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String(255), nullable=False)
    definition = Column(String(1000), nullable=False)
    price = Column(Float, nullable=False)
    image = Column(String(500), nullable=True)
