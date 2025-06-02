sentence_extraction_prompt = """
You will be given a medical document. Extract the **relevant sentences only** for each of the following categories:
- AML diagnosis
- Precedent diseases
- Performance status (ECOG, KPS)
- Mutational status (e.g., NPM1, TP53)

Output must be in JSON format as:
{
  "document_title": "",
  "aml_diagnosis_sentences": [],
  "precedent_disease_sentences": [],
  "performance_status_sentences": [],
  "mutational_status_sentences": []
}
"""

field_extraction_prompt = """
You will receive grouped sentences relevant to a patient's cancer data.
From these, extract the following fields:

Return the output in this format:
{
  "document_title": "",
  "aml_diagnosis_date": {"value": "", "evidence": ""},
  "precedent_disease": [
    {"name": "", "date": "", "evidence": ""}
  ],
  "performance_status": {
    "ecog_score": {"value": "", "date": "", "evidence": ""},
    "kps_score": {"value": "", "date": "", "evidence": ""}
  },
  "mutational_status": {
    "NPM1": {"status": "", "date": "", "evidence": ""},
    "RUNX1": {"status": "", "date": "", "evidence": ""},
    "TP53": {"status": "", "date": "", "evidence": ""},
    "FLT3": {"status": "", "date": "", "evidence": ""},
    "ASXL1": {"status": "", "date": "", "evidence": ""}
  }
}
"""
