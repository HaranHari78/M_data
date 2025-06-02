def sentence_extraction_prompt(title, text):
    return f"""
You are analyzing a clinical note for an AML (acute myeloid leukemia) patient.
Extract only the sentences that contain strong evidence for the following categories:

1. AML Diagnosis Date
2. Precedent Disease (name + date)
3. Performance Status at Baseline:
   - ECOG (0–4) or KPS score with date
4. Mutational Status (genes: NPM1, RUNX1, TP53, FLT3, ASXL1)

Document Title: {title}

Text:
{text}

Return a JSON in the format:
{{
  "document_title": "{title}",
  "aml_diagnosis_sentences": [],
  "precedent_disease_sentences": [],
  "performance_status_sentences": [],
  "mutational_status_sentences": []
}}

Only include sentences that clearly contain the relevant evidence.
"""
