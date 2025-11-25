from fastapi import APIRouter

from core.schemas.user import UserRegisteredNotification

router = APIRouter()


@router.post("user-created")
def notify_user_created(info: UserRegisteredNotification):
    """
    Этот вебхук будет активирован при создании пользователя..
    """
