from typing import List, Optional, Any
from schemas.knowledge_base import PatientKnowledgeBase
from insurance.templates.models import ProcedureTemplate
from insurance.gap_analysis.types import EvidenceCategory, EvidenceStatus
from insurance.gap_analysis.result import EvidenceItem

class DeterministicMatcher:
    """
    Performs exact and case-insensitive deterministic matching.
    """
    
    @staticmethod
    def _match_list(required: List[str], provided: List[str], category: EvidenceCategory) -> List[EvidenceItem]:
        results = []
        prov_lower = [p.lower() for p in provided if p]
        
        for req in required:
            if not req:
                continue
                
            req_lower = req.lower()
            # Check for exact case-insensitive substring match
            matched_val = next((p for p in provided if p and req_lower in p.lower()), None)
            
            if matched_val:
                results.append(EvidenceItem(
                    category=category,
                    requirement=req,
                    status=EvidenceStatus.MATCHED,
                    matched_value=matched_val,
                    reason="Exact or substring match found."
                ))
            else:
                results.append(EvidenceItem(
                    category=category,
                    requirement=req,
                    status=EvidenceStatus.MISSING,
                    reason=f"Missing required {category.value.lower().replace('_', ' ')}."
                ))
        return results

    @classmethod
    def match_diagnoses(cls, template: ProcedureTemplate, kb: PatientKnowledgeBase) -> List[EvidenceItem]:
        provided = []
        if kb.clinical and kb.clinical.diagnoses:
            provided = [d.description for d in kb.clinical.diagnoses if d.description] + \
                       [d.code for d in kb.clinical.diagnoses if d.code]
        return cls._match_list(template.required_diagnoses, provided, EvidenceCategory.DIAGNOSIS)

    @classmethod
    def match_documents(cls, template: ProcedureTemplate, kb: PatientKnowledgeBase) -> List[EvidenceItem]:
        # Using document titles, notes titles or file names if available
        provided = []
        if kb.clinical and kb.clinical.notes:
            provided = [n.title for n in kb.clinical.notes if n.title]
        return cls._match_list(template.required_documents, provided, EvidenceCategory.DOCUMENT)

    @classmethod
    def match_clinical_findings(cls, template: ProcedureTemplate, kb: PatientKnowledgeBase) -> List[EvidenceItem]:
        provided = []
        if kb.clinical and kb.clinical.physical_exam:
            provided.append(kb.clinical.physical_exam)
        if kb.clinical and kb.clinical.symptoms:
            provided.extend(kb.clinical.symptoms)
        return cls._match_list(template.required_clinical_findings, provided, EvidenceCategory.CLINICAL_FINDING)

    @classmethod
    def match_imaging(cls, template: ProcedureTemplate, kb: PatientKnowledgeBase) -> List[EvidenceItem]:
        provided = []
        if kb.clinical and kb.clinical.imaging_reports:
            provided = [img.procedure_name for img in kb.clinical.imaging_reports if img.procedure_name]
        return cls._match_list(template.required_imaging, provided, EvidenceCategory.IMAGING)

    @classmethod
    def match_medications(cls, template: ProcedureTemplate, kb: PatientKnowledgeBase) -> List[EvidenceItem]:
        provided = []
        if kb.clinical and kb.clinical.medications:
            provided = [m.name for m in kb.clinical.medications if m.name]
        return cls._match_list(template.required_medications, provided, EvidenceCategory.MEDICATION)

    @classmethod
    def match_conservative_treatment(cls, template: ProcedureTemplate, kb: PatientKnowledgeBase) -> List[EvidenceItem]:
        provided = []
        if kb.clinical and kb.clinical.conservative_treatments:
            provided = kb.clinical.conservative_treatments
        # Fallback to medications if it's pharmacological conservative treatment
        if kb.clinical and kb.clinical.medications:
            provided.extend([m.name for m in kb.clinical.medications if m.name])
        return cls._match_list(template.required_conservative_treatment, provided, EvidenceCategory.CONSERVATIVE_TREATMENT)

    @classmethod
    def match_lab_results(cls, template: ProcedureTemplate, kb: PatientKnowledgeBase) -> List[EvidenceItem]:
        provided = []
        if kb.clinical and kb.clinical.lab_results:
            provided = [lab.test_name for lab in kb.clinical.lab_results if lab.test_name]
        return cls._match_list(template.required_lab_results, provided, EvidenceCategory.LAB_RESULT)

    @classmethod
    def match_provider_types(cls, template: ProcedureTemplate, kb: PatientKnowledgeBase) -> List[EvidenceItem]:
        provided = []
        if kb.providers:
            provided = [p.specialty for p in kb.providers if p.specialty]
        return cls._match_list(template.required_provider_types, provided, EvidenceCategory.PROVIDER_TYPE)

    @classmethod
    def match_insurance(cls, template: ProcedureTemplate, kb: PatientKnowledgeBase) -> List[EvidenceItem]:
        results = []
        if not kb.administrative or not kb.administrative.insurance_details:
            results.append(EvidenceItem(
                category=EvidenceCategory.INSURANCE,
                requirement="Valid Insurance Details",
                status=EvidenceStatus.MISSING,
                reason="Patient insurance details are missing."
            ))
        else:
             results.append(EvidenceItem(
                category=EvidenceCategory.INSURANCE,
                requirement="Valid Insurance Details",
                status=EvidenceStatus.MATCHED,
                matched_value="Present",
                reason="Patient insurance details are verified."
            ))
        return results
