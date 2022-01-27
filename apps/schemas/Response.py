from pydantic import BaseModel
from typing import List


class ScrapResponse(BaseModel):
    status: int = 200
    message: str = None
    data: dict = {}

class BaseResponse(BaseModel):
    status: int = 200
    message: str = None
    data: dict = []