from schemas.knowledge_base import PatientKnowledgeBase
from insurance.rules.result import RuleEvaluationResult, RuleResult
from insurance.rules.registry import RuleRegistry
from insurance.rules.types import RuleStatus, RulePriority

class RuleEngine:
    """
    Evaluates all registered rules against a PatientKnowledgeBase.
    """

    def evaluate(self, kb: PatientKnowledgeBase) -> RuleEvaluationResult:
        result = RuleEvaluationResult()
        
        all_rules = RuleRegistry.get_all_rules()
        total_applicable = 0
        passed_applicable = 0
        
        score = 100

        for rule_cls in all_rules:
            rule_instance = rule_cls()
            
            try:
                rule_result = rule_instance.evaluate(kb)
            except Exception as e:
                # If a rule crashes, treat it as a warning/failure
                rule_result = rule_instance.build_result(
                    status=RuleStatus.FAILED,
                    reason=f"Rule evaluation crashed: {str(e)}",
                    recommendation="Review rule logic."
                )

            # Categorize the result
            if rule_result.status == RuleStatus.PASSED:
                result.passed_rules.append(rule_result)
                total_applicable += 1
                passed_applicable += 1
            elif rule_result.status == RuleStatus.FAILED:
                result.failed_rules.append(rule_result)
                total_applicable += 1
                # Adjust score
                if rule_result.priority == RulePriority.CRITICAL:
                    score -= 30
                elif rule_result.priority == RulePriority.HIGH:
                    score -= 20
                elif rule_result.priority == RulePriority.MEDIUM:
                    score -= 15
                elif rule_result.priority == RulePriority.LOW:
                    score -= 5
            elif rule_result.status == RuleStatus.WARNING:
                result.warnings.append(rule_result)
                total_applicable += 1
                # Small deduction for warnings
                if rule_result.priority in [RulePriority.CRITICAL, RulePriority.HIGH]:
                    score -= 5
            elif rule_result.status == RuleStatus.NOT_APPLICABLE:
                result.not_applicable.append(rule_result)
                
            # Collect missing fields and recommendations
            if rule_result.missing_fields:
                result.all_missing_fields.extend(rule_result.missing_fields)
            if rule_result.recommendation:
                result.global_recommendations.append(rule_result.recommendation)

        # Ensure score is within 0-100
        result.readiness_score = max(0, min(100, score))
        
        if total_applicable > 0:
            result.completion_percentage = round((passed_applicable / total_applicable) * 100, 2)
        else:
            result.completion_percentage = 0.0
            
        # Deduplicate global recommendations and missing fields
        result.global_recommendations = list(dict.fromkeys(result.global_recommendations))
        result.all_missing_fields = list(dict.fromkeys(result.all_missing_fields))

        return result
