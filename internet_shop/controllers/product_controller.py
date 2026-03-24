from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from internet_shop.database import SessionLocal
from internet_shop.schemas import ProductCreate, ProductResponse
from internet_shop.models import Product
from internet_shop.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ProductResponse)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    service = ProductService(db)

    db_product = Product(**product.model_dump())
    return service.add(db_product)


@router.delete("/{product_id}")
def remove_product(product_id: UUID, db: Session = Depends(get_db)):
    try:
        service = ProductService(db)
        return service.remove(product_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/", response_model=ProductResponse)
def edit_product(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        service = ProductService(db)
        db_product = Product(**product.model_dump())
        return service.edit(db_product)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{product_id}", response_model=ProductResponse)
def search_product(product_id: UUID, db: Session = Depends(get_db)):
    service = ProductService(db)
    product = service.search(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product
