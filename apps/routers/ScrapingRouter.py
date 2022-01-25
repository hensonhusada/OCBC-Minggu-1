from fastapi import APIRouter, Query
from apps.controllers.ScrapingController import ScrapingController
from apps.schemas import BaseResponse

router = APIRouter()

# Get articles from psychologytoday as dict
@router.get("/get_articles")
async def get_articles(page: int = Query(..., example=1, ge=1)):
    data = ScrapingController.get_articles(page)
    return data

# Insert articles from psychologytoday to database
@router.put("/update_articles")
async def update_articles(page: int = Query(..., example=1, ge=1)):
    data = ScrapingController.get_articles(page)
    if type(data) != BaseResponse:
        return data
    response = ScrapingController.to_db(data.data)  # Save articles to database
    return response

# @router.put("/update_articles")

# Get five newest article from database
@router.get("/get_latest_articles")
async def get_latest_articles(number: int | None = Query(None, ge=1)):
    response = ScrapingController.get_some_articles(number)
    return response