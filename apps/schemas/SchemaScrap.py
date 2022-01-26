import datetime
from nturl2path import url2pathname
from operator import index
from turtle import title
from pydantic import BaseModel
from typing import List

class ResponseScrapURL(BaseModel):
    url_list: List[str]

class ResponseScrapDetail(BaseModel):
    index: str = None
    title: str
    author: str
    magazine: str
    publishdate: datetime.date
    url: str
    paragraph: str = None

class ShortArticle(BaseModel):
    title: str
    author: str
    publishdate: datetime.date
    url: str

class SomeArticle(BaseModel):
    article_list: List[ShortArticle]

