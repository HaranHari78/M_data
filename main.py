import json
import os
import pandas as pd
import re
from utils import load_config, call_openai_function
from prompts import sentence_extraction_prompt, field_extraction_prompt
from schemas import sentence_extraction_schema, field_extraction_schema

config = load_config()
model = config['gpt_models']['model_gpt4o']
input_file = "medicaldata.csv"
sentence_output_file = "output/extracted_sentences.json"
structured_output_file = "output/structured_data.json"

os.makedirs("output", exist_ok=True)
sentence_results = []
structured_results = []

def clean_json_response(response: str):
    if not response or not isinstance(response, str):
        return ""
    cleaned = re.sub(r'```(?:json)?\n?|\n?```', '', response).strip()
    return cleaned

df = pd.read_csv(input_file)

for index, row in df.iterrows():
    title = row.get("title", "")
    text = row.get("text", "")
    print(f"\n[🔍 Step 1: Extracting sentences for]: {title}")

    # 🔹 Sentence extraction using function calling
    sentence_function_call = {
        "name": sentence_extraction_schema["name"]
    }

    sentence_response = call_openai_function(
        model=model,
        prompt=sentence_extraction_prompt + f"\n\n{text}",
        functions=[sentence_extraction_schema],
        function_call=sentence_function_call
    )

    if not sentence_response:
        continue

    sentence_json = sentence_response.get("arguments", {})
    sentence_results.append(sentence_json)

    print(f"[🔍 Step 2: Extracting structured fields for]: {title}")

    # 🔹 Field extraction using function calling
    field_function_call = {
        "name": field_extraction_schema["name"]
    }

    field_response = call_openai_function(
        model=model,
        prompt=field_extraction_prompt + f"\n\n{json.dumps(sentence_json)}",
        functions=[field_extraction_schema],
        function_call=field_function_call
    )

    if field_response:
        structured_json = field_response.get("arguments", {})
        structured_results.append(structured_json)

# Save outputs
with open(sentence_output_file, 'w', encoding='utf-8') as f:
    json.dump(sentence_results, f, indent=2)

with open(structured_output_file, 'w', encoding='utf-8') as f:
    json.dump(structured_results, f, indent=2)
