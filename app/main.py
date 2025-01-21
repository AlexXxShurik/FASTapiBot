from fastapi import FastAPI

from app.api.v1 import products
from app.db.crud import get_trackable_product
from app.db.models import create_database
from app.db.session import AsyncSessionLocal

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await create_database()
    async with AsyncSessionLocal() as db:
        await get_trackable_product(db)


app.include_router(products.router, prefix="/api/v1/products", tags=["products"])
