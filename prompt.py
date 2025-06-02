sentence_extraction_prompt = """
You are given a medical document. Extract only relevant sentences under each category:
- AML diagnosis
- Precedent diseases (mention disease name and date)
- Performance status (ECOG, KPS)
- Mutational status (e.g., TP53, FLT3)

Output JSON format:
{
  "document_title": "<title>",
  "aml_diagnosis_sentences": [],
  "precedent_disease_sentences": [],
  "performance_status_sentences": [],
  "mutational_status_sentences": []
}
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
