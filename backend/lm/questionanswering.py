from transformers import pipeline
import tempfile
from dateutil.parser import parse
import re
nlp = pipeline(
    "document-question-answering",
    model="impira/layoutlm-document-qa",
)

def field_map(field_type: str, answer: str):
    if field_type == "string":
        return answer
    if field_type == "iso_date":
        return parse(answer).isoformat()
    if field_type == "number":
        return re.sub("[^\d\.]", "", answer)
    return answer


def answer_questions(docdata: str, questions: list[dict]):

    answer = {}
    meta = {}
    for question in questions:
        result = nlp(docdata,
                     question["question"]
        )
        answer[question["field"]] =  field_map(question["field_type"], result[0]["answer"])
        meta[question["field"]] = result
    return {"answer": answer, "meta": meta}