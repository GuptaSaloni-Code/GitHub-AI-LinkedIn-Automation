from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_linkedin_post(
    commit_message,
    changed_files,
    code_diff
):

    prompt = f"""
You are a professional technical content writer.

Create a professional LinkedIn post based ONLY on the GitHub development
information provided below.

Do not invent features, technologies, results, or achievements.

GitHub Commit:
{commit_message}

Changed Files:
{changed_files}

Code Diff:
{code_diff}

Write the LinkedIn post in this structure:

1. Strong opening hook
2. What was built or changed
3. Short technical explanation
4. What was learned or improved
5. Professional closing
6. 4-6 relevant hashtags

Keep the post clear, natural, and suitable for a software developer's LinkedIn profile.

Do not mention that AI generated the post.
"""

    response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
)

    return response.text