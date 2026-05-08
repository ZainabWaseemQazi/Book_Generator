from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import home, outline, review, chapters, compile

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(home.router)
app.include_router(outline.router)
app.include_router(review.router)
app.include_router(chapters.router)
app.include_router(compile.router)