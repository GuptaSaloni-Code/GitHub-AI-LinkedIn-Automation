# AI-Powered Developer Content Automation System

An AI-powered automation system that converts GitHub development activity into professional LinkedIn post drafts.

Whenever a developer pushes a commit to a connected GitHub repository, the system receives the event through a GitHub Webhook, analyzes the commit and code changes, generates a LinkedIn-ready post using Google Gemini, and sends the draft to the developer through email.

The final LinkedIn post is reviewed and published manually by the developer.

---

## Project Overview

Developers frequently work on projects and make meaningful technical changes, but documenting and sharing their progress on professional platforms can be time-consuming.

This project automates the content creation part of that process.

Instead of manually writing a LinkedIn post after every important development update:

GitHub Commit → AI Analysis → LinkedIn Draft → Email

The system automatically converts development activity into a professional content draft while keeping the final publishing decision with the developer.

---

## Features

- GitHub Push Webhook integration
- Automatic detection of new commits
- Fetches commit details using GitHub REST API
- Retrieves:
  - Commit message
  - Changed files
  - File status
  - Additions and deletions
  - Code diff
- AI-powered LinkedIn post generation using Google Gemini
- Professional LinkedIn post structure
- Automatic email delivery of generated drafts
- Human review before publishing
- Webhook authentication using HMAC SHA-256
- No database required
- Cloud deployment using Render
- Secure environment variable based API key management
- Testing it
- fixed bug

---

## System Architecture

```text
Developer
    │
    │ Git Push
    ▼
GitHub Repository
    │
    │ GitHub Webhook
    ▼
FastAPI Backend
    │
    │ GitHub REST API
    ▼
Commit Details + Code Diff
    │
    ▼
Google Gemini
    │
    │ AI Generated LinkedIn Draft
    ▼
Resend Email API
    │
    ▼
Developer Email
    │
    │ Review / Edit
    ▼
Manual LinkedIn Post
