import aiohttp
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Product

scheduler = AsyncIOScheduler()

async def get_product(db: AsyncSession, artikul: str):
    """
    Получение данных о продукте по артикулу из базы данных.
    """

    # Обновляю данные при каждом запросе, если не нужно - закомментируйте
    await create_product(db, artikul)

    result = await db.execute(select(Product).where(Product.artikul == artikul))
    product = result.scalars().first()

    if not product:
        return None

    return product

async def get_trackable_product(db: AsyncSession):
    """
    Найти в базе отслеживаемые продукты и запустить сбор с периодичностью 30 мин
    """
    result = await db.execute(select(Product).where(Product.is_trackable == True))
    trackable_products = result.scalars().all()

    for product in trackable_products:
        await start_periodic_update(product.artikul, db)

async def create_product(db: AsyncSession, artikul: str):
    """
    Добавление данный в базу данный через API, если такой товар есть, то обновляем
    """
    url = "https://card.wb.ru/cards/v1/detail"
    params = {
        "appType": 1,
        "curr": "rub",
        "dest": -1257786,
        "spp": 30,
        "nm": artikul
    }

    async def fetch_data():
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                print(f"An error occurred: {e}")
                return None

    data = await fetch_data()

    if not data or "data" not in data or "products" not in data["data"]:
        return None

    product = data["data"]["products"][0]

    name = product.get("name", "Нет имени")
    price = product.get("salePriceU", 0) / 100
    rating = product.get("rating", 0)
    total_quantity = product.get("totalQuantity", 0)

    result = await db.execute(select(Product).where(Product.artikul == artikul))
    existing_product = result.scalars().first()

    if existing_product:
        existing_product.name = name
        existing_product.price = price
        existing_product.rating = rating
        existing_product.total_quantity = total_quantity
    else:
        new_product = Product(
            artikul=artikul,
            name=name,
            price=price,
            rating=rating,
            total_quantity=total_quantity
        )
        db.add(new_product)

    await db.commit()
    await db.refresh(existing_product if existing_product else new_product)
    return existing_product if existing_product else new_product

async def start_periodic_update(artikul: str, db):
    """
    Обновление данных по артикулю с переодичностью 30 минут
    """

    print(f"Запущен 30 мин артикуль {artikul}")

    await create_product(db, artikul)

    result = await db.execute(select(Product).where(Product.artikul == artikul))
    existing_product = result.scalars().first()

    if existing_product:
        existing_product.is_trackable = True
        await db.commit()
        await db.refresh(existing_product)

    scheduler.add_job(
        create_product,
        trigger=IntervalTrigger(minutes=30),
        args=[db, artikul],
        id=f"subscribe-{artikul}",
        replace_existing=True
    )