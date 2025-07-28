from fastapi import APIRouter


router = APIRouter(tags=["Каталог"])


@router.get("/")
def get_product_types():
    return {"message": "Hello, World!"}
