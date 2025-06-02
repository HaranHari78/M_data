sentence_extraction_prompt = """
You will be given a medical document. Extract only the relevant sentences for the following categories:
- AML diagnosis
- Precedent diseases
- Performance status (ECOG or KPS)
- Mutational status (TP53, FLT3, etc.)

Return ONLY valid JSON in this format — no explanation, no markdown, no comments:

{
  "document_title": "<title>",
  "aml_diagnosis_sentences": [],
  "precedent_disease_sentences": [],
  "performance_status_sentences": [],
  "mutational_status_sentences": []
}

Do not add markdown syntax like ```json. Output must be pure JSON only.
"""


field_extraction_prompt = """
You are given pre-filtered sentences from a medical document. From them, extract structured information in this format:

{
  "document_title": "<title>",
  "aml_diagnosis_date": {"value": "", "evidence": ""},
  "precedent_disease": [
    {"name": "", "date": "", "evidence": ""}
  ],
  "performance_status": {
    "ecog_score": {"value": "", "date": "", "evidence": ""},
    "kps_score": {"value": "", "date": "", "evidence": ""}
  },
  "mutational_status": {
    "TP53": {"status": "", "date": "", "evidence": ""},
    "FLT3": {"status": "", "date": "", "evidence": ""},
    "NPM1": {"status": "", "date": "", "evidence": ""},
    "RUNX1": {"status": "", "date": "", "evidence": ""},
    "ASXL1": {"status": "", "date": "", "evidence": ""}
  }
}
Only use the extracted sentences. Be accurate and do not hallucinate.
"""
