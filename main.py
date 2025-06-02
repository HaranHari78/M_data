import json
import re
import pandas as pd
from prompts import sentence_extraction_prompt
from schemas import function_schema
from utils import load_config, call_openai_api

# Configuration
openai_config = load_config()
model = openai_config['gpt_models']['model_gpt4o']
input_file = r"C:\Users\HariharaM12\Downloads\medicaldata.csv"
sentence_output_file = 'extracted_sentences.json'
structured_output_file = 'structured_data.json'
sentence_results = []
structured_results = []

def clean_json_response(response: str):
    if not response or not isinstance(response, str):
        return ""
    cleaned = re.sub(r'```(?:json)?\n?|\n?```', '', response).strip()
    cleaned = cleaned.replace('\n', ' ')
    return cleaned

def call_openai_with_function(text, model, function_schema):
    from openai import AzureOpenAI
    openai_config = load_config()

    # ✅ FIX: Use the same custom client from utils.py
    custom_http_client = httpx.Client(verify=False)

    client = AzureOpenAI(
        api_key=openai_config["azure_openai"]["api_key"],
        api_version=openai_config["azure_openai"]["api_version"],
        azure_endpoint=openai_config["azure_openai"]["endpoint"],
        http_client=custom_http_client  # ✅ ADD THIS
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a medical data analyst extracting structured cancer patient data from clinical text. Be precise and fill only fields with strong evidence."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            functions=function_schema,
            function_call={"name": "extract_cancer_patient_data"}
        )
        return response.choices[0].message.function_call.arguments
    except Exception as e:
        print("Function calling failed:", e)
        return None

# Read input data
df = pd.read_csv(input_file, encoding='utf-8')

for index, row in df.iterrows():
    title = row.get('title', "")
    text = row.get('text', "")
    print(f"\n[🔍 Analyzing]: {title[:60]}...")

    if not text:
        continue

    # Step 1 - Sentence extraction
    prompt1 = sentence_extraction_prompt(title, text)
    sentence_response = call_openai_api(prompt1, model)
    if not sentence_response:
        continue
    cleaned_sentence_response = clean_json_response(sentence_response)
    try:
        extracted_sentences = json.loads(cleaned_sentence_response)
        sentence_results.append(extracted_sentences)
    except json.JSONDecodeError:
        print("⚠️ Error decoding sentence extraction.")
        continue

    # Step 2 - Function Calling Extraction
    combined_sentences = ". ".join(
        extracted_sentences.get('aml_diagnosis_sentences', []) +
        extracted_sentences.get('precedent_disease_sentences', []) +
        extracted_sentences.get('performance_status_sentences', []) +
        extracted_sentences.get('mutational_status_sentences', [])
    )

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

# Save results
with open(sentence_output_file, 'w', encoding='utf-8') as f:
    json.dump(sentence_results, f, indent=4)

with open(structured_output_file, 'w', encoding='utf-8') as f:
    json.dump(structured_results, f, indent=4)

print("\n✅ Data saved successfully.")
