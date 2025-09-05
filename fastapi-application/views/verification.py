# from fastapi import APIRouter, Request
#
# from core.config import settings
# from utils.templates import templates
#
#
# router = APIRouter(
#     prefix=settings.view.verify_email,
# )
#
#
# @router.get(
#     "/",
#     name="verify_email",
#     include_in_schema=False,
# )
# def verify_email(
#     request: Request,
#     token: str,
# ):
#     return templates.TemplateResponse(
#         name="verification.html",
#         context={
#             "request": request,
#             "token": token,
#         },
#     )
