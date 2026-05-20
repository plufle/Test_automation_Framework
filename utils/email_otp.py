import os
import imaplib
import email
import re
import time

IMAP_HOST = os.getenv("IMAP_HOST", "imap.gmail.com")


def fetch_otp(
    email_user,
    email_pass,
    subject="Your TRY Login Code",
    retries=10,
    delay=5,
):
    """
    Poll IMAP inbox for an OTP email matching *subject*.

    Retries up to *retries* times with *delay* seconds between each attempt
    (default: 10 × 5s = 50s total wait). Marks the email as Seen once found.

    Raises Exception with diagnostic info if the OTP is not found.
    """
    mail = imaplib.IMAP4_SSL(IMAP_HOST)
    mail.login(email_user, email_pass)

    for attempt in range(1, retries + 1):
        mail.select("inbox")

        status, data = mail.search(
            None,
            f'(UNSEEN SUBJECT "{subject}")'
        )

        mail_ids = data[0].split()

        if not mail_ids:
            print(f"[OTP] Attempt {attempt}/{retries}: no unread emails matching '{subject}'. Waiting {delay}s...")
            time.sleep(delay)
            continue

        latest_email_id = mail_ids[-1]

        status, msg_data = mail.fetch(
            latest_email_id,
            "(RFC822)"
        )

        msg = email.message_from_bytes(msg_data[0][1])

        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = (
                        part.get_payload(decode=True)
                        .decode(errors="ignore")
                    )
        else:
            body = (
                msg.get_payload(decode=True)
                .decode(errors="ignore")
            )

        match = re.search(r"\b\d{6}\b", body)

        if match:
            otp = match.group()
            print(f"[OTP] Found OTP on attempt {attempt}/{retries}")

            mail.store(
                latest_email_id,
                "+FLAGS",
                "\\Seen"
            )

            mail.logout()
            return otp

        print(f"[OTP] Attempt {attempt}/{retries}: email found but no 6-digit code in body. Waiting {delay}s...")
        time.sleep(delay)

    mail.logout()
    raise Exception(
        f"OTP not found after {retries} attempts ({retries * delay}s). "
        f"Subject filter: '{subject}', IMAP host: {IMAP_HOST}, user: {email_user}"
    )

    fetch_otp()