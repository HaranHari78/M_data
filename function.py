# schemas.py

function_schema = [
    {
        "name": "extract_cancer_patient_data",
        "description": "Extracts detailed structured information from clinical notes of cancer patients.",
        "parameters": {
            "type": "object",
            "properties": {
                "document_title": {"type": "string"},
                "aml_diagnosis_date": {
                    "type": "object",
                    "properties": {
                        "value": {"type": "string"},
                        "evidence": {"type": "string"}
                    },
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
                "patient_age": {"type": "string"},
                "gender": {"type": "string"},
                "treatment_plan": {"type": "string"},
                "risk_classification": {"type": "string"},
                "response_to_treatment": {"type": "string"}
            },
            "required": ["document_title", "aml_diagnosis_date"]
        }
    }
]
