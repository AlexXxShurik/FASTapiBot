from pydantic import BaseModel

class ProductCreate(BaseModel):
    artikul: str

class ProductResponse(BaseModel):
    id: int
    name: str
    artikul: str
    price: float
    rating: float
    total_quantity: int
    is_trackable: bool

    class Config:
        from_attributes = True
