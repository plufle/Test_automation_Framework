import imaplib
import os
from dotenv import load_dotenv

load_dotenv()

print("HOST:", os.getenv("IMAP_HOST"))
print("USER:", os.getenv("EMAIL_USER"))

mail = imaplib.IMAP4_SSL(
    os.getenv("IMAP_HOST")
)

mail.login(
    os.getenv("EMAIL_USER"),
    os.getenv("EMAIL_PASS")
)

print("SUCCESS")