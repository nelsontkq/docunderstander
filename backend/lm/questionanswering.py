import base64
from transformers import DonutProcessor, VisionEncoderDecoderModel
import torch
from PIL import Image
import io
from dateutil.parser import parse
import re

processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
model = VisionEncoderDecoderModel.from_pretrained(
    # "nelsntk/donut-docvqa-v3"
    "naver-clova-ix/donut-base-finetuned-docvqa"
)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)


def prompt(base64_image: str, user_inputs: list[str]):
    try:
        image_data = base64.b64decode(base64_image)
        image_stream = io.BytesIO(image_data)
        image_stream.seek(0)  # Ensure you're at the start of the stream
        image = Image.open(image_stream)
        # Ensure image is in RGB format
        if image.mode != 'RGB':
            image = image.convert('RGB')
    except IOError:
        raise ValueError("Cannot identify image file. Ensure that the image data is valid and properly encoded.")
    pixel_values = processor(image, return_tensors="pt").pixel_values
    for user_input in user_inputs:
        prompt = f"<s_docvqa><s_question>{user_input}</s_question><s_answer>"
        decoder_input_ids = processor.tokenizer(prompt, add_special_tokens=False, return_tensors="pt").input_ids
        outputs = model.generate(
            pixel_values.to(device),
            decoder_input_ids=decoder_input_ids.to(device),
            max_length=model.decoder.config.max_position_embeddings,
            pad_token_id=processor.tokenizer.pad_token_id,
            eos_token_id=processor.tokenizer.eos_token_id,
            use_cache=True,
            bad_words_ids=[[processor.tokenizer.unk_token_id]],
            return_dict_in_generate=True,
        )
        sequence = processor.batch_decode(outputs.sequences)[0]
        sequence = sequence.replace(processor.tokenizer.eos_token, "").replace(processor.tokenizer.pad_token, "")
        sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()  # remove first task start token
        yield processor.token2json(sequence)["answer"]


def field_map(field_type: str, answer: str):
    if field_type == "string":
        return answer
    if field_type == "iso_date":
        return parse(answer).isoformat()
    if field_type == "number":
        return re.sub(r"[^\d\.]", "", answer)
    return answer


def answer_questions(docdata: str, questions: list[dict]):
    just_questions = [question["question"] for question in questions]
    result = {}
    for i, j in enumerate(prompt(docdata, just_questions)):
        result[questions[i]["field"]] = field_map(questions[i]["field_type"], j)
    return result
