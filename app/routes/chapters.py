from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.database import supabase
from app.temp_storage import TEMP_STORAGE
from app.services.ai_services import (
    generate_chapter,
    regenerate_chapter,
    generate_summary
)
from app.services.email_service import send_email
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


CHAPTERS = [
    "Introduction",
    "Main Concepts",
    "Conclusion"
]


@router.get("/generate-chapter/{book_id}/{chapter_number}")
async def create_chapter(book_id: str, chapter_number: int):

    book = supabase.table("books").select("*").eq("id", book_id).execute().data[0]

    approved_chapters = supabase.table("chapters") \
        .select("*") \
        .eq("book_id", book_id) \
        .execute().data
    
    context = "".join([
        c["chapter_summary"] for c in approved_chapters
    ])

    research_summary = TEMP_STORAGE[book_id]["research_summary"]

    chapter_title = CHAPTERS[chapter_number - 1]

    chapter_text = generate_chapter(
        book["title"],
        chapter_title,
        research_summary,
        context
    )

    summary = generate_summary(chapter_text)

    TEMP_STORAGE[f"{book_id}_{chapter_number}"] = {
        "chapter_title": chapter_title,
        "chapter_content": chapter_text,
        "chapter_summary": summary
    }

    review_link = f"http://127.0.0.1:8000/review-chapter/{book_id}/{chapter_number}"

    await send_email(
        subject=f"Chapter {chapter_number} Ready",
        recipient=book["editor_email"],
        body=f"Review chapter here: {review_link}"
    )

    return RedirectResponse(review_link, status_code=303)

