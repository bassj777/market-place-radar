from pydantic import BaseModel, HttpUrl


class Offer(BaseModel):
    title: str
    price: float
    location: str
    url: HttpUrl
    category: str
    score: int = 0