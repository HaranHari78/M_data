import os
import pandas as pd
import json
import asyncio
from utils import load_config, async_openai_chat
from prompts import sentence_extraction_prompt, field_extraction_prompt

config = load_config()
model = config['gpt_models']['model_gpt4o']

input_file = "medicaldata.csv"
sentence_output_file = "output/extracted_sentences.json"
structured_output_file = "output/structured_data.json"
os.makedirs("output", exist_ok=True)

sentence_results = []
structured_results = []

async def extract_for_row(title, text):
    print(f"\n[🔍 Step 1: Extracting sentences for]: {title}")
    sentence_prompt = sentence_extraction_prompt + f"\n\nDocument Title: {title}\n{text}"
    sentence_response = await async_openai_chat(sentence_prompt, model)
    if not sentence_response:
        return None, None

    try:
        sentence_json = json.loads(sentence_response)
        sentence_results.append(sentence_json)
    except json.JSONDecodeError:
        print("⚠️ Sentence extraction JSON parse error.")
        return None, None

    print(f"[🔍 Step 2: Extracting structured fields for]: {title}")
    field_prompt = field_extraction_prompt + f"\n\n{sentence_response}"
    field_response = await async_openai_chat(field_prompt, model)
    if not field_response:
        return sentence_json, None

    try:
        field_json = json.loads(field_response)
        structured_results.append(field_json)
    except json.JSONDecodeError:
        print("⚠️ Field extraction JSON parse error.")

    return sentence_json, field_response

async def main():
    df = pd.read_csv(input_file)
    tasks = []
    for _, row in df.iterrows():
        title = row.get("title", "")
        text = row.get("text", "")
        tasks.append(extract_for_row(title, text))

    await asyncio.gather(*tasks)

    with open(sentence_output_file, 'w', encoding='utf-8') as f:
        json.dump(sentence_results, f, indent=2)

    with open(structured_output_file, 'w', encoding='utf-8') as f:
        json.dump(structured_results, f, indent=2)

if __name__ == "__main__":
    asyncio.run(main())
