from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import pandas as pd
import pickle

from sentence_transformers import SentenceTransformer

from Duplicate_Incident_API.duplicate_detector import DuplicateDetector


app = FastAPI(
    title="SALEM Duplicate Incident Detection API"
)


class ReportRequest(BaseModel):
    description: str

BASE_DIR = Path(__file__).resolve().parent
print("Loading Dataset...")

df = pd.read_csv(
    BASE_DIR / "reports_clean.csv"
)

print("Loading Embeddings...")

with open(
    BASE_DIR / "report_embeddings.pkl",
    "rb"
) as f:

    embeddings = pickle.load(f)

print("Loading SBERT Model...")

model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

detector = DuplicateDetector(
    model,
    embeddings,
    df
)

print("API Ready")


@app.get("/")
def home():

    return {
        "message":
        "Duplicate Detection API Running"
    }


@app.post("/check-duplicate")
def check_duplicate(
    report: ReportRequest
):

    result = detector.check_duplicate(
        report.description
    )

    return result