import smtplib
from email.message import EmailMessage
from config import Config

def send_alert_email(to_email: str, subject: str, body: str) -> bool:
    """
    Send alert email if email is enabled in config. Returns True if attempted.
    """
    if not Config.EMAIL_ENABLED or not Config.EMAIL_USERNAME or not Config.EMAIL_PASSWORD or not Config.EMAIL_FROM:
        return False

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = Config.EMAIL_FROM
    msg["To"] = to_email
    msg.set_content(body)

    try:
        with smtplib.SMTP(Config.EMAIL_SMTP_HOST, Config.EMAIL_SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(Config.EMAIL_USERNAME, Config.EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print("Email send failed:", e)
        return False