from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.crud import create_product, start_periodic_update
from app.services.wildberries import fetch_product_data
from app.schemas.product import ProductCreate, ProductResponse

router = APIRouter()


@router.post("/", response_model=ProductResponse)
async def create_product_view(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    product_data = await fetch_product_data(product.artikul)
    if not product_data:
        raise HTTPException(status_code=404, detail="Product not found")

    db_product = await create_product(
        db, product.artikul
    )
    return db_product

@router.get("/subscribe/{artikul}")
async def subscribe(artikul: str, db: AsyncSession = Depends(get_db)):
    await start_periodic_update(artikul, db)
    return {"message": f"Подписка на {artikul} активирована, данные будут обновляться каждые 30 минут."}