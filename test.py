import requests
import base64
import time
from pdf2image import convert_from_path
 
from sys import argv
url = "http://146.235.198.112:8000/documentqna"

def get_answers(filename):
    if filename.endswith(".pdf"):
        images = convert_from_path(filename)
        filename = filename.replace(".pdf", ".png")
        images[0].save(filename, 'PNG')
    with open(filename, "rb") as f:
        base64_file = base64.b64encode(f.read()).decode('utf-8')
    data = {
        "document_type": "whatever_document", # purely for logging
        "document": base64_file,
        "items": [
            {
                "question": "What is the Order Number?",
                "field": "order_number",
                "field_type": "string"
            },
            {
                "question": "What is the total?",
                "field": "total",
                "field_type": "string"
            }
        ]
    }

    start_time = time.time()
    response = requests.post(url, json=data)
    print(f"Time taken (seconds): {round(time.time() - start_time, 2)}\n\n")
    return response.text

print(get_answers(argv[1]))