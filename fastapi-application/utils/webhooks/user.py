# Функция для отправки уведомления о новом пользователе
import logging
import aiohttp
import time

from core.models import User
from core.config import settings
from core.schemas.user import UserRead, UserRegisteredNotification

log = logging.getLogger(__name__)


async def send_new_user_notification(user: User) -> None:
    wh_data = UserRegisteredNotification(
        user=UserRead.model_validate(user),
        ts=int(time.time()),
    ).model_dump()
    log.info("Notify user created with data: %s", wh_data)
    async with aiohttp.ClientSession() as session:
        async with session.post(settings.webhook.webhook_url, json=wh_data) as response:
            data = await response.json()
            log.info("Sent webhook, got response: %s", data)
