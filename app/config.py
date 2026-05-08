from dotenv import load_dotenv
import os

load_dotenv()

OPENAPI_API_KEY=os.getenv("OPENAPI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
SUPABASE_URL=os.getenv("SUPABASE_URL")
SUPABASE_KEY=os.getenv("SUPABASE_KEY")
MAIL_USER=os.getenv("MAIL_USER")
MAIL_PASSWORD=os.getenv("MAIL_PASSWORD")
MAIL_FROM=os.getenv("MAIL_FROM")
MAIL_PORT=os.getenv("MAIL_PORT")
MAIL_SERVER=os.getenv("MAIL_SERVER")
MAIL_TLS=os.getenv("MAIL_TLS")
MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME")
