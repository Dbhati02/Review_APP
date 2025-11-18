from fastapi import HTTPException
from loguru import logger

def safe_extract(form, key):
    """Extract form field safely."""
    try:
        return form.get(key, "").strip()
    except Exception as e:
        logger.error(f"Failed to extract form key={key}: {e}")
        return ""
