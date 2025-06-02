# prompts.py

def sentence_extraction_prompt(title, text):
    return f"""
You are analyzing a clinical note for an AML (acute myeloid leukemia) cancer patient.
Extract only the most relevant sentences that provide evidence for the following categories:

1. AML Diagnosis Date
2. Precedent Disease (including disease name and date of mention)
3. Performance Status at Baseline:
   - ECOG (0–4) or KPS score
   - With date if mentioned
4. Mutational Status (NPM1, RUNX1, TP53, FLT3, ASXL1 genes)

Title: {title}

Document:
{text}

Return a JSON object in this format:

{{
  "document_title": "{title}",
  "aml_diagnosis_sentences": [],
  "precedent_disease_sentences": [],
  "performance_status_sentences": [],
  "mutational_status_sentences": []
}}

Only include sentences that are relevant and contain medical evidence.
"""
