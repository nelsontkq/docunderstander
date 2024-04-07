from typing import Union

import torch
from fastapi import FastAPI
from app.lm.questionanswering import answer_questions
from app.models import DocumentQA

app = FastAPI()
if not torch.cuda.is_available():
    raise ValueError("Cuda not enabled!")

@app.post("/documentqna")
def read_item(request: DocumentQA):
    body = request.model_dump()
    try:
        result = answer_questions(body["document"], body["items"])
        return result
    except Exception as e:
        return {"error": str(e)}
