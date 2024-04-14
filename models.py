from pydantic import BaseModel

class Order(BaseModel):
    symbol: str
    quantity: float
    price: float


class DhanPostback(BaseModel):
    order_id: str
    status: str  
