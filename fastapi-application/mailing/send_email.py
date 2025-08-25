import aiosmtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from core.config import settings


async def send_email(
    recipient: str,
    subject: str,
    plain_content: str,
    html_content: str = "",
):
    """
    Функция отправки письма.

    :param recipient: - кому мы отправляем.
    :param subject: - тема письма.
    :param plain_content: - текст письма.
    :param html_content: - html письма.
    :return:
    """

    admin_email = settings.admin.admin_email

    message = MIMEMultipart("alternative")
    message["From"] = admin_email
    message["To"] = recipient
    message["Subject"] = subject

    plain_text_message = MIMEText(
        plain_content,
        "plain",
        "utf-8",
    )
    message.attach(plain_text_message)

    if html_content:
        html_message = MIMEText(
            html_content,
            "html",
            "utf-8",
        )
        message.attach(html_message)

    await aiosmtplib.send(
        message,
        hostname="127.0.0.1",
        port=1025,
    )
