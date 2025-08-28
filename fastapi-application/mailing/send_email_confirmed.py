from textwrap import dedent

from core.models import User
from mailing.send_email import send_email
from utils import templates


async def send_email_confirmed(user: User):
    """
    Отправка письма пользователю о подтверждении email.

    :param user: - пользователь.
    :return:
    """

    recipient = user.email
    subject = "Email confirmed"

    plain_content = dedent(
        f"""\
        Dear {recipient},

        Your email has been confirmed.

        Thank you for using BoatPro.ru!
        © 2025 BoatPro.ru
        """
    )

    template = templates.get_template("mailing/email-verify/email-verified.html")
    context = {"user": user}
    html_content = template.render(context)
    await send_email(
        recipient=recipient,
        subject=subject,
        plain_content=plain_content,
        html_content=html_content,
    )
