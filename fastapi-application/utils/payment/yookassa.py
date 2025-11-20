import hmac

from hashlib import sha256
from yookassa import Configuration, Payment
from yookassa.domain.request import PaymentRequest

from core.config import settings


Configuration.account_id = settings.yookassa.account_id
Configuration.secret_key = settings.yookassa.secret_key


def generate_payment_link(
    order_id: int,
    amount: float,
    description: str,
) -> dict:
    """
    Генерирует ссылку на оплату через YooKassa.
    """
    request = PaymentRequest()
    request.amount = {
        "value": f"{amount:.2f}",
        "currency": "RUB",
    }
    request.capture = True
    request.description = description
    request.confirmation = {
        "type": "redirect",
        "return_url": f"http://{settings.run.host}:{settings.run.port}{settings.view.orders}",
    }
    request.metadata = {"order_id": order_id}

    payment = Payment.create(request)
    return {
        "payment_id": payment.id,
        "confirmation_url": payment.confirmation.confirmation_url,
        "status": payment.status,
    }


def verify_webhook_signature(
    body: str,
    signature: str,
) -> bool:
    """
    Проверяет подпись вебхука YooKassa.

    :param body: Тело запроса (в виде строки)
    :param signature: Значение заголовка X-YooKassa-Signature
    :return: True, если подпись валидна
    """
    secret_key = settings.yookassa.secret_key
    digest = hmac.new(
        secret_key.encode("utf-8"),
        body.encode("utf-8"),
        sha256,
    ).hexdigest()
    return hmac.compare_digest(digest, signature)
