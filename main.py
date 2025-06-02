import os
import json
import pandas as pd
import re
import asyncio
from utils import load_config, call_openai_api_async
from prompts import sentence_extraction_prompt, field_extraction_prompt

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

async def process_row(index, row):
    title = row.get("title", "")
    text = row.get("text", "")

    print(f"[🔍 Step 1: Extracting sentences for]: {title}")
    sentence_response = await call_openai_api_async(sentence_extraction_prompt + f"\n\n{text}", model)
    cleaned_sentences = clean_json_response(sentence_response)

    try:
        sentence_json = json.loads(cleaned_sentences)
        sentence_results.append(sentence_json)
    except Exception as e:
        print(f"[❌] Sentence parsing failed for {title}: {e}")
        return

    print(f"[🧠 Step 2: Extracting fields for]: {title}")
    field_response = await call_openai_api_async(field_extraction_prompt + f"\n\n{cleaned_sentences}", model)
    cleaned_fields = clean_json_response(field_response)

    try:
        structured_json = json.loads(cleaned_fields)
        structured_results.append(structured_json)
    except Exception as e:
        print(f"[❌] Field parsing failed for {title}: {e}")

async def main():
    df = pd.read_csv(input_file)
    tasks = [process_row(index, row) for index, row in df.iterrows()]
    await asyncio.gather(*tasks)

    with open(sentence_output_file, 'w', encoding='utf-8') as f:
        json.dump(sentence_results, f, indent=2)

    with open(structured_output_file, 'w', encoding='utf-8') as f:
        json.dump(structured_results, f, indent=2)

if __name__ == "__main__":
    asyncio.run(main())
