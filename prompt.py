# prompts.py

def build_function_prompt(title, text):
    return f"""
You are given a clinical note for an AML (Acute Myeloid Leukemia) patient.
Extract all relevant structured information in JSON format.

Document Title: {title}
Document Text:
{text}

Return only a JSON object with the following structure:
{{
  "aml_diagnosis_date": {{ "value": "", "evidence": "" }},
  "precedent_disease": [
    {{ "name": "", "date": "", "evidence": "" }}
  ],
  "performance_status": {{
    "ecog_score": {{ "value": "", "date": "", "evidence": "" }},
    "kps_score": {{ "value": "", "date": "", "evidence": "" }}
  }},
  "mutational_status": {{
    "NPM1": {{"status": "", "date": "", "evidence": ""}},
    "RUNX1": {{"status": "", "date": "", "evidence": ""}},
    "TP53": {{"status": "", "date": "", "evidence": ""}},
    "FLT3": {{"status": "", "date": "", "evidence": ""}},
    "ASXL1": {{"status": "", "date": "", "evidence": ""}}
  }},
  "age": "", 
  "gender": "",
  "treatment_plan": "",
  "risk_score": "",
  "physician_notes_summary": ""
}}

Strictly follow the JSON structure. If data is missing, use empty strings.
    """

def extraction_function_schema():
    return {
        "name": "extract_aml_patient_data",
        "description": "Extract AML-related patient details from clinical notes.",
        "parameters": {
            "type": "object",
            "properties": {
                "aml_diagnosis_date": {
                    "type": "object",
                    "properties": {
                        "value": {"type": "string"},
                        "evidence": {"type": "string"}
                    }
                },
                "precedent_disease": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "date": {"type": "string"},
                            "evidence": {"type": "string"}
                        }
                    }
                },
                "performance_status": {
                    "type": "object",
                    "properties": {
                        "ecog_score": {
                            "type": "object",
                            "properties": {
                                "value": {"type": "string"},
                                "date": {"type": "string"},
                                "evidence": {"type": "string"}
                            }
                        },
                        "kps_score": {
                            "type": "object",
                            "properties": {
                                "value": {"type": "string"},
                                "date": {"type": "string"},
                                "evidence": {"type": "string"}
                            }
                        }
                    }
                },
                "mutational_status": {
                    "type": "object",
                    "properties": {
                        "NPM1": {"type": "object", "properties": {"status": {"type": "string"}, "date": {"type": "string"}, "evidence": {"type": "string"}}},
                        "RUNX1": {"type": "object", "properties": {"status": {"type": "string"}, "date": {"type": "string"}, "evidence": {"type": "string"}}},
                        "TP53": {"type": "object", "properties": {"status": {"type": "string"}, "date": {"type": "string"}, "evidence": {"type": "string"}}},
                        "FLT3": {"type": "object", "properties": {"status": {"type": "string"}, "date": {"type": "string"}, "evidence": {"type": "string"}}},
                        "ASXL1": {"type": "object", "properties": {"status": {"type": "string"}, "date": {"type": "string"}, "evidence": {"type": "string"}}}
                    }
                },
                "age": {"type": "string"},
                "gender": {"type": "string"},
                "treatment_plan": {"type": "string"},
                "risk_score": {"type": "string"},
                "physician_notes_summary": {"type": "string"}
            },
            "required": ["aml_diagnosis_date", "precedent_disease", "performance_status", "mutational_status"]
        }
    }
