import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

app = FastAPI(title="LegalEase API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DocumentRequest(BaseModel):
    doc_type: str
    details: str

@app.get("/")
def home():
    return {"message": "LegalEase Backend API is Running!"}

@app.post("/generate-document")
def generate_document(req: DocumentRequest):
    try:
        # Full model path explicitly passed
        model = genai.GenerativeModel('models/gemini-3.5-flash')
        prompt = f"Generate a professional, legally structured draft for a {req.doc_type}. Key Details: {req.details}"
        response = model.generate_content(prompt)
        return {"status": "success", "document": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))