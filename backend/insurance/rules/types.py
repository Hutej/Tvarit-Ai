from enum import Enum

class RuleStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"
    NOT_APPLICABLE = "NOT_APPLICABLE"

class RuleCategory(str, Enum):
    CLINICAL = "CLINICAL"
    ADMINISTRATIVE = "ADMINISTRATIVE"
    DEMOGRAPHIC = "DEMOGRAPHIC"
    COMPLETENESS = "COMPLETENESS"

class RulePriority(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
