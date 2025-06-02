import json
import os
import pandas as pd
import re
from utils import load_config, call_openai_with_functions
from prompts import sentence_extraction_prompt, field_extraction_prompt
from schemas import sentence_extraction_schema, field_extraction_schema

# Load config
config = load_config()
model = config['gpt_models']['model_gpt4o']

# File paths
input_file = "medicaldata.csv"
sentence_output_file = "output/extracted_sentences.json"
structured_output_file = "output/structured_data.json"

# Create output directory
os.makedirs("output", exist_ok=True)

# Result containers
sentence_results = []
structured_results = []

# JSON cleanup (optional)
def clean_json_response(response: str):
    if not response or not isinstance(response, str):
        return ""
    return re.sub(r'```(?:json)?\n?|\n?```', '', response).strip()

# Read CSV input
df = pd.read_csv(input_file)

# Processing each row
for index, row in df.iterrows():
    title = row.get("title", "").strip()
    text = row.get("text", "").strip()

    if not title or not text:
        print(f"[⚠️ Skipping empty row at index {index}]")
        continue

    print(f"\n[🔍 Step 1: Extracting sentences for]: {title}")

    # Step 1: Extract sentences
    sentence_response = call_openai_with_functions(
        model=model,
        messages=[{"role": "user", "content": sentence_extraction_prompt + f"\n\n{text}"}],
        functions=[sentence_extraction_schema],
        function_call={"name": sentence_extraction_schema["name"]}
    )

    if not sentence_response:
        print(f"[❌] Sentence extraction failed for {title}")
        continue

    sentence_response["document_title"] = title
    sentence_results.append(sentence_response)

    print(f"[🔍 Step 2: Extracting structured fields for]: {title}")

    # Step 2: Extract fields using extracted sentences
    sentence_json_str = json.dumps(sentence_response)

    field_response = call_openai_with_functions(
        model=model,
        messages=[{"role": "user", "content": field_extraction_prompt + f"\n\n{sentence_json_str}"}],
        functions=[field_extraction_schema],
        function_call={"name": field_extraction_schema["name"]}
    )

    if not field_response:
        print(f"[❌] Field extraction failed for {title}")
        continue

    field_response["document_title"] = title
    structured_results.append(field_response)

# Save all extracted sentence results
with open(sentence_output_file, 'w', encoding='utf-8') as f:
    json.dump(sentence_results, f, indent=2)

# Save all structured data results
with open(structured_output_file, 'w', encoding='utf-8') as f:
    json.dump(structured_results, f, indent=2)

print("\n✅ Extraction complete. Output saved in 'output/' folder.")
