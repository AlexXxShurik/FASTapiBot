import httpx
from typing import Optional

async def fetch_product_data(artikul: str) -> Optional[dict]:
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={artikul}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        if data.get("data") and data["data"].get("products"):
            product = data["data"]["products"][0]
            return {
                "name": product["name"],
                "price": product["salePriceU"] / 100,
                "rating": product["rating"],
                "total_quantity": product["totalQuantity"]
            }
    return None
