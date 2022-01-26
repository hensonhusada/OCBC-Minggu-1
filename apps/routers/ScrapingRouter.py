from fastapi import APIRouter, Query, Response
from apps.controllers.ScrapingController import ScrapingController
from apps.schemas import BaseResponse

router = APIRouter()

# Get articles from psychologytoday as dict
# @router.get("/get_articles")
# async def get_articles(page: int = Query(..., example=1, ge=1)):
#     data = ScrapingController.get_articles(page)
#     return data

# # Insert articles from psychologytoday to database
# @router.put("/update_articles")
# async def update_articles(page: int = Query(..., example=1, ge=1)):
#     data = ScrapingController.get_articles(page)
#     if type(data) != BaseResponse:
#         return data
#     response = ScrapingController.to_db(data.data)  # Save articles to database
#     return response

# # @router.put("/update_articles")

# # Get five newest article from database
# @router.get("/get_latest_articles")
# async def get_latest_articles(number: int | None = Query(None, ge=1)):
#     response = ScrapingController.get_some_articles(number)
#     return response

# Get article urls from psychologytoday.com
@router.get("/get_articles_urls")
async def get_articles_urls(response: Response, page_number: int| None = Query(None, ge=1)):
    result = ScrapingController.get_articles_urls()
    response.status_code = result.status
    return result

# Get article details by url
@router.get("/get_article_detail")
async def get_article_detail(response: Response, url: str):
    result = ScrapingController.get_article_detail(url)
    response.status_code = result.status
    return result