from core.exceptions import TvaritException

class RuleException(TvaritException):
    """Base exception for rule operations."""
    pass

class RuleExecutionException(RuleException):
    def __init__(self, message: str = "Rule execution failed"):
        super().__init__(message, code="RULE_EXECUTION_ERROR", status_code=500)

class RuleRegistrationException(RuleException):
    def __init__(self, message: str = "Rule registration failed"):
        super().__init__(message, code="RULE_REGISTRATION_ERROR", status_code=500)
