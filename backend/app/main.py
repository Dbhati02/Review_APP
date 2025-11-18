from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import twilio_webhook
from .db import Base, engine

# Create all tables in DB
Base.metadata.create_all(bind=engine)

# FastAPI app instance
app = FastAPI(title="WhatsApp Product Review Collector")

# Enable CORS for frontend (React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # allow all origins (safe for assignment demo)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

# -----------------------------
# Include Twilio Webhook Router
# -----------------------------
# NOTE: This exposes:
# POST /twilio/webhook
# GET  /twilio/reviews  (not required by assignment)
app.include_router(
    twilio_webhook.router,
    prefix="/twilio"
)

# -----------------------------
# REQUIRED ASSIGNMENT ENDPOINT:
# GET /api/reviews
# -----------------------------
@app.get("/api/reviews")
def get_all_reviews():
    """
    Assignment requires GET /api/reviews
    This function simply calls the existing twilio_webhook.reviews handler internally.
    """
    from .db import SessionLocal
    from .models import Review
    from .schemas import ReviewOut

    db = SessionLocal()
    data = db.query(Review).order_by(Review.created_at.desc()).all()
    db.close()

    return data
