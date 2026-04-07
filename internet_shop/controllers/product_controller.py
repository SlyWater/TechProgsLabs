from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from internet_shop.dependencies import get_product_service
from internet_shop.models import Product
from internet_shop.schemas import ProductCreate, ProductResponse, ProductUpdate
from internet_shop.services.interfaces import IProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse)
def add_product(
        product: ProductCreate,
        service: IProductService = Depends(get_product_service),
):
    db_product = Product(**product.model_dump())
    return service.add(db_product)


@router.delete("/{product_id}")
def remove_product(
        product_id: UUID,
        service: IProductService = Depends(get_product_service),
):
    try:
        return service.remove(product_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/", response_model=ProductResponse)
def edit_product(
        product: ProductUpdate,
        service: IProductService = Depends(get_product_service),
):
    try:
        db_product = Product(**product.model_dump())
        return service.edit(db_product)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{product_id}", response_model=ProductResponse)
def search_product(
        product_id: UUID,
        service: IProductService = Depends(get_product_service),
):
    product = service.search(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product
