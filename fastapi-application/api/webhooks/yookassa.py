import json

from typing import Annotated
from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.orders_service import OrdersService

from core.config import settings
from core.dependencies import get_db_session
from core.models.orders import Order, OrderStatus
from utils.payment.yookassa import verify_webhook_signature


router = APIRouter(
    prefix=settings.api.v1.yookassa,
    include_in_schema=True,
)


@router.post("")
async def yookassa_webhook(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """
    Обработчик вебхука от YooKassa.

    Принимает уведомления о статусе платежа (например, успешная оплата).
    Проверяет подпись запроса, извлекает ID заказа из metadata и обновляет статус заказа на `paid`.

    ## Ожидаемый сценарий:
    - Пользователь оплачивает заказ.
    - YooKassa отправляет POST-запрос на этот эндпоинт.
    - Сервер проверяет подпись и статус платежа.
    - Если статус `payment.succeeded` — заказ помечается как оплаченный.

    ## Требования:
    - Запрос должен содержать заголовок `X-YooKassa-Signature`.
    - Тело запроса должно быть валидным JSON.
    - В `metadata` платежа должен быть `order_id`.

    ## Ответы:
    - `200 OK` — вебхук успешно обработан.
    - `400 Bad Request` — ошибка валидации, подпись не совпадает, неверные данные.
    - `404 Not Found` — заказ не найден.
    """
    body = await request.body()
    signature = request.headers.get("X-YooKassa-Signature")

    if not signature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing X-YooKassa-Signature header",
        )

    if not verify_webhook_signature(body.decode("utf-8"), signature):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid signature",
        )

    try:
        data = json.loads(body.decode("utf-8"))
        event = data.get("event")
        payment = data.get("object")

        if event != "payment.succeeded":
            return {"status": "ignored"}

        order_id = int(payment["metadata"].get("order_id", 0))
        if not order_id:
            raise HTTPException(status_code=400, detail="Invalid order_id in metadata")

        service = OrdersService(session=session)
        order = await service.get_order_by_id(order_id=order_id)
        if not order:
            raise HTTPException(
                status_code=404,
                detail="Order not found",
            )

        if payment["status"] == "succeeded":
            order.status = OrderStatus.PAID
            await session.commit()

        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Webhook error: {str(e)}",
        )
