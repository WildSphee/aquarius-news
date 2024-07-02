import smtplib

from_gmailaddress = "gooseabot@gmail.com"
to_gmailaddress = ["gooseabot@gmail.com"]
app_password = "fggpahvdkwbpicqx"


def send_mail(subject: str = "Empty Subject", body: str = "empty body") -> bool:
    """
    send an email using google SMTP

    subject (str): The title of the email
    body (str): The body of the email
    """

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
