from fastapi import FastAPI

from internet_shop.controllers.product_controller import router as product_router
from internet_shop.database import engine
from internet_shop.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Internet Shop API")

app.include_router(product_router)
