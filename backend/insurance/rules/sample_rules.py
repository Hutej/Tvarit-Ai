from typing import List
from schemas.knowledge_base import PatientKnowledgeBase
from insurance.rules.base import Rule
from insurance.rules.types import RuleCategory, RulePriority, RuleStatus
from insurance.rules.registry import RuleRegistry

class PatientExistsRule(Rule):
    @property
    def rule_id(self) -> str: return "CMP-001"
    
    @property
    def name(self) -> str: return "Patient Information Exists"
    
    @property
    def description(self) -> str: return "Validates that basic patient demographics exist."
    
    @property
    def priority(self) -> RulePriority: return RulePriority.CRITICAL
    
    @property
    def category(self) -> RuleCategory: return RuleCategory.COMPLETENESS
    
    @property
    def required_fields(self) -> List[str]: return ["patient.name", "patient.dob"]

    def evaluate(self, kb: PatientKnowledgeBase) -> 'RuleResult':
        if not kb.patient:
            return self.build_result(
                status=RuleStatus.FAILED,
                reason="No patient information found.",
                missing_fields=["patient"],
                recommendation="Provide a document containing patient demographics."
            )
            
        missing = []
        if not kb.patient.first_name and not kb.patient.last_name:
            missing.append("patient.name")
        if not kb.patient.date_of_birth:
            missing.append("patient.dob")
            
        if missing:
            return self.build_result(
                status=RuleStatus.FAILED,
                reason="Incomplete patient demographics.",
                missing_fields=missing,
                recommendation="Ensure patient name and date of birth are present."
            )
            
        return self.build_result(
            status=RuleStatus.PASSED,
            reason="Patient demographics are complete.",
            evidence=[f"Patient: {kb.patient.first_name} {kb.patient.last_name}"]
        )

class DiagnosisExistsRule(Rule):
    @property
    def rule_id(self) -> str: return "CMP-002"
    
    @property
    def name(self) -> str: return "Diagnosis Exists"
    
    @property
    def description(self) -> str: return "Validates that at least one diagnosis is present."
    
    @property
    def priority(self) -> RulePriority: return RulePriority.CRITICAL
    
    @property
    def category(self) -> RuleCategory: return RuleCategory.CLINICAL
    
    @property
    def required_fields(self) -> List[str]: return ["clinical.diagnoses"]

    def evaluate(self, kb: PatientKnowledgeBase) -> 'RuleResult':
        if not kb.clinical or not kb.clinical.diagnoses:
            return self.build_result(
                status=RuleStatus.FAILED,
                reason="No diagnoses found.",
                missing_fields=["clinical.diagnoses"],
                recommendation="Provide a clinical note or referral containing the diagnosis."
            )
            
        diagnoses_str = [d.description or d.code for d in kb.clinical.diagnoses if d.description or d.code]
        return self.build_result(
            status=RuleStatus.PASSED,
            reason=f"Found {len(kb.clinical.diagnoses)} diagnoses.",
            evidence=diagnoses_str
        )

class InsuranceExistsRule(Rule):
    @property
    def rule_id(self) -> str: return "CMP-003"
    
    @property
    def name(self) -> str: return "Insurance Details Exist"
    
    @property
    def description(self) -> str: return "Validates that payer/insurance details are present."
    
    @property
    def priority(self) -> RulePriority: return RulePriority.HIGH
    
    @property
    def category(self) -> RuleCategory: return RuleCategory.ADMINISTRATIVE
    
    @property
    def required_fields(self) -> List[str]: return ["administrative.insurance_details"]

    def evaluate(self, kb: PatientKnowledgeBase) -> 'RuleResult':
        if not kb.administrative or not kb.administrative.insurance_details:
            return self.build_result(
                status=RuleStatus.WARNING,
                reason="No insurance details found. This might be a cash pay or details might be in another document.",
                missing_fields=["administrative.insurance_details"],
                recommendation="Provide insurance card or face sheet."
            )
            
        return self.build_result(
            status=RuleStatus.PASSED,
            reason="Insurance details are present."
        )

# Register the sample rules
RuleRegistry.register(PatientExistsRule)
RuleRegistry.register(DiagnosisExistsRule)
RuleRegistry.register(InsuranceExistsRule)
