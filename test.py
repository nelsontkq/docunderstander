import requests
import base64
from sys import argv
url = "http://localhost:8000/documentqna"

def get_answers(filename):
    with open(filename, "rb") as f:
        base64_file = base64.b64encode(f.read()).decode('utf-8')
    data = {
        "document_type": "closing_disclosure",
        "document": base64_file,
        "items": [
            {
                "question": "What is the Interest Rate?",
                "field": "interest_rate",
                "field_type": "string"
            },
            {
                "question": "When is the closing date?",
                "field": "closing_date",
                "field_type": "iso_date"
            }
        ]
    }
    response = requests.post(url, json=data)
    return response.text

print(get_answers(argv[1]))