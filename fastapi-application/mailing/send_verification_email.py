from textwrap import dedent

from core.models import User
from mailing.send_email import send_email
from utils import templates


async def send_verification_email(
    user: User,
    verification_link: str,
):
    """
    Отправка пользователю письма с подтверждением email.

    :param user: Пользователь.
    :param verification_link: Ссылка для подтверждения email.
    :return: None. Функция ничего не возвращает.
    """

    recipient = user.email
    recipient_name = user.first_name
    subject = f"Подтвердите адрес электронной почты для BoatPro.ru"

    plain_content = dedent(
        f"""\
        Уважаемый {recipient_name},
        
        Для подтверждения email, пожалуйста, перейдите по ссылке:
        {verification_link}
        
        Спасибо за регистрацию на BoatPro.ru!
        © 2025 BoatPro.ru
        """
    )

    template = templates.get_template("mailing/email-verify/verification_request.html")
    context = {
        "user": user,
        "verification_link": verification_link,
    }
    html_content = template.render(context)
    await send_email(
        recipient=recipient,
        subject=subject,
        plain_content=plain_content,
        html_content=html_content,
    )
