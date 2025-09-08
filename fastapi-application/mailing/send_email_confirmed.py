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
    recipient_name = user.first_name
    subject = "Адрес электронной почты подтвержден"

    plain_content = dedent(
        f"""\
        Уважаемый {recipient_name},

        Ваш адрес электронной почты подтверждён.

        Спасибо за использование BoatPro.ru!
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
