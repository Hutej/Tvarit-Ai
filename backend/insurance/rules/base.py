from abc import ABC, abstractmethod
from typing import List, Any
from schemas.knowledge_base import PatientKnowledgeBase
from insurance.rules.types import RuleCategory, RulePriority, RuleStatus
from insurance.rules.result import RuleResult

class Rule(ABC):
    """
    Abstract base class for all Prior Authorization rules.
    """
    
    @property
    @abstractmethod
    def rule_id(self) -> str:
        pass
        
    @property
    @abstractmethod
    def name(self) -> str:
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        pass
        
    @property
    @abstractmethod
    def priority(self) -> RulePriority:
        pass
        
    @property
    @abstractmethod
    def category(self) -> RuleCategory:
        pass
        
    @property
    @abstractmethod
    def required_fields(self) -> List[str]:
        pass

    @abstractmethod
    def evaluate(self, kb: PatientKnowledgeBase) -> RuleResult:
        """
        Evaluate the rule against the knowledge base.
        Must return a RuleResult.
        """
        pass

    def build_result(
        self, 
        status: RuleStatus, 
        reason: str, 
        evidence: List[str] = None,
        missing_fields: List[str] = None,
        recommendation: str = None,
        confidence: float = 1.0
    ) -> RuleResult:
        """
        Helper to construct the RuleResult.
        """
        return RuleResult(
            rule_id=self.rule_id,
            name=self.name,
            category=self.category,
            priority=self.priority,
            status=status,
            reason=reason,
            evidence=evidence or [],
            missing_fields=missing_fields or [],
            recommendation=recommendation,
            confidence=confidence
        )
