
A small FastAPI backend that collects product reviews sent via WhatsApp (Twilio webhook) and stores them in a database.

Features
- Receive messages from Twilio WhatsApp webhook and run a simple conversational state machine.
- Store reviews in a SQL database using SQLAlchemy.
- Exposes:
  - POST /twilio/webhook  — Twilio webhook for incoming WhatsApp messages
  - GET  /api/reviews     — Returns all collected reviews (required by the assignment)
  - GET  /twilio/reviews  — (additional) returns reviews as well

Repository layout (important files)
- `backend/app/main.py`         — FastAPI app and assignment endpoint
- `backend/app/routes/twilio_webhook.py` — Twilio webhook and conversation flow
- `backend/app/models.py`       — SQLAlchemy models (Review)
- `backend/app/db.py`           — Database init (reads DATABASE_URL from .env)
- `backend/requirements.txt`    — Python dependencies
- `frontend/`                   — React frontend (separate)

Prerequisites
- Python 3.10+ installed
- Git (optional)
- A database reachable via a SQLAlchemy URL (Postgres recommended). For a quick demo you can use SQLite.
- (For real Twilio testing) a Twilio account and a publicly accessible URL (use ngrok for local testing).

Environment variables
Create a `.env` file in `backend/` with at least the following variables:

DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DBNAME
# or for quick local demo using SQLite:
# DATABASE_URL=sqlite:///./test.db

TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_WHATSAPP_NUMBER=whatsapp:+1415XXXXXXX

Note: `backend/app/config.py` reads these values on startup and will log errors if required values are missing.

Install and run (PowerShell)
1. From project root open PowerShell and create & activate a virtual environment:

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1

2. Install dependencies:

    pip install -r backend\requirements.txt

3. Ensure `backend/.env` exists and contains `DATABASE_URL` (and Twilio vars if needed).

4. Run the FastAPI server (run from the `backend` folder or adjust the module path):

    cd backend
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

The API will be available at http://127.0.0.1:8000
- GET /api/reviews  → returns stored reviews
- POST /twilio/webhook → Twilio should POST incoming WhatsApp messages here

Testing Twilio webhooks locally
- Use a tunneling service (ngrok) to expose your local server to the internet and configure Twilio to send webhooks to:
  https://<your-ngrok-id>.ngrok.io/twilio/webhook

Notes and tips
- The backend expects a SQLAlchemy-compatible `DATABASE_URL`. For Postgres use the `postgresql+psycopg2://...` scheme. If you use SQLite for testing, the repository will create the file DB automatically.
- The code includes a simple in-memory conversation manager (`backend/app/conversation.py`). It is not persistent and is suitable for demo/assignment purposes only.
- If you plan to deploy, secure CORS settings and protect environment secrets.

Troubleshooting
- If the server fails on startup with a database error, double-check `DATABASE_URL` in `backend/.env` and ensure the target DB is reachable and credentials are correct.
- If Twilio rejects your webhook requests, verify `TWILIO_AUTH_TOKEN` in `.env` and ensure your public callback URL exactly matches the one Twilio sends (use ngrok and the `/twilio/webhook` path).


