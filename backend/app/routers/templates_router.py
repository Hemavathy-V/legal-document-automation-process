from typing import List
from fastapi import APIRouter, Depends, HTTPException

from backend.app.deps.deps import get_current_user
from backend.app.schemas.schemas import TemplateResponse, UserResponse
from backend.app.services.template_service import fetch_templates
from backend.app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["templates"])

@router.get("/templates", response_model=List[TemplateResponse])
def list_templates(current_user: UserResponse = Depends(get_current_user)):
    logger.info("templates_list_requested", extra={"user": current_user.user_id})

    try:
        templates = fetch_templates()
        logger.info("templates_retrieved", extra={"count": len(templates)})
        return templates

    except Exception:
        logger.exception("templates_fetch_failed")
        raise HTTPException(500, "Unable to fetch templates")