from fastapi import APIRouter, Depends, HTTPException

from core.config import settings
from core.schemas.products import BoatCreate, BoatUpdate, BoatRead


router = APIRouter(prefix=settings.api.v1.boats, tags=["Катера"])


@router.get("/")
def get_boats():
    return {"message": "Hello, World!"}


# def get_boat_service(db=Depends(get_db)):
#     return BoatService(db)
#
#
# @router.get("/", response_model=list[BoatRead])
# def read_boats(service: BoatService = Depends(get_boat_service)):
#     return service.get_all()
#
#
# @router.get("/{boat_id}", response_model=BoatRead)
# def read_boat(boat_id: int, service: BoatService = Depends(get_boat_service)):
#     boat = service.get(boat_id)
#     if not boat:
#         raise HTTPException(status_code=404, detail="Boat not found")
#     return boat
#
#
# @router.post("/", response_model=BoatRead)
# def create_boat(
#     boat: BoatCreate,
#     service: BoatService = Depends(get_boat_service),
# ):
#     return service.create(boat)
#
#
# @router.put("/{boat_id}", response_model=BoatRead)
# def update_boat(
#     boat_id: int,
#     boat: BoatCreate,
#     service: BoatService = Depends(get_boat_service),
# ):
#     updated_boat = service.update(boat_id, boat)
#     if not updated_boat:
#         raise HTTPException(status_code=404, detail="Boat not found")
#     return updated_boat
#
#
# @router.delete("/{boat_id}")
# def delete_boat(
#     boat_id: int,
#     service: BoatService = Depends(get_boat_service),
# ):
#     if not service.delete(boat_id):
#         raise HTTPException(status_code=404, detail="Boat not found")
#     return {"message": "Boat deleted"}
