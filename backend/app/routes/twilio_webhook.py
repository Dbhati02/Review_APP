from fastapi import APIRouter, Request, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from twilio.request_validator import RequestValidator

from ..db import SessionLocal
from ..models import Review
from ..schemas import ReviewOut
from ..config import settings
from ..conversation import conv
from ..utils import safe_extract
from loguru import logger

router = APIRouter()

# Initialize Twilio Validator
validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)


# ---------------- DB DEPENDENCY ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------------- WHATSAPP WEBHOOK -----------------------------
@router.post("/webhook", response_class=PlainTextResponse)
async def twilio_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Twilio WhatsApp webhook. Validates signature and processes the conversation.
    """
    form = await request.form()

    # -------- FIX SIGNATURE VALIDATION URL PROBLEM --------
    # Twilio sends webhook URL WITHOUT query parameters.
    # FastAPI request.url includes them → mismatch → INVALID.
    # We reconstruct the base URL exactly like Twilio expects.
    base_url = str(request.url).split("?")[0]

    signature = request.headers.get("X-Twilio-Signature", "")

    if not validator.validate(base_url, form, signature):
        logger.warning(f"Invalid Twilio signature for URL: {base_url}")
        return PlainTextResponse("Invalid request signature.", status_code=403)

    # Extract fields
    user_number = safe_extract(form, "From")
    body = safe_extract(form, "Body").strip()

    logger.info(f"Message from {user_number}: {body}")

    # -------- SAFE STATE INITIALIZATION --------
    state = conv.get(user_number)

    if state is None:
        state = {"stage": "start"}
        conv.update(user_number, state)

    # --------- STATE MACHINE LOGIC ----------
    if state["stage"] == "start":
        conv.update(user_number, {"stage": "awaiting_product"})
        return "Hi! 😊 Which product do you want to review?"

    elif state["stage"] == "awaiting_product":
        conv.update(user_number, {
            "stage": "awaiting_name",
            "product": body
        })
        return "Great! What's your name?"

    elif state["stage"] == "awaiting_name":
        state["name"] = body
        state["stage"] = "awaiting_review"
        conv.update(user_number, state)
        return f"Awesome, {body}! Please type your review now."

    elif state["stage"] == "awaiting_review":
        new_review = Review(
            contact_number=user_number,
            user_name=state["name"],
            product_name=state["product"],
            product_review=body
        )
        db.add(new_review)
        db.commit()
        db.refresh(new_review)

        conv.reset(user_number)

        return f"Thanks {state['name']}! 🎉 Your review for {state['product']} is saved."

    else:
        conv.reset(user_number)
        return "Let's start again 😊 Which product would you like to review?"


# ----------------------------- GET ALL REVIEWS -----------------------------
@router.get("/reviews", response_model=list[ReviewOut])
def get_reviews(db: Session = Depends(get_db)):
    """
    Returns all stored reviews.
    """
    data = db.query(Review).order_by(Review.created_at.desc()).all()
    return data
