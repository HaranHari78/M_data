import json
import re
import os
import pandas as pd
import httpx
from schemas import function_schema
from utils import load_config
from openai import AzureOpenAI

# Configuration
openai_config = load_config()
model = openai_config['gpt_models']['model_gpt4o']
input_file = r"C:\Users\HariharaM12\Downloads\medicaldata.csv"

# Output folder and file
output_dir = 'output'
structured_output_file = os.path.join(output_dir, 'structured_data.json')

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

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

    custom_http_client = httpx.Client(verify=False, timeout=60.0)  # ⬅️ Set 60s timeout

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
                {"role": "system", "content": "You are a medical data analyst extracting structured cancer patient data from clinical text."},
                {"role": "user", "content": text}
            ],
            functions=function_schema,
            function_call={"name": "extract_cancer_patient_data"}
        )
        return response.choices[0].message.function_call.arguments
    except Exception as e:
        print("❌ Function calling failed:", e)
        return None


# Read input data
df = pd.read_csv(input_file, encoding='utf-8')

# Process each record
for index, row in df.iterrows():
    title = row.get('title', "")
    text = row.get('text', "")
    print(f"\n[🔍 Extracting from]: {title[:60]}...")

    if not text:
        continue

    structured_json = call_openai_with_function(text, model, function_schema)
    if not structured_json:
        continue

    try:
        structured_data = json.loads(structured_json)
        structured_data["document_title"] = title
        structured_results.append(structured_data)
    except json.JSONDecodeError:
        print("⚠️ Error decoding structured JSON.")
        continue

# Save output
with open(structured_output_file, 'w', encoding='utf-8') as f:
    json.dump(structured_results, f, indent=4)

print("\n✅ Cancer-related structured data extracted and saved.")
print(f"📝 Output saved to: {structured_output_file} ({len(structured_results)} records)")
