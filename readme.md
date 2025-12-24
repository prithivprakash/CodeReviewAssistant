# AI Code Review Assistant

An AI-powered code assistant that can:
- Review code and point out issues
- Explain existing code
- Generate new code from natural language
- Assist with SQL query generation

The project is built as a **full-stack application** with:
- **FastAPI (Python)** backend
- **Next.js (React)** frontend
- Pluggable LLM providers (Groq, OpenAI, Gemini)

---

## Features

- Multiple modes:
  - **Review** – strict code review with bugs, complexity, and fixes
  - **Explain** – clear explanation of what the code does
  - **Generate** – generate production-ready code from requirements
  - **SQL** – convert requirements into optimized SQL queries
- Supports multiple programming languages (starting with Python & SQL)
- Uses environment variables for API keys (no hardcoded secrets)
- Clean frontend that displays raw LLM output reliably

---

## Tech Stack

### Backend
- Python
- FastAPI
- LangChain
- Environment-based provider selection

### Frontend
- Next.js (App Router)
- React
- Tailwind CSS

---

## Project Structure

.
├── backend/
│ ├── main.py
│ ├── llm_factory.py
│ ├── python_analyzer.py
│ ├── requirements.txt
│ └── .env.example
│
├── frontend/
│ ├── app/
│ ├── lib/
│ ├── public/
│ ├── package.json
│ └── next.config.ts
│
├── .gitignore
└── README.md

yaml
Copy code

---

## Setup Instructions

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux or MacOS
pip install -r requirements.txt
Create a .env file based on .env.example, then run:

bash
Copy code
uvicorn main:app --reload
Backend runs on http://127.0.0.1:8000.

Frontend
bash
Copy code
cd frontend
npm install
npm run dev
Frontend runs on http://localhost:3000.

Environment Variables
API keys are not committed.
Use .env.example to configure:

Default LLM provider

Provider-specific API keys

Future Improvements
Structured JSON output from backend

Rich UI rendering for sections and code blocks

More static analysis per language

Authentication & usage limits

License
MIT

yaml
Copy code

This README is:
- Honest
- Not over-claiming
- Recruiter-friendly
- Leaves room for growth

---

## Commit and push README

From repo root:

```bash
git add README.md
git commit -m "Add initial README with setup and project overview"
git push