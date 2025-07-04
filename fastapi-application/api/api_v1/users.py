from fastapi import APIRouter


router = APIRouter(tags=["Users"])

@router.get("/")
async def get_users():
    pass