from typing import Any
from fastapi import Request
from fastapi.responses import ORJSONResponse, RedirectResponse
from starlette.types import ASGIApp, Receive, Scope, Send


class CustomRateLimitMiddleware:
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
