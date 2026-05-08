from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.database import supabase

router = APIRouter()
templates = Jinja2Templates(directory="app/template")


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={}
)

@router.post("/create-book")
def create_book(
    title: str = Form(...),
    editor_email: str = Form(...),
    notes: str = Form(...)
):

    result = supabase.table("books").insert({
        "title": title,
        "editor_email": editor_email,
        "status": "outline_pending"
    }).execute()

    book_id = result.data[0]["id"]

    return RedirectResponse(
        url=f"/generate-outline/{book_id}?notes={notes}",
        status_code=303
    )