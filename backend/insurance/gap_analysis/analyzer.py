from schemas.knowledge_base import PatientKnowledgeBase
from insurance.templates.models import ProcedureTemplate
from insurance.gap_analysis.types import RiskLevel, EvidenceStatus, EvidenceCategory
from insurance.gap_analysis.result import GapAnalysisResult, EvidenceItem
from insurance.gap_analysis.matcher import DeterministicMatcher

class GapAnalyzer:
    """
    Compares PatientKnowledgeBase against ProcedureTemplate to identify missing evidence.
    """

    def analyze(self, kb: PatientKnowledgeBase, template: ProcedureTemplate) -> GapAnalysisResult:
        result = GapAnalysisResult(
            procedure_code=template.procedure_code,
            procedure_name=template.procedure_name
        )

        all_evidence: list[EvidenceItem] = []
        
        # Run matchers
        all_evidence.extend(DeterministicMatcher.match_diagnoses(template, kb))
        all_evidence.extend(DeterministicMatcher.match_documents(template, kb))
        all_evidence.extend(DeterministicMatcher.match_clinical_findings(template, kb))
        all_evidence.extend(DeterministicMatcher.match_imaging(template, kb))
        all_evidence.extend(DeterministicMatcher.match_medications(template, kb))
        all_evidence.extend(DeterministicMatcher.match_conservative_treatment(template, kb))
        all_evidence.extend(DeterministicMatcher.match_lab_results(template, kb))
        all_evidence.extend(DeterministicMatcher.match_provider_types(template, kb))
        all_evidence.extend(DeterministicMatcher.match_insurance(template, kb))

        # Categorize results
        for item in all_evidence:
            if item.status == EvidenceStatus.MATCHED:
                result.matched_evidence.append(item)
            elif item.status == EvidenceStatus.MISSING:
                result.missing_evidence.append(item)
            elif item.status == EvidenceStatus.PARTIAL:
                result.partial_evidence.append(item)
            elif item.status == EvidenceStatus.CONFLICTING:
                result.conflicting_evidence.append(item)

        total_requirements = len(all_evidence)
        matched_count = len(result.matched_evidence)
        missing_count = len(result.missing_evidence)
        
        # Completeness
        if total_requirements > 0:
            result.overall_completeness = round((matched_count / total_requirements) * 100, 2)
        else:
            result.overall_completeness = 100.0

        # Readiness Score and Risk Level
        score = 100
        critical_missing = 0
        
        for item in result.missing_evidence:
            if item.category in [EvidenceCategory.DIAGNOSIS, EvidenceCategory.CLINICAL_FINDING]:
                score -= 20
                critical_missing += 1
            elif item.category in [EvidenceCategory.IMAGING, EvidenceCategory.CONSERVATIVE_TREATMENT]:
                score -= 15
                critical_missing += 1
            elif item.category == EvidenceCategory.INSURANCE:
                score -= 25
                critical_missing += 1
            else:
                score -= 5
                
        result.readiness_score = max(0, min(100, score))
        
        if result.readiness_score >= 90:
            result.risk_level = RiskLevel.LOW
        elif result.readiness_score >= 70:
            result.risk_level = RiskLevel.MEDIUM
        elif result.readiness_score >= 40:
            result.risk_level = RiskLevel.HIGH
        else:
            result.risk_level = RiskLevel.CRITICAL

        # Generate Deterministic Recommendations
        recommendations = []
        for item in result.missing_evidence:
            rec = f"Upload or provide evidence for {item.category.value.lower().replace('_', ' ')}: {item.requirement}"
            recommendations.append(rec)
            
        result.recommendations = list(dict.fromkeys(recommendations))
        
        # Next Best Actions (Prioritize critical categories)
        critical_categories = [
            EvidenceCategory.INSURANCE, 
            EvidenceCategory.DIAGNOSIS, 
            EvidenceCategory.CLINICAL_FINDING, 
            EvidenceCategory.IMAGING
        ]
        
        next_actions = []
        for item in result.missing_evidence:
            if item.category in critical_categories:
                next_actions.append(f"CRITICAL: Address missing {item.category.value.replace('_', ' ')} - {item.requirement}")
                
        for item in result.missing_evidence:
            if item.category not in critical_categories:
                next_actions.append(f"Add missing {item.category.value.replace('_', ' ')} - {item.requirement}")
                
        result.next_best_actions = next_actions

        # Summary
        if result.risk_level == RiskLevel.LOW:
            result.summary = "Submission is highly complete and ready for prior authorization."
        elif result.risk_level == RiskLevel.MEDIUM:
            result.summary = "Submission is mostly complete but missing some supporting evidence."
        else:
            result.summary = f"Submission is incomplete. Missing {missing_count} critical elements."

        return result
