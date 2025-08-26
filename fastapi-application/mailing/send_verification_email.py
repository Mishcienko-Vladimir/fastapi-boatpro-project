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

    :param user: - пользователь.
    :param verification_link: - ссылка для подтверждения email.
    :return:
    """

    recipient = user.email
    subject = f"Confirm your email for MFBoats.com"

    plain_content = dedent(
        f"""\
        Dear {recipient},
        
        Please follow the link to verify your email:
        {verification_link}
        
        Thank you for using MFBoats.com!
        © 2025 MFBoats.com
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
