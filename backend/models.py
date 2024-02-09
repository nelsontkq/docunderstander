
from fastapi import File
from pydantic import BaseModel, Field, Base64Bytes

class DocumentQuestion(BaseModel):
    question: str = Field(..., title="The question to ask", examples=["What is the order amount?"])
    field: str = Field(..., title="The field to extract", examples=["order_amount"])
    field_type: str = Field(..., title="The type of field", examples=["string", "iso_date", "number"])


class DocumentQA(BaseModel):
    document_type: str = Field(..., title="The type of document", examples=["closing_disclosure"])
    document: Base64Bytes = Field(..., title="The base64 to process")
    items: list[DocumentQuestion] = Field(..., title="The list of questions to ask")
