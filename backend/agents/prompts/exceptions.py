from core.exceptions import TvaritException

class PromptException(TvaritException):
    """Base exception for prompt operations."""
    pass

class PromptTemplateException(PromptException):
    def __init__(self, message: str = "Error in prompt template"):
        super().__init__(message, code="PROMPT_TEMPLATE_ERROR", status_code=500)

class VariableMissingException(PromptException):
    def __init__(self, message: str = "Required prompt variable is missing"):
        super().__init__(message, code="PROMPT_VARIABLE_MISSING", status_code=400)

class TemplateNotFoundException(PromptException):
    def __init__(self, message: str = "Prompt template not found"):
        super().__init__(message, code="TEMPLATE_NOT_FOUND", status_code=404)
