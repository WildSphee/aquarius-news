import os
import smtplib
from unittest.mock import MagicMock, patch

import pytest

from aquarius.schemas.exceptions import CustomError
from aquarius.smtp import send_mail


def test_send_mail_success(monkeypatch):
    """Test that send_mail sends an email successfully with correct SMTP setup."""
    with patch("smtplib.SMTP") as mock_smtp:
        monkeypatch.setenv("SMTP_PASSWORD", "fake_password")
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
    """Test that send_mail returns False when sending the email fails."""
    with patch("smtplib.SMTP") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        mock_server.sendmail.side_effect = smtplib.SMTPException("Sending failed")

        result = send_mail("Test Subject", "Test Body")

        assert result is False


def test_send_mail_no_password(monkeypatch):
    """Test that send_mail raises CustomError when SMTP_PASSWORD is not set."""
    # Unset SMTP_PASSWORD environment variable
    monkeypatch.delenv("SMTP_PASSWORD", raising=False)
    with pytest.raises(CustomError, match="SMTP_PASSWORD not set in .env."):
        send_mail("Test Subject", "Test Body")


@patch.dict(os.environ, {"SMTP_PASSWORD": "fake_password"})
def test_send_mail_exception():
    """Test that send_mail returns False when an exception occurs during SMTP setup."""
    with patch("smtplib.SMTP") as mock_smtp:
        mock_smtp.side_effect = Exception("General exception")

        result = send_mail("Test Subject", "Test Body")

        assert result is False
