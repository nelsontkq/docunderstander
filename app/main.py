from typing import Union

from fastapi import FastAPI
from backend.lm.questionanswering import answer_questions
from backend.models import DocumentQA

app = FastAPI()

@app.post("/documentqna")
def read_item(request: DocumentQA):
    body = request.model_dump()
    try:
        result = answer_questions(body["document"], body["items"])
        return result
    except Exception as e:
        return {"error": str(e)}
