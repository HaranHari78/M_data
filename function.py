# schemas.py

function_schema = [
    {
        "name": "extract_cancer_patient_data",
        "description": "Extract structured cancer patient data from clinical notes. Include diagnosis, prior disease history, mutation profile, treatment details, and other relevant oncology metrics.",
        "parameters": {
            "type": "object",
            "properties": {
                "document_title": {"type": "string"},

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
                            "disease": {"type": "string"},
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

                // 🔽 Additional Cancer-Related Fields
                "patient_age": {"type": "string"},
                "gender": {"type": "string"},
                "disease_stage": {"type": "string"},
                "treatment_plan": {"type": "string"},
                "response_to_treatment": {"type": "string"},
                "relapse_status": {"type": "string"},
                "cytogenetic_profile": {"type": "string"},
                "bone_marrow_blast_percentage": {"type": "string"},
                "hemoglobin_level": {"type": "string"},
                "wbc_count": {"type": "string"},
                "platelet_count": {"type": "string"},
                "ldh_level": {"type": "string"}
            },
            "required": ["document_title", "aml_diagnosis_date"]
        }
    }
]
