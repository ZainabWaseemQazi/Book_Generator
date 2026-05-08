from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.temp_storage import TEMP_STORAGE
from app.database import supabase
from app.services.ai_services import regenerate_outline

router = APIRouter()
template=Jinja2Templates(directory="app/templates")

@router.get("/review-outline/{book_id}")
def review_outline_page(request: Request, book_id: str):

    outline = TEMP_STORAGE[book_id]["outline"]

    return templates.TemplateResponse(
        "outline_review.html",
        {
            "request": request,
            "outline": outline,
            "book_id": book_id
        }
    )

@router.post("/review-outline/{book_id}")
def review_outline(
    book_id: str,
    action: str = Form(...),
    notes: str = Form("")
):

    current_outline = TEMP_STORAGE[book_id]["outline"]

    if action == "approve":

        supabase.table("outlines").insert({
            "book_id": book_id,
            "outline_content": current_outline,
            "approved": True
        }).execute()

        return RedirectResponse(
            url=f"/generate-chapter/{book_id}/1",
            status_code=303
        )
    new_outline = regenerate_outline(current_outline, notes)

    TEMP_STORAGE[book_id]["outline"] = new_outline

    return RedirectResponse(
        url=f"/review-outline/{book_id}",
        status_code=303
    )

