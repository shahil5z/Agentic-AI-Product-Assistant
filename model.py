from pydantic import BaseModel
from typing import List

class ProductResponse(BaseModel):
    name: str
    details: str
    price: int
    release_date: str
    advantages: List[str]
    disadvantages: List[str]
