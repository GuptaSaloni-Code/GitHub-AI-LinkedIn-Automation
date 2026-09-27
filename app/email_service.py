import resend
import os
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")


def send_linkedin_draft(linkedin_post, commit_message):

    params = {
        "from": "onboarding@resend.dev",
        "to": [os.getenv("EMAIL_TO")],
        "subject": f"LinkedIn Draft - {commit_message}",
        "text": linkedin_post
    }

    email = resend.Emails.send(params)

    return email