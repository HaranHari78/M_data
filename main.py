import json
import re
import os
import pandas as pd
import httpx
from prompts import sentence_extraction_prompt
from schemas import function_schema
from utils import load_config, call_openai_api
from openai import AzureOpenAI

# Configuration
openai_config = load_config()
model = openai_config['gpt_models']['model_gpt4o']
input_file = r"C:\Users\HariharaM12\Downloads\medicaldata.csv"

# Output folder and files
output_dir = 'output'
sentence_output_file = os.path.join(output_dir, 'extracted_sentences.json')
structured_output_file = os.path.join(output_dir, 'structured_data.json')
os.makedirs(output_dir, exist_ok=True)

sentence_results = []
structured_results = []

def clean_json_response(response: str):
    if not response or not isinstance(response, str):
        return ""
    cleaned = re.sub(r'```(?:json)?\n?|\\n?```', '', response).strip()
    cleaned = cleaned.replace('\n', ' ')
    return cleaned

def call_openai_with_function(text, model, function_schema):
    custom_http_client = httpx.Client(verify=False, timeout=60.0)

    client = AzureOpenAI(
        api_key=openai_config["azure_openai"]["api_key"],
        api_version=openai_config["azure_openai"]["api_version"],
        azure_endpoint=openai_config["azure_openai"]["endpoint"],
        http_client=custom_http_client
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a medical data analyst extracting structured cancer patient data from clinical text. Only extract fields supported by strong evidence."},
                {"role": "user", "content": text}
            ],
            functions=function_schema,
            function_call={"name": "extract_cancer_patient_data"}
        )
        return response.choices[0].message.function_call.arguments
    except Exception as e:
        print("❌ Function calling failed:", e)
        return None

# Read CSV
df = pd.read_csv(input_file, encoding='utf-8')

for index, row in df.iterrows():
    title = row.get('title', "")
    text = row.get('text', "")
    print(f"\n[🔍 Step 1: Extracting sentences for]: {title[:60]}")

    if not text:
        continue

    # Sentence Extraction
    prompt1 = sentence_extraction_prompt(title, text)
    sentence_response = call_openai_api(prompt1, model)
    if not sentence_response:
        continue

    cleaned_sentence_response = clean_json_response(sentence_response)
    try:
        extracted_sentences = json.loads(cleaned_sentence_response)
        sentence_results.append(extracted_sentences)
    except json.JSONDecodeError:
        print("⚠️ Error decoding sentence JSON.")
        continue

    # Combine sentences for structured extraction
    combined_sentences = ". ".join(
        extracted_sentences.get('aml_diagnosis_sentences', []) +
        extracted_sentences.get('precedent_disease_sentences', []) +
        extracted_sentences.get('performance_status_sentences', []) +
        extracted_sentences.get('mutational_status_sentences', [])
    )

    print(f"[🧠 Step 2: Extracting fields for]: {title[:60]}")
    structured_json = call_openai_with_function(combined_sentences, model, function_schema)
    if not structured_json:
        continue

    try:
        structured_data = json.loads(structured_json)
        structured_data["document_title"] = title
        structured_results.append(structured_data)
    except json.JSONDecodeError:
        print("⚠️ Error decoding structured JSON.")
        continue

# Save outputs
with open(sentence_output_file, 'w', encoding='utf-8') as f:
    json.dump(sentence_results, f, indent=4)

with open(structured_output_file, 'w', encoding='utf-8') as f:
    json.dump(structured_results, f, indent=4)

print("\n✅ All records processed and saved.")
