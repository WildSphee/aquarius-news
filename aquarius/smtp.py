import os
import smtplib

from dotenv import load_dotenv
from schemas.exceptions import CustomError

load_dotenv()

from_gmailaddress = "gooseabot@gmail.com"
to_gmailaddress = ["gooseabot@gmail.com"]
app_password = os.getenv("SMTP_PASSWORD")


def send_mail(subject: str = "Empty Subject", body: str = "empty body") -> bool:
    """
    send an email using google SMTP

    attribute:
        subject (str): The title of the email
        body (str): The body of the email
    return:
        bool: if success, returns true, on exception false
    """

    if not app_password:
        raise CustomError("SMTP_PASSWORD not set in .env.")

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(from_gmailaddress, app_password)

        msg = f"Subject:{subject}\n{body}"

        server.sendmail(from_gmailaddress, to_gmailaddress, msg.encode("utf-8"))

        print("email has been sent")
        server.quit()
        return True

    except Exception as e:
        print("email sending failed", e)
        return False
