from typing import Any
from fastapi import Request
from fastapi.responses import ORJSONResponse, RedirectResponse
from starlette.types import ASGIApp, Receive, Scope, Send


class CustomRateLimitMiddleware:
    """
    CustomRateLimitMiddleware для перехвата и обработки ответов с кодом 429 (Too Many Requests).

    Назначение:
    -----------
    Этот модуль содержит `CustomRateLimitMiddleware` — кастомный middleware для FastAPI, который перехватывает
    ответы с кодом **429 Too Many Requests** (слишком много запросов) и возвращает пользователю корректный
    ответ в зависимости от типа запроса:

    - Для **API-запросов** (`/api/...`) — возвращает JSON-ответ с сообщением об ошибке.
    - Для **веб-страниц** — перенаправляет на страницу `/limit-exceeded`.

    Таким образом, обеспечивается:
    - Удобная обработка лимитов для фронтенда (через JSON).
    - Понятный UX для пользователей (через редирект на страницу с пояснением).

    Особенности:
    ------------
    - Работает поверх стандартного механизма rate limiting (например, `slowapi` или `fastapi-limiter`).
    - Не блокирует запрос, а **перехватывает ответ** с кодом 429.
    - Позволяет избежать вывода "голого" текста в браузере при превышении лимита.

    Логика работы:
    ---------------
    1. Middleware ожидает завершения обработки запроса.
    2. Когда сервер пытается отправить ответ с `status=429`, middleware перехватывает его.
    3. В зависимости от пути:
       - Если путь начинается с `/api` → возвращается `ORJSONResponse` с JSON-ошибкой.
       - Иначе → редирект на `/limit-exceeded`.
    4. Оригинальный ответ не отправляется.

    Использование:
    --------------
    Добавляется в приложение через `app.add_middleware(CustomRateLimitMiddleware)`
    """

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope)
        override_send = self.create_override_send(scope, receive, request, send)
        await self.app(scope, receive, override_send)

    def create_override_send(
        self,
        scope: Scope,
        receive: Receive,
        request: Request,
        send: Send,
    ) -> Send:
        sent = False

        async def override_send(message: dict[str, Any]) -> None:
            nonlocal sent

            if sent:
                return

            if message["type"] == "http.response.start" and message["status"] == 429:
                sent = True

                if request.url.path.startswith("/api"):
                    response = ORJSONResponse(
                        content={"detail": "Слишком много запросов, попробуйте позже."},
                        status_code=429,
                    )
                else:
                    response = RedirectResponse(url="/limit-exceeded")

                await response(scope, receive, send)
                return

            await send(message)

        return override_send
