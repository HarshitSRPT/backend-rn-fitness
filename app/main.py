from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import forms

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://rnfitness.fit",
        "https://www.rnfitness.fit",
        "https://api.rnfitness.fit",
        "https://rn-fitness.vercel.app",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
def health():
    return {"status": "ok"}


app.include_router(forms.router, prefix="/api")
