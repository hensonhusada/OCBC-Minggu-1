import datetime
from nturl2path import url2pathname
from operator import index
from turtle import title
from pydantic import BaseModel
from typing import List

class ResponseScrapURL(BaseModel):
    url_list: List[str]

class ResponseScrapDetail(BaseModel):
    index: str
    title: str
    author: str
    magazine: str
    publishdate: datetime.datetime
    url: str
    paragraph: str