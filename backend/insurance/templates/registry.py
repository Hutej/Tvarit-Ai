from typing import Dict, List, Optional
from insurance.templates.models import ProcedureTemplate

class TemplateRegistry:
    """
    Registry for managing Procedure Templates.
    """
    _templates_by_code: Dict[str, ProcedureTemplate] = {}

    @classmethod
    def register(cls, template: ProcedureTemplate) -> None:
        cls._templates_by_code[template.procedure_code.upper()] = template

    @classmethod
    def get(cls, procedure_code: str) -> Optional[ProcedureTemplate]:
        return cls._templates_by_code.get(procedure_code.upper())

    @classmethod
    def list(cls) -> List[ProcedureTemplate]:
        return list(cls._templates_by_code.values())

    @classmethod
    def find_by_code(cls, code: str) -> Optional[ProcedureTemplate]:
        return cls.get(code)

    @classmethod
    def find_by_name(cls, name: str) -> Optional[ProcedureTemplate]:
        name_lower = name.lower()
        for t in cls.list():
            if t.procedure_name.lower() == name_lower:
                return t
            for alias in t.aliases:
                if alias.lower() == name_lower:
                    return t
        return None
