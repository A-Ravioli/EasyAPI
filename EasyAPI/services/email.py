import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailService:
    def __init__(self, provider, **credentials):
        self.provider = provider
        if provider == "smtp":
            self.client = smtplib.SMTP(credentials["host"], credentials["port"])
            self.client.starttls()
            self.client.login(credentials["username"], credentials["password"])
        # Additional providers like SendGrid or AWS SES can be added here

    def send_email(self, to_address, subject, body, from_address=None):
        message = MIMEMultipart()
        message["From"] = from_address or "noreply@example.com"
        message["To"] = to_address
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        text = message.as_string()
        self.client.sendmail(from_address, to_address, text)
        return f"Email sent to {to_address}"
