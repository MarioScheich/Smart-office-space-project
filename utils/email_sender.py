# utils/email_sender.py
import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "aamsciot@gmail.com"           # ✅ Your Gmail address
SMTP_PASSWORD = "wmry zqhb djta ahtt"     # ✅ Paste 16-char App Password here

def send_email(subject, body, recipients):
    if not recipients:
        print("❌ No recipients specified.")
        return

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = ", ".join(recipients)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, recipients, msg.as_string())
            print(f"📧 Email sent to {', '.join(recipients)}")
    except Exception as e:
        print("❌ Failed to send email:", e)
