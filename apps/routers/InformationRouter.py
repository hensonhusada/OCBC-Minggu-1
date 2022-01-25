from fastapi import APIRouter
from main import PARAMS


APPS_INFORMATION = PARAMS.APPS_INFORMATION
router = APIRouter()


@router.get("/")
async def home():
    return APPS_INFORMATION["title"]


@router.get("/ping")
async def ping():
    return APPS_INFORMATION["version"]
