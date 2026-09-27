from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv
import requests
import os
import hmac
import hashlib

from app.ai_service import generate_linkedin_post
from app.email_service import send_linkedin_draft

load_dotenv()

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

app = FastAPI(
    title="AI-Powered Developer Content Automation System",
    description="Converts GitHub development activity into AI-generated LinkedIn content.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "AI Developer Content Automation System is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/github-webhook")
async def github_webhook(request: Request):

    # Read the raw request body
    body = await request.body()

    # Get GitHub's signature
    signature = request.headers.get("X-Hub-Signature-256")

    if not signature:
        raise HTTPException(
            status_code=401,
            detail="Missing GitHub signature"
        )

    # Create our own signature using the secret
    expected_signature = "sha256=" + hmac.new(
        WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    # Compare signatures securely
    if not hmac.compare_digest(
        signature,
        expected_signature
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid GitHub signature"
        )

    # Convert request body to JSON
    data = await request.json()

    print("\n========================================")
    print("        GitHub Push Received!")
    print("========================================")

    # Repository information
    repository = data.get("repository", {})
    repo_name = repository.get("full_name")

    branch = data.get("ref")
    commit_sha = data.get("after")

    print("Repository:", repo_name)
    print("Branch:", branch)
    print("Commit SHA:", commit_sha)

    # Variables for AI
    commit_message = ""
    changed_files_text = ""
    code_diff_text = ""

    # Get commit details
    if repo_name and commit_sha:

        api_url = (
            f"https://api.github.com/repos/"
            f"{repo_name}/commits/{commit_sha}"
        )

        response = requests.get(api_url)

        if response.status_code == 200:

            commit_data = response.json()

            # Commit message
            commit_message = commit_data.get(
                "commit", {}
            ).get(
                "message",
                ""
            )

            print("\nCommit Message:")
            print(commit_message)

            # Changed files
            files = commit_data.get("files", [])

            print("\nChanged Files:")

            for file in files:

                filename = file.get("filename")
                status = file.get("status")
                additions = file.get("additions")
                deletions = file.get("deletions")

                file_info = (
                    f"{filename} | "
                    f"{status} | "
                    f"+{additions} / -{deletions}"
                )

                print("-", file_info)

                changed_files_text += (
                    file_info + "\n"
                )

                # Actual code diff
                patch = file.get("patch")

                if patch:

                    print("\n--- CODE DIFF ---")
                    print(patch)
                    print("--- END DIFF ---")

                    code_diff_text += (
                        f"\nFile: {filename}\n"
                        f"{patch}\n"
                    )

        else:

            print(
                "\nGitHub API Error:",
                response.status_code
            )

    # Generate LinkedIn post using Gemini
    if commit_message:

        print("\nGenerating LinkedIn post with Gemini...")

        linkedin_post = generate_linkedin_post(
            commit_message=commit_message,
            changed_files=changed_files_text,
            code_diff=code_diff_text
        )

        print("\n========================================")
        print("       AI GENERATED LINKEDIN POST")
        print("========================================")
        print(linkedin_post)
        print("========================================")

        # Send LinkedIn draft by email
        print("\nSending LinkedIn draft by email...")

        email_result = send_linkedin_draft(
            linkedin_post=linkedin_post,
            commit_message=commit_message
        )

        print("\n========================================")
        print("             EMAIL SENT")
        print("========================================")
        print(email_result)
        print("========================================")

    else:

        linkedin_post = ""
        email_result = None

    return {
        "status": "received",
        "linkedin_post": linkedin_post,
        "email": email_result
    } 