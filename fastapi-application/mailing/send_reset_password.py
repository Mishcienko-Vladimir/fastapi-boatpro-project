from textwrap import dedent

from core.models import User
from mailing.send_email import send_email
from utils import templates


async def send_reset_password(
    user: User,
    reset_password_link: str,
):
    """
    Отправка пользователю письма со сбросом пароля.

    :param user: - пользователь.
    :param reset_password_link: - ссылка для сброса пароля.
    :return:
    """

    recipient = user.email
    recipient_name = user.first_name
    subject = f"Сбросить пароль на BoatPro.ru"

    plain_content = dedent(
        f"""\
        Уважаемый {recipient_name},

        Для сброса пароля, пожалуйста, перейдите по ссылке:
        {reset_password_link}

        Спасибо за использование BoatPro.ru!
        © 2025 BoatPro.ru
        """
    )

    template = templates.get_template(
        "mailing/email-verify/verification_request.html"
    )  # !!!!!!!!!!!
    context = {
        "user": user,
        "reset_password_link": reset_password_link,
    }
    html_content = template.render(context)
    await send_email(
        recipient=recipient,
        subject=subject,
        plain_content=plain_content,
        html_content=html_content,
    )
