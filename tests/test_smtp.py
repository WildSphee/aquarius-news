import os
import smtplib
from unittest.mock import MagicMock, patch

import pytest

from aquarius.schemas.exceptions import CustomError
from aquarius.smtp import send_mail


def test_send_mail_success(monkeypatch):
    monkeypatch.setenv("SMTP_PASSWORD", "fake_password")

    with patch("send_mail.smtplib.SMTP") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        result = send_mail("Test Subject", "Test Body")

        assert result is True
        mock_server.ehlo.assert_called()
        mock_server.starttls.assert_called()
        mock_server.login.assert_called_with("gooseabot@gmail.com", "fake_password")
        mock_server.sendmail.assert_called_with(
            "gooseabot@gmail.com",
            ["gooseabot@gmail.com"],
            b"Subject:Test Subject\nTest Body",
        )
        mock_server.quit.assert_called()


@patch.dict(os.environ, {"SMTP_PASSWORD": "fake_password"})
def test_send_mail_failure():
    with patch("smtplib.SMTP") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        mock_server.sendmail.side_effect = smtplib.SMTPException("Sending failed")

        result = send_mail("Test Subject", "Test Body")

        assert result is False


def test_send_mail_no_password(monkeypatch):
    # Unset SMTP_PASSWORD environment variable
    monkeypatch.delenv("SMTP_PASSWORD", raising=False)
    with pytest.raises(CustomError, match="SMTP_PASSWORD not set in .env."):
        send_mail("Test Subject", "Test Body")


# Additional test for exception handling
@patch.dict(os.environ, {"SMTP_PASSWORD": "fake_password"})
def test_send_mail_exception():
    with patch("smtplib.SMTP") as mock_smtp:
        mock_smtp.side_effect = Exception("General exception")

        result = send_mail("Test Subject", "Test Body")

        assert result is False
