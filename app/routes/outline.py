from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.services.ai_services import (
    generate_outline,
    summarize_search_content
)

from app.services.serpapi_service import search_book_content
from app.services.email_service import send_email

from app.database import supabase
from app.temp_storage import TEMP_STORAGE

router = APIRouter()


@router.get("/generate-outline/{book_id}")
async def create_outline(book_id: str):

    book = supabase.table("books") \
        .select("*") \
        .eq("id", book_id) \
        .execute().data[0]

    # Search research content
    search_content = search_book_content(
        book["title"]
    )

    # Summarize research
    research_summary = summarize_search_content(
        search_content
    )

    # Generate outline
    outline = generate_outline(
        book["title"],
        research_summary
    )

    # Store temporarily
    TEMP_STORAGE[book_id] = {
        "outline": outline,
        "research_summary": research_summary
    }

    review_link = f"http://127.0.0.1:8000/review-outline/{book_id}"

    # Send email
    await send_email(
        subject="Outline Ready For Review",
        recipient=book["editor_email"],
        body=f"Review outline here: {review_link}"
    )

    return RedirectResponse(
        review_link,
        status_code=303
    )