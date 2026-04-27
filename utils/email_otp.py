import imaplib
import email
import re
import time


def fetch_otp(email_user, email_pass, subject="Your TRY Login Code", retries=5, delay=5):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_user, email_pass)

    for _ in range(retries):
        mail.select("inbox")

        status, data = mail.search(None, f'(UNSEEN SUBJECT "{subject}")')
        mail_ids = data[0].split()

        if not mail_ids:
            time.sleep(delay)
            continue

        latest_email_id = mail_ids[-1]

        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        match = re.search(r"\b\d{6}\b", body)
        if match:
            otp = match.group()

            mail.store(latest_email_id, '+FLAGS', '\\Seen')
            return otp

        time.sleep(delay)

    raise Exception("OTP not found")