sentence_extraction_prompt = """
You are an expert medical assistant. Given a clinical note, extract relevant sentences for the following:

1. AML diagnosis
2. Precedent diseases
3. Performance status (ECOG or KPS scores)
4. Mutational status (NPM1, TP53, FLT3, etc.)

Format:
{
  "document_title": "",
  "aml_diagnosis_sentences": [],
  "precedent_disease_sentences": [],
  "performance_status_sentences": [],
  "mutational_status_sentences": []
}
"""

field_extraction_prompt = """
You will receive categorized clinical sentences. From this, extract structured patient cancer information.

Format:
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
    "TP53": {"status": "", "date": "", "evidence": ""},
    "FLT3": {"status": "", "date": "", "evidence": ""}
  },
  "patient_age": "",
  "gender": "",
  "disease_stage": "",
  "treatment_plan": "",
  "response_to_treatment": "",
  "relapse_status": "",
  "cytogenetic_profile": "",
  "bone_marrow_blast_percentage": "",
  "hemoglobin_level": "",
  "wbc_count": "",
  "platelet_count": "",
  "ldh_level": ""
}
"""
---

Let me know when you want me to export these as individual files — or continue here. ​:contentReference[oaicite:0]{index=0}​
