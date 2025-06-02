from typing import List, Dict, Any
from openai.types.chat import FunctionDefinition

sentence_extraction_schema: FunctionDefinition = {
    "name": "extract_relevant_sentences",
    "description": "Extract relevant sentences from the medical note for specific categories.",
    "parameters": {
        "type": "object",
        "properties": {
            "document_title": {"type": "string"},
            "aml_diagnosis_sentences": {"type": "array", "items": {"type": "string"}},
            "precedent_disease_sentences": {"type": "array", "items": {"type": "string"}},
            "performance_status_sentences": {"type": "array", "items": {"type": "string"}},
            "mutational_status_sentences": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["document_title"]
    }
}

field_extraction_schema: FunctionDefinition = {
    "name": "extract_structured_fields",
    "description": "Extract structured cancer-related data from previously extracted sentences.",
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
                    "NPM1": {"type": "object", "properties": {
                        "status": {"type": "string"}, "date": {"type": "string"}, "evidence": {"type": "string"}}},
                    "RUNX1": {"type": "object", "properties": {
                        "status": {"type": "string"}, "date": {"type": "string"}, "evidence": {"type": "string"}}},
                    "TP53": {"type": "object", "properties": {
                        "status": {"type": "string"}, "date": {"type": "string"}, "evidence": {"type": "string"}}},
                    "FLT3": {"type": "object", "properties": {
                        "status": {"type": "string"}, "date": {"type": "string"}, "evidence": {"type": "string"}}},
                    "ASXL1": {"type": "object", "properties": {
                        "status": {"type": "string"}, "date": {"type": "string"}, "evidence": {"type": "string"}}}
                }
            }
        },
        "required": ["document_title", "aml_diagnosis_date"]
    }
}
