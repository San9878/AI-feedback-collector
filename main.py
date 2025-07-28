from fastapi import FastAPI
from pydantic import BaseModel
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = FastAPI()

class Feedback(BaseModel):
    prompt: str
    response: str
    rating: str
    comment: str

@app.post("/submit-feedback")
def submit(data: Feedback):
    result = supabase.table("feedbacks").insert(data.dict()).execute()
    return {"message": "saved", "data": result.data}

@app.get("/feedbacks")
def get_all():
    result = supabase.table("feedbacks").select("*").order("created_at", desc=True).execute()
    return result.data